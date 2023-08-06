#!/usr/bin/env python3

from curses.ascii import islower
from functools import partial
import io
from textwrap import dedent, indent
from asdl_parse import mk_parser, run_lexer, Tokens
import parser_rts as rts
from typing import Iterator, List, TextIO, Tuple
import requests
from pathlib import Path

import ast
from astuce.inference import safe_infer
from astuce.parser import parse as astuce_parse
from astuce.nodes import nodes_of_class, get_if_statement_ancestor
from astor import to_source
import attr

_parse = mk_parser()

def parse(text: str, filename: str = "unknown"):
    tokens = list(run_lexer(filename, text))

    res = _parse(None, Tokens(tokens))
    if res[0]:
        return res[1]
    msgs = []
    assert res[1]
    maxline = 0
    for each in res[1]:
        i, msg = each
        token = tokens[i]
        lineno = token.lineno
        maxline = max(lineno, maxline)
        colno = token.colno
        msgs.append(f"Line {lineno + 1}, column {colno}, {msg}")

    e = SyntaxError()
    e.lineno = maxline + 1
    e.msg = "\n".join(msgs)
    e.filename = filename
    off = token.offset
    e.offset = off
    e.text = text[: text.find("\n", off)]
    raise e

def get_ann(stub_ast: ast.Module, typename:str, field:str) -> str:
    try:
        annassign = stub_ast.locals[typename][0].locals[field][0].statement
    except KeyError:
        return 'Any'
    assert isinstance(annassign, ast.AnnAssign), ast.dump(annassign)
    ann = annassign.annotation
    unparsed = to_source(ann).strip()
    # Workaround the extra parenthesis added by the to_source() function.
    if unparsed.startswith('(') and unparsed.endswith(')'):
        unparsed = unparsed[1:-1]
    # Workaround special cases in _ast.pyi
    return unparsed\
        .replace('_Identifier', 'str')\
        .replace('_Pattern', 'pattern')\
        .replace('_Slice', 'slice')

def get_abstract_classdefs(stub_ast: ast.Module, spec_names: List[str], python_version:Tuple[int,int]) -> Iterator[ast.ClassDef]:
    classdefs = nodes_of_class(stub_ast, ast.ClassDef)
    clss = [cls for cls in classdefs if cls.name not in spec_names and cls.name.islower()]
    for cls in clss:
        maybeif = get_if_statement_ancestor(cls)
        if isinstance(maybeif, ast.If) and \
            isinstance(maybeif.test, ast.Compare) and \
            isinstance(maybeif.test.left, ast.Attribute) and to_source(maybeif.test.left).strip() == "sys.version_info" and \
            isinstance(maybeif.test.ops[0], ast.GtE):
                assert safe_infer(maybeif.test.comparators[0]) is not None
                python_version_guard = ast.literal_eval(safe_infer(maybeif.test.comparators[0]))
                class_location = maybeif.locate_child(cls, recurse=True)[0]
                if class_location == 'body':
                    if python_version < python_version_guard:
                        continue
                elif class_location == 'orelse':
                    if python_version >= python_version_guard:
                        continue
                else:
                    assert False
                
                yield cls
        else:
            yield cls

def get_base_of_class(stub_ast: ast.Module, name:str) -> str:
    cls = stub_ast.locals[name][0]
    assert isinstance(cls, ast.ClassDef)
    assert len(cls.bases)==1
    return to_source(cls.bases[0]).strip().replace('_Slice', 'slice')


base_visitor_src = '''
class _BaseRewriter(Generic[T_i, T_o, T_p]):
      
  def visit(self, ob: T_i, parent:Optional[T_p]) -> T_o:
    """Visit a node and return the new node."""
    method = 'visit_' + ob.__class__.__name__
    visitor = getattr(self, method, self.unknown_visit)
    return visitor(ob, parent)

  def unknown_visit(self, ob: T_i, parent:Optional[T_p]) -> T_o:
    """
    Called when entering unknown object types.
    Raise an exception unless overridden.
    """
    raise NotImplementedError(
        '%s visiting unknown object type: %s'
        % (self.__class__, ob.__class__.__name__))
'''

rewriter_src = '''

_PrimitiveType = Any 
# More like [Literal[None, True, False], str, int] with elipsis as well.

_InputT = Union[ast.AST, _PrimitiveType]
_OutputT = Union[nodes.AST, _PrimitiveType]
_ParentT = nodes.AST

class Rewriter(_BaseRewriter[_InputT, _OutputT, _ParentT]):
    """Rewrites ast"""

    def __init__(self, nodes:NodesT=Nodes) -> None:
        """
        @param nodes: Namespace that contains all the nodes classes.
            It can be a module or a subclass of Nodes.
        """
        self.nodes = nodes

    # handle primitive types, not nodes.
    def unknown_visit(self, ob: Any, parent:Optional[nodes.AST]) -> Any:
        return ob
'''

main_src = '''

if __name__ == "__main__":
   # Reads a file to ast.AST, store module. 
   # Transform the module to the new node classes.
   # assert that ast.dump(old) == ast.dump(new). 
   # assert that for every AST child, the parent attribute is set. 
   # print success. 

   from pathlib import Path
   from sys import argv

   file = Path(argv[1:][0])
   src = file.read_text()
   mod = ast.parse(src, file.as_posix())
   new_mod = Rewriter().visit(mod, None)
   assert ast.dump(mod) == ast.dump(new_mod)
   for node in ast.walk(new_mod):
        if not isinstance(node, ast.Module):
            assert node.parent is not None
        else:
            assert node.parent is None

'''

def format_rewriter(io:TextIO, 
                          specs: List[Tuple[str, List[Tuple[str, str]]]], 
                          stub_ast: ast.Module, 
                          python_version: Tuple[int,int]):
    def l(_l:str, level=0):
        io.write(indent(_l, '    '*level) + "\n")

    version_str = ''.join(str(v) for v in python_version)
    l(f'''"""AST rewriter for python {'.'.join(str(v) for v in python_version)}"""''')
    l("# this file is auto-generated, please don't edit it directly.")

    l("import ast, builtins")
    l("from typing import Any, Generic, TypeVar, Optional, Union, Protocol, Type, TYPE_CHECKING, overload")
    l("if TYPE_CHECKING:")
    l("from typing import Literal", level=1)

    # Import nodes modules relatively.
    l(f"from ..nodes import nodes{version_str} as nodes")
    l("")
    l("class NodesT(Protocol):")
    # generate the Protocol for the nodes.py module.
    for typename, fields in specs:
        l(f"{typename}: Type[nodes.{typename}]", level=1)
    l("")

    l("class Nodes(NodesT):")
    l(f'''"""Class that aliases all concrete node classes as found in nodes{version_str}.py file."""''', level=1)
    # generate the default implementation of the NodesT Protocol.
    for typename, fields in specs:
        l(f"{typename} = nodes.{typename}", level=1)
    l("")

    l("T_i = TypeVar('T_i')")
    l("T_o = TypeVar('T_o')")
    l("T_p = TypeVar('T_p')")

    l(base_visitor_src)
    l(rewriter_src)
    l("")

    # generate the overloads for visit() methods.
    l("if TYPE_CHECKING:", level=1)

    for typename in [s[0] for s in specs] + \
        [cls.name for cls in list(get_abstract_classdefs(stub_ast, [s[0] for s in specs], python_version))]:
        l("@overload", level=2)
        l(f"def visit(self, node:ast.{typename}, parent:Optional[nodes.AST]) -> nodes.{typename}:...", level=2)
    
    # primitive types
    l("@overload", level=2)
    l(f"def visit(self, node:str, parent:Optional[nodes.AST]) -> str:...", level=2)
    l("@overload", level=2)
    l(f"def visit(self, node:bool, parent:Optional[nodes.AST]) -> bool:...", level=2)
    l("@overload", level=2)
    l(f"def visit(self, node:int, parent:Optional[nodes.AST]) -> int:...", level=2)
    l("@overload", level=2)
    l(f"def visit(self, node:Any, parent:Optional[nodes.AST]) -> Any:...", level=2)

    l(f"def visit(self, node:_InputT, parent:Optional[_ParentT]) -> _OutputT:...", level=2)
    l("")
    for typename, fields in specs:
        l(f"def visit_{typename}(self, node:ast.{typename}, parent:nodes.AST) -> nodes.{typename}:", level=1)

        l(f"newnode = self.nodes.{typename}(", level=2)
        l(f"parent = parent,", level=3)
        for attr in ['lineno', 'col_offset', 'end_lineno', 'end_col_offset']:
            default_value = '-1'
            l(f"{attr} = getattr(node, {attr!r}, {default_value}),", level=3)
        l(f")", level=2)
        l("")

        for type, field in fields:
            annotation = get_ann(stub_ast, typename, field)
            
            if annotation.startswith('list['):
                l(f"{field} = [self.visit(n, newnode) for n in node.{field}]", level=2)
            else:
                l(f"{field} = self.visit(node.{field}, newnode)", level=2)
        l("")
        if len(fields)>0:
            l(f"newnode._postinit(", level=2)
            for type, field in fields:
                l(f"{field} = {field},", level=3)

            l(f")", level=2)
            l("")
        l(f"return newnode", level=2)
        l("")
    
    l(main_src)

def format_augmented_nodes(io:TextIO, 
                          specs: List[Tuple[str, List[Tuple[str, str]]]], 
                          stub_ast: ast.Module, 
                          python_version: Tuple[int,int]) -> str:
    def l(_l:str, level=0):
        io.write(indent(_l, '    '*level) + "\n")

    l(f'''"""AST nodes for python {'.'.join(str(v) for v in python_version)}"""''')
    l("# this file is auto-generated, please don't edit it directly.")

    if python_version>= (3,7):
        l("from __future__ import annotations")
    l("import ast")
    l("from typing import Optional, Any, TYPE_CHECKING")
    l("if TYPE_CHECKING:")
    l("from typing import Literal", level=1)
    l("_unset:Any = object()")
    l("_unset_init:Any = object()")
    
    init_signature = '''(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None'''
    init_code:str = indent(dedent(f'''
        def __init__{init_signature}:
            self.parent = parent
            self.lineno = lineno
            self.col_offset = col_offset
            self.end_lineno = end_lineno
            self.end_col_offset = end_col_offset'''), prefix='        ')
    subclass_init:str = indent(dedent(f'''
        def __init__{init_signature}:
            super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
    '''), prefix='    ')
    
    base_lines = dedent(f"""
    class AST(ast.AST):
        {init_code}
    """).splitlines()
    
    for line in base_lines:
        l(line)
    l("")
    
    all_annotations = []
    _last_abstract_class = None
    for abstract_class in get_abstract_classdefs(stub_ast, [s[0] for s in specs]+['AST'], python_version=python_version):
        typename = abstract_class.name
        if _last_abstract_class and _last_abstract_class.name == 'expr' and typename != 'slice':
            l("# special case slice.")
            l("slice = expr")
        l(f"class {typename}(ast.{typename}, AST): ...")
        _last_abstract_class = abstract_class
    l("")

    for typename, fields in specs:
        # TODO: Add suport for extra base classes
        # replace 'AST' by the class name from typeshed.
        # generate all classes from typeshed that are not in the
        # spec at the begining of the file. 
        l(f"class {typename}(ast.{typename}, {get_base_of_class(stub_ast, typename)}):")
        if not fields:
            args = ""
        else:
            args = "".join(f", {field}:{get_ann(stub_ast, typename, field)!r}=_unset" for type, field in fields)
        for _line in subclass_init.splitlines():
            l(_line)

        indent_string = f"        "
        if args:
            # complete __init__ with _unset_init values. 
            l(f"{indent_string}# all fields defaults to _unset_init")
            for type, field in fields:
                l(f"{indent_string}self.{field} = _unset_init")
            l("")
            
            # define postinit for AST fields only.
            l(f"    def _postinit(self{args}) -> None:")
            
            l(f'{indent_string}"""start checking validation"""')
            for type, field in fields:
                if type == rts.noDefault:
                    l(
                        indent_string
                        + f'if {field} is _unset: raise ValueError({field + " cannot be empty."!r})'
                    )
                elif type == rts.defaultList:
                    l(indent_string + f"if {field} is _unset: {field} = []")
                elif type == rts.defaultNone:
                    l(indent_string + f"if {field} is _unset: {field} = None")
            
            for type, field in fields:
                ignore = ""
                if type == rts.defaultList:
                    ignore = " #type:ignore"
                
                l(f"{indent_string}self.{field} = {field}{ignore}")

                all_annotations += [get_ann(stub_ast, typename, field)]
        l("")

    for ann in sorted(set(all_annotations)):
        l(f"# {ann}")

def generate_rewriter(python_version: Tuple[int, int]) -> str:
    major, minor = python_version
    asdl_url = f"https://raw.githubusercontent.com/python/cpython/{major}.{minor}/Parser/Python.asdl"
    
    asdl_text = requests.get(asdl_url).text
    asdl_specs = parse(asdl_text, asdl_url)

    f = io.StringIO()
        
    ast_stubs_contents = requests.get('https://raw.githubusercontent.com/python/typeshed/master/stdlib/_ast.pyi').text
    
    format_rewriter(f, asdl_specs, astuce_parse(ast_stubs_contents, modname='_ast'), python_version=python_version)
    return f.getvalue()

def generate_augmented_nodes(python_version: Tuple[int, int]) -> str:
    """
    Returns a standalone module string containing all new AST nodes.
    New AST nodes have a supplementary attribute: 'parent' and 
    their __init__ signature is not compatible with older nodes.
    """
    major, minor = python_version
    asdl_url = f"https://raw.githubusercontent.com/python/cpython/{major}.{minor}/Parser/Python.asdl"
    
    asdl_text = requests.get(asdl_url).text
    asdl_specs = parse(asdl_text, asdl_url)

    f = io.StringIO()
        
    ast_stubs_contents = requests.get('https://raw.githubusercontent.com/python/typeshed/master/stdlib/_ast.pyi').text
    
    format_augmented_nodes(f, asdl_specs, astuce_parse(ast_stubs_contents, modname='_ast'), python_version=python_version)
    return f.getvalue()

_init_module_top = '''\
from sys import version_info
ver = version_info[:2]    
'''

@attr.s(auto_attribs=True)
class ASTLibraryGenerator:
    """
    Generates {package_name}.nodes and {package_name}.rewriter packages.
    """
    library_path: Path
    python_versions: List[Tuple[int,int]]

    def generate(self, ) -> None:
        self.library_path.mkdir(parents=True, exist_ok=True)
        
        self.write_nodes_init_module()
        self.write_rewriter_init_module()
        self.write_lib_init_module()

        for python_version in self.python_versions:
            self.write_nodes(python_version)
            self.write_rewriter(python_version)
        

    def write_nodes(self, python_version: Tuple[int, int]) -> None:
        src_text = generate_augmented_nodes(python_version)
        major, minor = python_version
        module_path = self.library_path / 'nodes'

        with (module_path / f"nodes{major}{minor}.py").open("w") as f:
            f.write(src_text)

    def write_nodes_init_module(self) -> None:
        # TODO: generate __all__ for all versions.

        module_path = self.library_path / 'nodes'
        module_path.mkdir(parents=True, exist_ok=True)

        with (module_path / f"__init__.py").open("w") as f:
            def l(_l:str, level=0):
                f.write(indent(_l, '    '*level) + "\n")
            
            l(_init_module_top)
            
            for i, pyversion in enumerate(self.python_versions):
                major, minor = pyversion
                _else = '' if i==0 else 'el'
                l(f'{_else}if ver == ({major},{minor}):')
                l(f'from .nodes{major}{minor} import *', level=1)
                
            l("else: raise NotImplementedError(f'python version not supported: {ver}')")

    def write_rewriter(self, python_version: Tuple[int, int]) -> None:
        src_text = generate_rewriter(python_version)
        major, minor = python_version
        module_path = self.library_path / 'rewriter'

        with (module_path / f"rewriter{major}{minor}.py").open("w") as f:
            f.write(src_text)

    def write_rewriter_init_module(self) -> None:
        # TODO: generate __all__ for all versions.
        
        module_path = self.library_path / 'rewriter'
        module_path.mkdir(parents=True, exist_ok=True)

        with (module_path / f"__init__.py").open("w") as f:
            def l(_l:str, level=0):
                f.write(indent(_l, '    '*level) + "\n")
            
            l(_init_module_top)
            
            for i, pyversion in enumerate(self.python_versions):
                major, minor = pyversion
                _else = '' if i==0 else 'el'
                l(f'{_else}if ver == ({major},{minor}):')
                l(f'from .rewriter{major}{minor} import *', level=1)
                
            l("else: raise NotImplementedError(f'python version not supported: {ver}')")

    def write_lib_init_module(self) -> None:
        module_path = self.library_path / '__init__.py'
        module_path.touch()

# TODO: Make the parent argument non-optional
# for everything except the ast.Module 

if __name__ == "__main__":

    """
    Usage
        ./generate_library/generate.py ast_nodes
        # Will generate nodes under ./ast_nodes

        ./generate_library/generate.py ast_nodes ./src/my_lib/
        # Will generate nodes under ./src/my_lib/ast_nodes
    """
    
    from sys import argv
    args = argv[1:]
    
    if len(args)>=1:
        pack_name = args[0]
        assert pack_name.isidentifier(), f"First argument should be the package name, not {args[0]!r}"
        
        if len(args)==1:
            path = Path(pack_name)
        elif len(args)==2:
            path = Path(args[1]) /pack_name
    else:
        assert False, "Script takes at least one argument: the package name"
    
    generator = ASTLibraryGenerator(library_path=path, 
        python_versions=[
            (3,6),
            (3,7),
            (3,8),
            (3,9),
            (3,10),
            (3,11),
        ])

    generator.generate()

    print('Done')
    
    
