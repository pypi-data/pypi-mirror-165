"""AST nodes for python 3.7"""
# this file is auto-generated, please don't edit it directly.
from __future__ import annotations
import ast
from typing import Optional, Any, TYPE_CHECKING
if TYPE_CHECKING:
    from typing import Literal
_unset:Any = object()
_unset_init:Any = object()

class AST(ast.AST):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        self.parent = parent
        self.lineno = lineno
        self.col_offset = col_offset
        self.end_lineno = end_lineno
        self.end_col_offset = end_col_offset

class mod(ast.mod, AST): ...
class stmt(ast.stmt, AST): ...
class expr(ast.expr, AST): ...
class slice(ast.slice, AST): ...
class expr_context(ast.expr_context, AST): ...
class boolop(ast.boolop, AST): ...
class operator(ast.operator, AST): ...
class unaryop(ast.unaryop, AST): ...
class cmpop(ast.cmpop, AST): ...
class excepthandler(ast.excepthandler, AST): ...

class Module(ast.Module, mod):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.body = _unset_init

    def _postinit(self, body:'list[stmt]'=_unset) -> None:
        """start checking validation"""
        if body is _unset: body = []
        self.body = body #type:ignore

class Interactive(ast.Interactive, mod):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.body = _unset_init

    def _postinit(self, body:'list[stmt]'=_unset) -> None:
        """start checking validation"""
        if body is _unset: body = []
        self.body = body #type:ignore

class Expression(ast.Expression, mod):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.body = _unset_init

    def _postinit(self, body:'expr'=_unset) -> None:
        """start checking validation"""
        if body is _unset: raise ValueError('body cannot be empty.')
        self.body = body

class Suite(ast.Suite, mod):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.body = _unset_init

    def _postinit(self, body:'list[stmt]'=_unset) -> None:
        """start checking validation"""
        if body is _unset: body = []
        self.body = body #type:ignore

class FunctionDef(ast.FunctionDef, stmt):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.name = _unset_init
        self.args = _unset_init
        self.body = _unset_init
        self.decorator_list = _unset_init
        self.returns = _unset_init

    def _postinit(self, name:'str'=_unset, args:'arguments'=_unset, body:'list[stmt]'=_unset, decorator_list:'list[expr]'=_unset, returns:'expr | None'=_unset) -> None:
        """start checking validation"""
        if name is _unset: raise ValueError('name cannot be empty.')
        if args is _unset: raise ValueError('args cannot be empty.')
        if body is _unset: body = []
        if decorator_list is _unset: decorator_list = []
        if returns is _unset: returns = None
        self.name = name
        self.args = args
        self.body = body #type:ignore
        self.decorator_list = decorator_list #type:ignore
        self.returns = returns

class AsyncFunctionDef(ast.AsyncFunctionDef, stmt):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.name = _unset_init
        self.args = _unset_init
        self.body = _unset_init
        self.decorator_list = _unset_init
        self.returns = _unset_init

    def _postinit(self, name:'str'=_unset, args:'arguments'=_unset, body:'list[stmt]'=_unset, decorator_list:'list[expr]'=_unset, returns:'expr | None'=_unset) -> None:
        """start checking validation"""
        if name is _unset: raise ValueError('name cannot be empty.')
        if args is _unset: raise ValueError('args cannot be empty.')
        if body is _unset: body = []
        if decorator_list is _unset: decorator_list = []
        if returns is _unset: returns = None
        self.name = name
        self.args = args
        self.body = body #type:ignore
        self.decorator_list = decorator_list #type:ignore
        self.returns = returns

class ClassDef(ast.ClassDef, stmt):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.name = _unset_init
        self.bases = _unset_init
        self.keywords = _unset_init
        self.body = _unset_init
        self.decorator_list = _unset_init

    def _postinit(self, name:'str'=_unset, bases:'list[expr]'=_unset, keywords:'list[keyword]'=_unset, body:'list[stmt]'=_unset, decorator_list:'list[expr]'=_unset) -> None:
        """start checking validation"""
        if name is _unset: raise ValueError('name cannot be empty.')
        if bases is _unset: bases = []
        if keywords is _unset: keywords = []
        if body is _unset: body = []
        if decorator_list is _unset: decorator_list = []
        self.name = name
        self.bases = bases #type:ignore
        self.keywords = keywords #type:ignore
        self.body = body #type:ignore
        self.decorator_list = decorator_list #type:ignore

class Return(ast.Return, stmt):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.value = _unset_init

    def _postinit(self, value:'expr | None'=_unset) -> None:
        """start checking validation"""
        if value is _unset: value = None
        self.value = value

class Delete(ast.Delete, stmt):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.targets = _unset_init

    def _postinit(self, targets:'list[expr]'=_unset) -> None:
        """start checking validation"""
        if targets is _unset: targets = []
        self.targets = targets #type:ignore

class Assign(ast.Assign, stmt):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.targets = _unset_init
        self.value = _unset_init

    def _postinit(self, targets:'list[expr]'=_unset, value:'expr'=_unset) -> None:
        """start checking validation"""
        if targets is _unset: targets = []
        if value is _unset: raise ValueError('value cannot be empty.')
        self.targets = targets #type:ignore
        self.value = value

class AugAssign(ast.AugAssign, stmt):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.target = _unset_init
        self.op = _unset_init
        self.value = _unset_init

    def _postinit(self, target:'expr'=_unset, op:'operator'=_unset, value:'expr'=_unset) -> None:
        """start checking validation"""
        if target is _unset: raise ValueError('target cannot be empty.')
        if op is _unset: raise ValueError('op cannot be empty.')
        if value is _unset: raise ValueError('value cannot be empty.')
        self.target = target
        self.op = op
        self.value = value

class AnnAssign(ast.AnnAssign, stmt):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.target = _unset_init
        self.annotation = _unset_init
        self.value = _unset_init
        self.simple = _unset_init

    def _postinit(self, target:'expr'=_unset, annotation:'expr'=_unset, value:'expr | None'=_unset, simple:'int'=_unset) -> None:
        """start checking validation"""
        if target is _unset: raise ValueError('target cannot be empty.')
        if annotation is _unset: raise ValueError('annotation cannot be empty.')
        if value is _unset: value = None
        if simple is _unset: raise ValueError('simple cannot be empty.')
        self.target = target
        self.annotation = annotation
        self.value = value
        self.simple = simple

class For(ast.For, stmt):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.target = _unset_init
        self.iter = _unset_init
        self.body = _unset_init
        self.orelse = _unset_init

    def _postinit(self, target:'expr'=_unset, iter:'expr'=_unset, body:'list[stmt]'=_unset, orelse:'list[stmt]'=_unset) -> None:
        """start checking validation"""
        if target is _unset: raise ValueError('target cannot be empty.')
        if iter is _unset: raise ValueError('iter cannot be empty.')
        if body is _unset: body = []
        if orelse is _unset: orelse = []
        self.target = target
        self.iter = iter
        self.body = body #type:ignore
        self.orelse = orelse #type:ignore

class AsyncFor(ast.AsyncFor, stmt):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.target = _unset_init
        self.iter = _unset_init
        self.body = _unset_init
        self.orelse = _unset_init

    def _postinit(self, target:'expr'=_unset, iter:'expr'=_unset, body:'list[stmt]'=_unset, orelse:'list[stmt]'=_unset) -> None:
        """start checking validation"""
        if target is _unset: raise ValueError('target cannot be empty.')
        if iter is _unset: raise ValueError('iter cannot be empty.')
        if body is _unset: body = []
        if orelse is _unset: orelse = []
        self.target = target
        self.iter = iter
        self.body = body #type:ignore
        self.orelse = orelse #type:ignore

class While(ast.While, stmt):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.test = _unset_init
        self.body = _unset_init
        self.orelse = _unset_init

    def _postinit(self, test:'expr'=_unset, body:'list[stmt]'=_unset, orelse:'list[stmt]'=_unset) -> None:
        """start checking validation"""
        if test is _unset: raise ValueError('test cannot be empty.')
        if body is _unset: body = []
        if orelse is _unset: orelse = []
        self.test = test
        self.body = body #type:ignore
        self.orelse = orelse #type:ignore

class If(ast.If, stmt):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.test = _unset_init
        self.body = _unset_init
        self.orelse = _unset_init

    def _postinit(self, test:'expr'=_unset, body:'list[stmt]'=_unset, orelse:'list[stmt]'=_unset) -> None:
        """start checking validation"""
        if test is _unset: raise ValueError('test cannot be empty.')
        if body is _unset: body = []
        if orelse is _unset: orelse = []
        self.test = test
        self.body = body #type:ignore
        self.orelse = orelse #type:ignore

class With(ast.With, stmt):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.items = _unset_init
        self.body = _unset_init

    def _postinit(self, items:'list[withitem]'=_unset, body:'list[stmt]'=_unset) -> None:
        """start checking validation"""
        if items is _unset: items = []
        if body is _unset: body = []
        self.items = items #type:ignore
        self.body = body #type:ignore

class AsyncWith(ast.AsyncWith, stmt):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.items = _unset_init
        self.body = _unset_init

    def _postinit(self, items:'list[withitem]'=_unset, body:'list[stmt]'=_unset) -> None:
        """start checking validation"""
        if items is _unset: items = []
        if body is _unset: body = []
        self.items = items #type:ignore
        self.body = body #type:ignore

class Raise(ast.Raise, stmt):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.exc = _unset_init
        self.cause = _unset_init

    def _postinit(self, exc:'expr | None'=_unset, cause:'expr | None'=_unset) -> None:
        """start checking validation"""
        if exc is _unset: exc = None
        if cause is _unset: cause = None
        self.exc = exc
        self.cause = cause

class Try(ast.Try, stmt):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.body = _unset_init
        self.handlers = _unset_init
        self.orelse = _unset_init
        self.finalbody = _unset_init

    def _postinit(self, body:'list[stmt]'=_unset, handlers:'list[ExceptHandler]'=_unset, orelse:'list[stmt]'=_unset, finalbody:'list[stmt]'=_unset) -> None:
        """start checking validation"""
        if body is _unset: body = []
        if handlers is _unset: handlers = []
        if orelse is _unset: orelse = []
        if finalbody is _unset: finalbody = []
        self.body = body #type:ignore
        self.handlers = handlers #type:ignore
        self.orelse = orelse #type:ignore
        self.finalbody = finalbody #type:ignore

class Assert(ast.Assert, stmt):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.test = _unset_init
        self.msg = _unset_init

    def _postinit(self, test:'expr'=_unset, msg:'expr | None'=_unset) -> None:
        """start checking validation"""
        if test is _unset: raise ValueError('test cannot be empty.')
        if msg is _unset: msg = None
        self.test = test
        self.msg = msg

class Import(ast.Import, stmt):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.names = _unset_init

    def _postinit(self, names:'list[alias]'=_unset) -> None:
        """start checking validation"""
        if names is _unset: names = []
        self.names = names #type:ignore

class ImportFrom(ast.ImportFrom, stmt):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.module = _unset_init
        self.names = _unset_init
        self.level = _unset_init

    def _postinit(self, module:'str | None'=_unset, names:'list[alias]'=_unset, level:'int'=_unset) -> None:
        """start checking validation"""
        if module is _unset: module = None
        if names is _unset: names = []
        if level is _unset: level = None
        self.module = module
        self.names = names #type:ignore
        self.level = level

class Global(ast.Global, stmt):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.names = _unset_init

    def _postinit(self, names:'list[str]'=_unset) -> None:
        """start checking validation"""
        if names is _unset: names = []
        self.names = names #type:ignore

class Nonlocal(ast.Nonlocal, stmt):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.names = _unset_init

    def _postinit(self, names:'list[str]'=_unset) -> None:
        """start checking validation"""
        if names is _unset: names = []
        self.names = names #type:ignore

class Expr(ast.Expr, stmt):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.value = _unset_init

    def _postinit(self, value:'expr'=_unset) -> None:
        """start checking validation"""
        if value is _unset: raise ValueError('value cannot be empty.')
        self.value = value

class Pass(ast.Pass, stmt):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class Break(ast.Break, stmt):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class Continue(ast.Continue, stmt):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class BoolOp(ast.BoolOp, expr):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.op = _unset_init
        self.values = _unset_init

    def _postinit(self, op:'boolop'=_unset, values:'list[expr]'=_unset) -> None:
        """start checking validation"""
        if op is _unset: raise ValueError('op cannot be empty.')
        if values is _unset: values = []
        self.op = op
        self.values = values #type:ignore

class BinOp(ast.BinOp, expr):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.left = _unset_init
        self.op = _unset_init
        self.right = _unset_init

    def _postinit(self, left:'expr'=_unset, op:'operator'=_unset, right:'expr'=_unset) -> None:
        """start checking validation"""
        if left is _unset: raise ValueError('left cannot be empty.')
        if op is _unset: raise ValueError('op cannot be empty.')
        if right is _unset: raise ValueError('right cannot be empty.')
        self.left = left
        self.op = op
        self.right = right

class UnaryOp(ast.UnaryOp, expr):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.op = _unset_init
        self.operand = _unset_init

    def _postinit(self, op:'unaryop'=_unset, operand:'expr'=_unset) -> None:
        """start checking validation"""
        if op is _unset: raise ValueError('op cannot be empty.')
        if operand is _unset: raise ValueError('operand cannot be empty.')
        self.op = op
        self.operand = operand

class Lambda(ast.Lambda, expr):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.args = _unset_init
        self.body = _unset_init

    def _postinit(self, args:'arguments'=_unset, body:'expr'=_unset) -> None:
        """start checking validation"""
        if args is _unset: raise ValueError('args cannot be empty.')
        if body is _unset: raise ValueError('body cannot be empty.')
        self.args = args
        self.body = body

class IfExp(ast.IfExp, expr):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.test = _unset_init
        self.body = _unset_init
        self.orelse = _unset_init

    def _postinit(self, test:'expr'=_unset, body:'expr'=_unset, orelse:'expr'=_unset) -> None:
        """start checking validation"""
        if test is _unset: raise ValueError('test cannot be empty.')
        if body is _unset: raise ValueError('body cannot be empty.')
        if orelse is _unset: raise ValueError('orelse cannot be empty.')
        self.test = test
        self.body = body
        self.orelse = orelse

class Dict(ast.Dict, expr):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.keys = _unset_init
        self.values = _unset_init

    def _postinit(self, keys:'list[expr | None]'=_unset, values:'list[expr]'=_unset) -> None:
        """start checking validation"""
        if keys is _unset: keys = []
        if values is _unset: values = []
        self.keys = keys #type:ignore
        self.values = values #type:ignore

class Set(ast.Set, expr):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.elts = _unset_init

    def _postinit(self, elts:'list[expr]'=_unset) -> None:
        """start checking validation"""
        if elts is _unset: elts = []
        self.elts = elts #type:ignore

class ListComp(ast.ListComp, expr):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.elt = _unset_init
        self.generators = _unset_init

    def _postinit(self, elt:'expr'=_unset, generators:'list[comprehension]'=_unset) -> None:
        """start checking validation"""
        if elt is _unset: raise ValueError('elt cannot be empty.')
        if generators is _unset: generators = []
        self.elt = elt
        self.generators = generators #type:ignore

class SetComp(ast.SetComp, expr):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.elt = _unset_init
        self.generators = _unset_init

    def _postinit(self, elt:'expr'=_unset, generators:'list[comprehension]'=_unset) -> None:
        """start checking validation"""
        if elt is _unset: raise ValueError('elt cannot be empty.')
        if generators is _unset: generators = []
        self.elt = elt
        self.generators = generators #type:ignore

class DictComp(ast.DictComp, expr):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.key = _unset_init
        self.value = _unset_init
        self.generators = _unset_init

    def _postinit(self, key:'expr'=_unset, value:'expr'=_unset, generators:'list[comprehension]'=_unset) -> None:
        """start checking validation"""
        if key is _unset: raise ValueError('key cannot be empty.')
        if value is _unset: raise ValueError('value cannot be empty.')
        if generators is _unset: generators = []
        self.key = key
        self.value = value
        self.generators = generators #type:ignore

class GeneratorExp(ast.GeneratorExp, expr):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.elt = _unset_init
        self.generators = _unset_init

    def _postinit(self, elt:'expr'=_unset, generators:'list[comprehension]'=_unset) -> None:
        """start checking validation"""
        if elt is _unset: raise ValueError('elt cannot be empty.')
        if generators is _unset: generators = []
        self.elt = elt
        self.generators = generators #type:ignore

class Await(ast.Await, expr):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.value = _unset_init

    def _postinit(self, value:'expr'=_unset) -> None:
        """start checking validation"""
        if value is _unset: raise ValueError('value cannot be empty.')
        self.value = value

class Yield(ast.Yield, expr):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.value = _unset_init

    def _postinit(self, value:'expr | None'=_unset) -> None:
        """start checking validation"""
        if value is _unset: value = None
        self.value = value

class YieldFrom(ast.YieldFrom, expr):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.value = _unset_init

    def _postinit(self, value:'expr'=_unset) -> None:
        """start checking validation"""
        if value is _unset: raise ValueError('value cannot be empty.')
        self.value = value

class Compare(ast.Compare, expr):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.left = _unset_init
        self.ops = _unset_init
        self.comparators = _unset_init

    def _postinit(self, left:'expr'=_unset, ops:'list[cmpop]'=_unset, comparators:'list[expr]'=_unset) -> None:
        """start checking validation"""
        if left is _unset: raise ValueError('left cannot be empty.')
        if ops is _unset: ops = []
        if comparators is _unset: comparators = []
        self.left = left
        self.ops = ops #type:ignore
        self.comparators = comparators #type:ignore

class Call(ast.Call, expr):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.func = _unset_init
        self.args = _unset_init
        self.keywords = _unset_init

    def _postinit(self, func:'expr'=_unset, args:'list[expr]'=_unset, keywords:'list[keyword]'=_unset) -> None:
        """start checking validation"""
        if func is _unset: raise ValueError('func cannot be empty.')
        if args is _unset: args = []
        if keywords is _unset: keywords = []
        self.func = func
        self.args = args #type:ignore
        self.keywords = keywords #type:ignore

class Num(ast.Num, expr):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.n = _unset_init

    def _postinit(self, n:'complex'=_unset) -> None:
        """start checking validation"""
        if n is _unset: raise ValueError('n cannot be empty.')
        self.n = n

class Str(ast.Str, expr):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.s = _unset_init

    def _postinit(self, s:'str'=_unset) -> None:
        """start checking validation"""
        if s is _unset: raise ValueError('s cannot be empty.')
        self.s = s

class FormattedValue(ast.FormattedValue, expr):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.value = _unset_init
        self.conversion = _unset_init
        self.format_spec = _unset_init

    def _postinit(self, value:'expr'=_unset, conversion:'int'=_unset, format_spec:'expr | None'=_unset) -> None:
        """start checking validation"""
        if value is _unset: raise ValueError('value cannot be empty.')
        if conversion is _unset: conversion = None
        if format_spec is _unset: format_spec = None
        self.value = value
        self.conversion = conversion
        self.format_spec = format_spec

class JoinedStr(ast.JoinedStr, expr):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.values = _unset_init

    def _postinit(self, values:'list[expr]'=_unset) -> None:
        """start checking validation"""
        if values is _unset: values = []
        self.values = values #type:ignore

class Bytes(ast.Bytes, expr):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.s = _unset_init

    def _postinit(self, s:'bytes'=_unset) -> None:
        """start checking validation"""
        if s is _unset: raise ValueError('s cannot be empty.')
        self.s = s

class NameConstant(ast.NameConstant, expr):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.value = _unset_init

    def _postinit(self, value:'Any'=_unset) -> None:
        """start checking validation"""
        if value is _unset: raise ValueError('value cannot be empty.')
        self.value = value

class Ellipsis(ast.Ellipsis, expr):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class Constant(ast.Constant, expr):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.value = _unset_init

    def _postinit(self, value:'Any'=_unset) -> None:
        """start checking validation"""
        if value is _unset: raise ValueError('value cannot be empty.')
        self.value = value

class Attribute(ast.Attribute, expr):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.value = _unset_init
        self.attr = _unset_init
        self.ctx = _unset_init

    def _postinit(self, value:'expr'=_unset, attr:'str'=_unset, ctx:'expr_context'=_unset) -> None:
        """start checking validation"""
        if value is _unset: raise ValueError('value cannot be empty.')
        if attr is _unset: raise ValueError('attr cannot be empty.')
        if ctx is _unset: raise ValueError('ctx cannot be empty.')
        self.value = value
        self.attr = attr
        self.ctx = ctx

class Subscript(ast.Subscript, expr):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.value = _unset_init
        self.slice = _unset_init
        self.ctx = _unset_init

    def _postinit(self, value:'expr'=_unset, slice:'slice'=_unset, ctx:'expr_context'=_unset) -> None:
        """start checking validation"""
        if value is _unset: raise ValueError('value cannot be empty.')
        if slice is _unset: raise ValueError('slice cannot be empty.')
        if ctx is _unset: raise ValueError('ctx cannot be empty.')
        self.value = value
        self.slice = slice
        self.ctx = ctx

class Starred(ast.Starred, expr):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.value = _unset_init
        self.ctx = _unset_init

    def _postinit(self, value:'expr'=_unset, ctx:'expr_context'=_unset) -> None:
        """start checking validation"""
        if value is _unset: raise ValueError('value cannot be empty.')
        if ctx is _unset: raise ValueError('ctx cannot be empty.')
        self.value = value
        self.ctx = ctx

class Name(ast.Name, expr):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.id = _unset_init
        self.ctx = _unset_init

    def _postinit(self, id:'str'=_unset, ctx:'expr_context'=_unset) -> None:
        """start checking validation"""
        if id is _unset: raise ValueError('id cannot be empty.')
        if ctx is _unset: raise ValueError('ctx cannot be empty.')
        self.id = id
        self.ctx = ctx

class List(ast.List, expr):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.elts = _unset_init
        self.ctx = _unset_init

    def _postinit(self, elts:'list[expr]'=_unset, ctx:'expr_context'=_unset) -> None:
        """start checking validation"""
        if elts is _unset: elts = []
        if ctx is _unset: raise ValueError('ctx cannot be empty.')
        self.elts = elts #type:ignore
        self.ctx = ctx

class Tuple(ast.Tuple, expr):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.elts = _unset_init
        self.ctx = _unset_init

    def _postinit(self, elts:'list[expr]'=_unset, ctx:'expr_context'=_unset) -> None:
        """start checking validation"""
        if elts is _unset: elts = []
        if ctx is _unset: raise ValueError('ctx cannot be empty.')
        self.elts = elts #type:ignore
        self.ctx = ctx

class Load(ast.Load, expr_context):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class Store(ast.Store, expr_context):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class Del(ast.Del, expr_context):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class AugLoad(ast.AugLoad, expr_context):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class AugStore(ast.AugStore, expr_context):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class Param(ast.Param, expr_context):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class Slice(ast.Slice, slice):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.lower = _unset_init
        self.upper = _unset_init
        self.step = _unset_init

    def _postinit(self, lower:'expr | None'=_unset, upper:'expr | None'=_unset, step:'expr | None'=_unset) -> None:
        """start checking validation"""
        if lower is _unset: lower = None
        if upper is _unset: upper = None
        if step is _unset: step = None
        self.lower = lower
        self.upper = upper
        self.step = step

class ExtSlice(ast.ExtSlice, slice):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.dims = _unset_init

    def _postinit(self, dims:'list[slice]'=_unset) -> None:
        """start checking validation"""
        if dims is _unset: dims = []
        self.dims = dims #type:ignore

class Index(ast.Index, slice):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.value = _unset_init

    def _postinit(self, value:'expr'=_unset) -> None:
        """start checking validation"""
        if value is _unset: raise ValueError('value cannot be empty.')
        self.value = value

class And(ast.And, boolop):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class Or(ast.Or, boolop):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class Add(ast.Add, operator):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class Sub(ast.Sub, operator):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class Mult(ast.Mult, operator):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class MatMult(ast.MatMult, operator):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class Div(ast.Div, operator):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class Mod(ast.Mod, operator):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class Pow(ast.Pow, operator):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class LShift(ast.LShift, operator):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class RShift(ast.RShift, operator):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class BitOr(ast.BitOr, operator):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class BitXor(ast.BitXor, operator):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class BitAnd(ast.BitAnd, operator):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class FloorDiv(ast.FloorDiv, operator):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class Invert(ast.Invert, unaryop):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class Not(ast.Not, unaryop):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class UAdd(ast.UAdd, unaryop):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class USub(ast.USub, unaryop):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class Eq(ast.Eq, cmpop):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class NotEq(ast.NotEq, cmpop):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class Lt(ast.Lt, cmpop):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class LtE(ast.LtE, cmpop):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class Gt(ast.Gt, cmpop):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class GtE(ast.GtE, cmpop):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class Is(ast.Is, cmpop):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class IsNot(ast.IsNot, cmpop):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class In(ast.In, cmpop):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class NotIn(ast.NotIn, cmpop):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)

class comprehension(ast.comprehension, AST):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.target = _unset_init
        self.iter = _unset_init
        self.ifs = _unset_init
        self.is_async = _unset_init

    def _postinit(self, target:'expr'=_unset, iter:'expr'=_unset, ifs:'list[expr]'=_unset, is_async:'int'=_unset) -> None:
        """start checking validation"""
        if target is _unset: raise ValueError('target cannot be empty.')
        if iter is _unset: raise ValueError('iter cannot be empty.')
        if ifs is _unset: ifs = []
        if is_async is _unset: raise ValueError('is_async cannot be empty.')
        self.target = target
        self.iter = iter
        self.ifs = ifs #type:ignore
        self.is_async = is_async

class ExceptHandler(ast.ExceptHandler, excepthandler):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.type = _unset_init
        self.name = _unset_init
        self.body = _unset_init

    def _postinit(self, type:'expr | None'=_unset, name:'str | None'=_unset, body:'list[stmt]'=_unset) -> None:
        """start checking validation"""
        if type is _unset: type = None
        if name is _unset: name = None
        if body is _unset: body = []
        self.type = type
        self.name = name
        self.body = body #type:ignore

class arguments(ast.arguments, AST):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.args = _unset_init
        self.vararg = _unset_init
        self.kwonlyargs = _unset_init
        self.kw_defaults = _unset_init
        self.kwarg = _unset_init
        self.defaults = _unset_init

    def _postinit(self, args:'list[arg]'=_unset, vararg:'arg | None'=_unset, kwonlyargs:'list[arg]'=_unset, kw_defaults:'list[expr | None]'=_unset, kwarg:'arg | None'=_unset, defaults:'list[expr]'=_unset) -> None:
        """start checking validation"""
        if args is _unset: args = []
        if vararg is _unset: vararg = None
        if kwonlyargs is _unset: kwonlyargs = []
        if kw_defaults is _unset: kw_defaults = []
        if kwarg is _unset: kwarg = None
        if defaults is _unset: defaults = []
        self.args = args #type:ignore
        self.vararg = vararg
        self.kwonlyargs = kwonlyargs #type:ignore
        self.kw_defaults = kw_defaults #type:ignore
        self.kwarg = kwarg
        self.defaults = defaults #type:ignore

class arg(ast.arg, AST):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.arg = _unset_init
        self.annotation = _unset_init

    def _postinit(self, arg:'str'=_unset, annotation:'expr | None'=_unset) -> None:
        """start checking validation"""
        if arg is _unset: raise ValueError('arg cannot be empty.')
        if annotation is _unset: annotation = None
        self.arg = arg
        self.annotation = annotation

class keyword(ast.keyword, AST):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.arg = _unset_init
        self.value = _unset_init

    def _postinit(self, arg:'str | None'=_unset, value:'expr'=_unset) -> None:
        """start checking validation"""
        if arg is _unset: arg = None
        if value is _unset: raise ValueError('value cannot be empty.')
        self.arg = arg
        self.value = value

class alias(ast.alias, AST):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.name = _unset_init
        self.asname = _unset_init

    def _postinit(self, name:'str'=_unset, asname:'str | None'=_unset) -> None:
        """start checking validation"""
        if name is _unset: raise ValueError('name cannot be empty.')
        if asname is _unset: asname = None
        self.name = name
        self.asname = asname

class withitem(ast.withitem, AST):

    def __init__(self, lineno: int=-1, col_offset: int=0, parent:Optional['AST']=None, *, end_lineno: Optional[int]=None, end_col_offset: Optional[int]=None) -> None:
        super().__init__(lineno, col_offset, parent, end_lineno=end_lineno, end_col_offset=end_col_offset)
        # all fields defaults to _unset_init
        self.context_expr = _unset_init
        self.optional_vars = _unset_init

    def _postinit(self, context_expr:'expr'=_unset, optional_vars:'expr | None'=_unset) -> None:
        """start checking validation"""
        if context_expr is _unset: raise ValueError('context_expr cannot be empty.')
        if optional_vars is _unset: optional_vars = None
        self.context_expr = context_expr
        self.optional_vars = optional_vars

# Any
# arg | None
# arguments
# boolop
# bytes
# complex
# expr
# expr | None
# expr_context
# int
# list[ExceptHandler]
# list[alias]
# list[arg]
# list[cmpop]
# list[comprehension]
# list[expr | None]
# list[expr]
# list[keyword]
# list[slice]
# list[stmt]
# list[str]
# list[withitem]
# operator
# slice
# str
# str | None
# unaryop
