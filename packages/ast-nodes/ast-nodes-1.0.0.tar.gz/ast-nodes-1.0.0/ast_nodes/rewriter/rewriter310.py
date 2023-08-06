"""AST rewriter for python 3.10"""
# this file is auto-generated, please don't edit it directly.
import ast, builtins
from typing import Any, Generic, TypeVar, Optional, Union, Protocol, Type, TYPE_CHECKING, overload
if TYPE_CHECKING:
    from typing import Literal
from ..nodes import nodes310 as nodes

class NodesT(Protocol):
    Module: Type[nodes.Module]
    Interactive: Type[nodes.Interactive]
    Expression: Type[nodes.Expression]
    FunctionType: Type[nodes.FunctionType]
    FunctionDef: Type[nodes.FunctionDef]
    AsyncFunctionDef: Type[nodes.AsyncFunctionDef]
    ClassDef: Type[nodes.ClassDef]
    Return: Type[nodes.Return]
    Delete: Type[nodes.Delete]
    Assign: Type[nodes.Assign]
    AugAssign: Type[nodes.AugAssign]
    AnnAssign: Type[nodes.AnnAssign]
    For: Type[nodes.For]
    AsyncFor: Type[nodes.AsyncFor]
    While: Type[nodes.While]
    If: Type[nodes.If]
    With: Type[nodes.With]
    AsyncWith: Type[nodes.AsyncWith]
    Match: Type[nodes.Match]
    Raise: Type[nodes.Raise]
    Try: Type[nodes.Try]
    Assert: Type[nodes.Assert]
    Import: Type[nodes.Import]
    ImportFrom: Type[nodes.ImportFrom]
    Global: Type[nodes.Global]
    Nonlocal: Type[nodes.Nonlocal]
    Expr: Type[nodes.Expr]
    Pass: Type[nodes.Pass]
    Break: Type[nodes.Break]
    Continue: Type[nodes.Continue]
    BoolOp: Type[nodes.BoolOp]
    NamedExpr: Type[nodes.NamedExpr]
    BinOp: Type[nodes.BinOp]
    UnaryOp: Type[nodes.UnaryOp]
    Lambda: Type[nodes.Lambda]
    IfExp: Type[nodes.IfExp]
    Dict: Type[nodes.Dict]
    Set: Type[nodes.Set]
    ListComp: Type[nodes.ListComp]
    SetComp: Type[nodes.SetComp]
    DictComp: Type[nodes.DictComp]
    GeneratorExp: Type[nodes.GeneratorExp]
    Await: Type[nodes.Await]
    Yield: Type[nodes.Yield]
    YieldFrom: Type[nodes.YieldFrom]
    Compare: Type[nodes.Compare]
    Call: Type[nodes.Call]
    FormattedValue: Type[nodes.FormattedValue]
    JoinedStr: Type[nodes.JoinedStr]
    Constant: Type[nodes.Constant]
    Attribute: Type[nodes.Attribute]
    Subscript: Type[nodes.Subscript]
    Starred: Type[nodes.Starred]
    Name: Type[nodes.Name]
    List: Type[nodes.List]
    Tuple: Type[nodes.Tuple]
    Slice: Type[nodes.Slice]
    Load: Type[nodes.Load]
    Store: Type[nodes.Store]
    Del: Type[nodes.Del]
    And: Type[nodes.And]
    Or: Type[nodes.Or]
    Add: Type[nodes.Add]
    Sub: Type[nodes.Sub]
    Mult: Type[nodes.Mult]
    MatMult: Type[nodes.MatMult]
    Div: Type[nodes.Div]
    Mod: Type[nodes.Mod]
    Pow: Type[nodes.Pow]
    LShift: Type[nodes.LShift]
    RShift: Type[nodes.RShift]
    BitOr: Type[nodes.BitOr]
    BitXor: Type[nodes.BitXor]
    BitAnd: Type[nodes.BitAnd]
    FloorDiv: Type[nodes.FloorDiv]
    Invert: Type[nodes.Invert]
    Not: Type[nodes.Not]
    UAdd: Type[nodes.UAdd]
    USub: Type[nodes.USub]
    Eq: Type[nodes.Eq]
    NotEq: Type[nodes.NotEq]
    Lt: Type[nodes.Lt]
    LtE: Type[nodes.LtE]
    Gt: Type[nodes.Gt]
    GtE: Type[nodes.GtE]
    Is: Type[nodes.Is]
    IsNot: Type[nodes.IsNot]
    In: Type[nodes.In]
    NotIn: Type[nodes.NotIn]
    comprehension: Type[nodes.comprehension]
    ExceptHandler: Type[nodes.ExceptHandler]
    arguments: Type[nodes.arguments]
    arg: Type[nodes.arg]
    keyword: Type[nodes.keyword]
    alias: Type[nodes.alias]
    withitem: Type[nodes.withitem]
    match_case: Type[nodes.match_case]
    MatchValue: Type[nodes.MatchValue]
    MatchSingleton: Type[nodes.MatchSingleton]
    MatchSequence: Type[nodes.MatchSequence]
    MatchMapping: Type[nodes.MatchMapping]
    MatchClass: Type[nodes.MatchClass]
    MatchStar: Type[nodes.MatchStar]
    MatchAs: Type[nodes.MatchAs]
    MatchOr: Type[nodes.MatchOr]
    TypeIgnore: Type[nodes.TypeIgnore]

class Nodes(NodesT):
    """Class that aliases all concrete node classes as found in nodes310.py file."""
    Module = nodes.Module
    Interactive = nodes.Interactive
    Expression = nodes.Expression
    FunctionType = nodes.FunctionType
    FunctionDef = nodes.FunctionDef
    AsyncFunctionDef = nodes.AsyncFunctionDef
    ClassDef = nodes.ClassDef
    Return = nodes.Return
    Delete = nodes.Delete
    Assign = nodes.Assign
    AugAssign = nodes.AugAssign
    AnnAssign = nodes.AnnAssign
    For = nodes.For
    AsyncFor = nodes.AsyncFor
    While = nodes.While
    If = nodes.If
    With = nodes.With
    AsyncWith = nodes.AsyncWith
    Match = nodes.Match
    Raise = nodes.Raise
    Try = nodes.Try
    Assert = nodes.Assert
    Import = nodes.Import
    ImportFrom = nodes.ImportFrom
    Global = nodes.Global
    Nonlocal = nodes.Nonlocal
    Expr = nodes.Expr
    Pass = nodes.Pass
    Break = nodes.Break
    Continue = nodes.Continue
    BoolOp = nodes.BoolOp
    NamedExpr = nodes.NamedExpr
    BinOp = nodes.BinOp
    UnaryOp = nodes.UnaryOp
    Lambda = nodes.Lambda
    IfExp = nodes.IfExp
    Dict = nodes.Dict
    Set = nodes.Set
    ListComp = nodes.ListComp
    SetComp = nodes.SetComp
    DictComp = nodes.DictComp
    GeneratorExp = nodes.GeneratorExp
    Await = nodes.Await
    Yield = nodes.Yield
    YieldFrom = nodes.YieldFrom
    Compare = nodes.Compare
    Call = nodes.Call
    FormattedValue = nodes.FormattedValue
    JoinedStr = nodes.JoinedStr
    Constant = nodes.Constant
    Attribute = nodes.Attribute
    Subscript = nodes.Subscript
    Starred = nodes.Starred
    Name = nodes.Name
    List = nodes.List
    Tuple = nodes.Tuple
    Slice = nodes.Slice
    Load = nodes.Load
    Store = nodes.Store
    Del = nodes.Del
    And = nodes.And
    Or = nodes.Or
    Add = nodes.Add
    Sub = nodes.Sub
    Mult = nodes.Mult
    MatMult = nodes.MatMult
    Div = nodes.Div
    Mod = nodes.Mod
    Pow = nodes.Pow
    LShift = nodes.LShift
    RShift = nodes.RShift
    BitOr = nodes.BitOr
    BitXor = nodes.BitXor
    BitAnd = nodes.BitAnd
    FloorDiv = nodes.FloorDiv
    Invert = nodes.Invert
    Not = nodes.Not
    UAdd = nodes.UAdd
    USub = nodes.USub
    Eq = nodes.Eq
    NotEq = nodes.NotEq
    Lt = nodes.Lt
    LtE = nodes.LtE
    Gt = nodes.Gt
    GtE = nodes.GtE
    Is = nodes.Is
    IsNot = nodes.IsNot
    In = nodes.In
    NotIn = nodes.NotIn
    comprehension = nodes.comprehension
    ExceptHandler = nodes.ExceptHandler
    arguments = nodes.arguments
    arg = nodes.arg
    keyword = nodes.keyword
    alias = nodes.alias
    withitem = nodes.withitem
    match_case = nodes.match_case
    MatchValue = nodes.MatchValue
    MatchSingleton = nodes.MatchSingleton
    MatchSequence = nodes.MatchSequence
    MatchMapping = nodes.MatchMapping
    MatchClass = nodes.MatchClass
    MatchStar = nodes.MatchStar
    MatchAs = nodes.MatchAs
    MatchOr = nodes.MatchOr
    TypeIgnore = nodes.TypeIgnore

T_i = TypeVar('T_i')
T_o = TypeVar('T_o')
T_p = TypeVar('T_p')

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


    if TYPE_CHECKING:
        @overload
        def visit(self, node:ast.Module, parent:Optional[nodes.AST]) -> nodes.Module:...
        @overload
        def visit(self, node:ast.Interactive, parent:Optional[nodes.AST]) -> nodes.Interactive:...
        @overload
        def visit(self, node:ast.Expression, parent:Optional[nodes.AST]) -> nodes.Expression:...
        @overload
        def visit(self, node:ast.FunctionType, parent:Optional[nodes.AST]) -> nodes.FunctionType:...
        @overload
        def visit(self, node:ast.FunctionDef, parent:Optional[nodes.AST]) -> nodes.FunctionDef:...
        @overload
        def visit(self, node:ast.AsyncFunctionDef, parent:Optional[nodes.AST]) -> nodes.AsyncFunctionDef:...
        @overload
        def visit(self, node:ast.ClassDef, parent:Optional[nodes.AST]) -> nodes.ClassDef:...
        @overload
        def visit(self, node:ast.Return, parent:Optional[nodes.AST]) -> nodes.Return:...
        @overload
        def visit(self, node:ast.Delete, parent:Optional[nodes.AST]) -> nodes.Delete:...
        @overload
        def visit(self, node:ast.Assign, parent:Optional[nodes.AST]) -> nodes.Assign:...
        @overload
        def visit(self, node:ast.AugAssign, parent:Optional[nodes.AST]) -> nodes.AugAssign:...
        @overload
        def visit(self, node:ast.AnnAssign, parent:Optional[nodes.AST]) -> nodes.AnnAssign:...
        @overload
        def visit(self, node:ast.For, parent:Optional[nodes.AST]) -> nodes.For:...
        @overload
        def visit(self, node:ast.AsyncFor, parent:Optional[nodes.AST]) -> nodes.AsyncFor:...
        @overload
        def visit(self, node:ast.While, parent:Optional[nodes.AST]) -> nodes.While:...
        @overload
        def visit(self, node:ast.If, parent:Optional[nodes.AST]) -> nodes.If:...
        @overload
        def visit(self, node:ast.With, parent:Optional[nodes.AST]) -> nodes.With:...
        @overload
        def visit(self, node:ast.AsyncWith, parent:Optional[nodes.AST]) -> nodes.AsyncWith:...
        @overload
        def visit(self, node:ast.Match, parent:Optional[nodes.AST]) -> nodes.Match:...
        @overload
        def visit(self, node:ast.Raise, parent:Optional[nodes.AST]) -> nodes.Raise:...
        @overload
        def visit(self, node:ast.Try, parent:Optional[nodes.AST]) -> nodes.Try:...
        @overload
        def visit(self, node:ast.Assert, parent:Optional[nodes.AST]) -> nodes.Assert:...
        @overload
        def visit(self, node:ast.Import, parent:Optional[nodes.AST]) -> nodes.Import:...
        @overload
        def visit(self, node:ast.ImportFrom, parent:Optional[nodes.AST]) -> nodes.ImportFrom:...
        @overload
        def visit(self, node:ast.Global, parent:Optional[nodes.AST]) -> nodes.Global:...
        @overload
        def visit(self, node:ast.Nonlocal, parent:Optional[nodes.AST]) -> nodes.Nonlocal:...
        @overload
        def visit(self, node:ast.Expr, parent:Optional[nodes.AST]) -> nodes.Expr:...
        @overload
        def visit(self, node:ast.Pass, parent:Optional[nodes.AST]) -> nodes.Pass:...
        @overload
        def visit(self, node:ast.Break, parent:Optional[nodes.AST]) -> nodes.Break:...
        @overload
        def visit(self, node:ast.Continue, parent:Optional[nodes.AST]) -> nodes.Continue:...
        @overload
        def visit(self, node:ast.BoolOp, parent:Optional[nodes.AST]) -> nodes.BoolOp:...
        @overload
        def visit(self, node:ast.NamedExpr, parent:Optional[nodes.AST]) -> nodes.NamedExpr:...
        @overload
        def visit(self, node:ast.BinOp, parent:Optional[nodes.AST]) -> nodes.BinOp:...
        @overload
        def visit(self, node:ast.UnaryOp, parent:Optional[nodes.AST]) -> nodes.UnaryOp:...
        @overload
        def visit(self, node:ast.Lambda, parent:Optional[nodes.AST]) -> nodes.Lambda:...
        @overload
        def visit(self, node:ast.IfExp, parent:Optional[nodes.AST]) -> nodes.IfExp:...
        @overload
        def visit(self, node:ast.Dict, parent:Optional[nodes.AST]) -> nodes.Dict:...
        @overload
        def visit(self, node:ast.Set, parent:Optional[nodes.AST]) -> nodes.Set:...
        @overload
        def visit(self, node:ast.ListComp, parent:Optional[nodes.AST]) -> nodes.ListComp:...
        @overload
        def visit(self, node:ast.SetComp, parent:Optional[nodes.AST]) -> nodes.SetComp:...
        @overload
        def visit(self, node:ast.DictComp, parent:Optional[nodes.AST]) -> nodes.DictComp:...
        @overload
        def visit(self, node:ast.GeneratorExp, parent:Optional[nodes.AST]) -> nodes.GeneratorExp:...
        @overload
        def visit(self, node:ast.Await, parent:Optional[nodes.AST]) -> nodes.Await:...
        @overload
        def visit(self, node:ast.Yield, parent:Optional[nodes.AST]) -> nodes.Yield:...
        @overload
        def visit(self, node:ast.YieldFrom, parent:Optional[nodes.AST]) -> nodes.YieldFrom:...
        @overload
        def visit(self, node:ast.Compare, parent:Optional[nodes.AST]) -> nodes.Compare:...
        @overload
        def visit(self, node:ast.Call, parent:Optional[nodes.AST]) -> nodes.Call:...
        @overload
        def visit(self, node:ast.FormattedValue, parent:Optional[nodes.AST]) -> nodes.FormattedValue:...
        @overload
        def visit(self, node:ast.JoinedStr, parent:Optional[nodes.AST]) -> nodes.JoinedStr:...
        @overload
        def visit(self, node:ast.Constant, parent:Optional[nodes.AST]) -> nodes.Constant:...
        @overload
        def visit(self, node:ast.Attribute, parent:Optional[nodes.AST]) -> nodes.Attribute:...
        @overload
        def visit(self, node:ast.Subscript, parent:Optional[nodes.AST]) -> nodes.Subscript:...
        @overload
        def visit(self, node:ast.Starred, parent:Optional[nodes.AST]) -> nodes.Starred:...
        @overload
        def visit(self, node:ast.Name, parent:Optional[nodes.AST]) -> nodes.Name:...
        @overload
        def visit(self, node:ast.List, parent:Optional[nodes.AST]) -> nodes.List:...
        @overload
        def visit(self, node:ast.Tuple, parent:Optional[nodes.AST]) -> nodes.Tuple:...
        @overload
        def visit(self, node:ast.Slice, parent:Optional[nodes.AST]) -> nodes.Slice:...
        @overload
        def visit(self, node:ast.Load, parent:Optional[nodes.AST]) -> nodes.Load:...
        @overload
        def visit(self, node:ast.Store, parent:Optional[nodes.AST]) -> nodes.Store:...
        @overload
        def visit(self, node:ast.Del, parent:Optional[nodes.AST]) -> nodes.Del:...
        @overload
        def visit(self, node:ast.And, parent:Optional[nodes.AST]) -> nodes.And:...
        @overload
        def visit(self, node:ast.Or, parent:Optional[nodes.AST]) -> nodes.Or:...
        @overload
        def visit(self, node:ast.Add, parent:Optional[nodes.AST]) -> nodes.Add:...
        @overload
        def visit(self, node:ast.Sub, parent:Optional[nodes.AST]) -> nodes.Sub:...
        @overload
        def visit(self, node:ast.Mult, parent:Optional[nodes.AST]) -> nodes.Mult:...
        @overload
        def visit(self, node:ast.MatMult, parent:Optional[nodes.AST]) -> nodes.MatMult:...
        @overload
        def visit(self, node:ast.Div, parent:Optional[nodes.AST]) -> nodes.Div:...
        @overload
        def visit(self, node:ast.Mod, parent:Optional[nodes.AST]) -> nodes.Mod:...
        @overload
        def visit(self, node:ast.Pow, parent:Optional[nodes.AST]) -> nodes.Pow:...
        @overload
        def visit(self, node:ast.LShift, parent:Optional[nodes.AST]) -> nodes.LShift:...
        @overload
        def visit(self, node:ast.RShift, parent:Optional[nodes.AST]) -> nodes.RShift:...
        @overload
        def visit(self, node:ast.BitOr, parent:Optional[nodes.AST]) -> nodes.BitOr:...
        @overload
        def visit(self, node:ast.BitXor, parent:Optional[nodes.AST]) -> nodes.BitXor:...
        @overload
        def visit(self, node:ast.BitAnd, parent:Optional[nodes.AST]) -> nodes.BitAnd:...
        @overload
        def visit(self, node:ast.FloorDiv, parent:Optional[nodes.AST]) -> nodes.FloorDiv:...
        @overload
        def visit(self, node:ast.Invert, parent:Optional[nodes.AST]) -> nodes.Invert:...
        @overload
        def visit(self, node:ast.Not, parent:Optional[nodes.AST]) -> nodes.Not:...
        @overload
        def visit(self, node:ast.UAdd, parent:Optional[nodes.AST]) -> nodes.UAdd:...
        @overload
        def visit(self, node:ast.USub, parent:Optional[nodes.AST]) -> nodes.USub:...
        @overload
        def visit(self, node:ast.Eq, parent:Optional[nodes.AST]) -> nodes.Eq:...
        @overload
        def visit(self, node:ast.NotEq, parent:Optional[nodes.AST]) -> nodes.NotEq:...
        @overload
        def visit(self, node:ast.Lt, parent:Optional[nodes.AST]) -> nodes.Lt:...
        @overload
        def visit(self, node:ast.LtE, parent:Optional[nodes.AST]) -> nodes.LtE:...
        @overload
        def visit(self, node:ast.Gt, parent:Optional[nodes.AST]) -> nodes.Gt:...
        @overload
        def visit(self, node:ast.GtE, parent:Optional[nodes.AST]) -> nodes.GtE:...
        @overload
        def visit(self, node:ast.Is, parent:Optional[nodes.AST]) -> nodes.Is:...
        @overload
        def visit(self, node:ast.IsNot, parent:Optional[nodes.AST]) -> nodes.IsNot:...
        @overload
        def visit(self, node:ast.In, parent:Optional[nodes.AST]) -> nodes.In:...
        @overload
        def visit(self, node:ast.NotIn, parent:Optional[nodes.AST]) -> nodes.NotIn:...
        @overload
        def visit(self, node:ast.comprehension, parent:Optional[nodes.AST]) -> nodes.comprehension:...
        @overload
        def visit(self, node:ast.ExceptHandler, parent:Optional[nodes.AST]) -> nodes.ExceptHandler:...
        @overload
        def visit(self, node:ast.arguments, parent:Optional[nodes.AST]) -> nodes.arguments:...
        @overload
        def visit(self, node:ast.arg, parent:Optional[nodes.AST]) -> nodes.arg:...
        @overload
        def visit(self, node:ast.keyword, parent:Optional[nodes.AST]) -> nodes.keyword:...
        @overload
        def visit(self, node:ast.alias, parent:Optional[nodes.AST]) -> nodes.alias:...
        @overload
        def visit(self, node:ast.withitem, parent:Optional[nodes.AST]) -> nodes.withitem:...
        @overload
        def visit(self, node:ast.match_case, parent:Optional[nodes.AST]) -> nodes.match_case:...
        @overload
        def visit(self, node:ast.MatchValue, parent:Optional[nodes.AST]) -> nodes.MatchValue:...
        @overload
        def visit(self, node:ast.MatchSingleton, parent:Optional[nodes.AST]) -> nodes.MatchSingleton:...
        @overload
        def visit(self, node:ast.MatchSequence, parent:Optional[nodes.AST]) -> nodes.MatchSequence:...
        @overload
        def visit(self, node:ast.MatchMapping, parent:Optional[nodes.AST]) -> nodes.MatchMapping:...
        @overload
        def visit(self, node:ast.MatchClass, parent:Optional[nodes.AST]) -> nodes.MatchClass:...
        @overload
        def visit(self, node:ast.MatchStar, parent:Optional[nodes.AST]) -> nodes.MatchStar:...
        @overload
        def visit(self, node:ast.MatchAs, parent:Optional[nodes.AST]) -> nodes.MatchAs:...
        @overload
        def visit(self, node:ast.MatchOr, parent:Optional[nodes.AST]) -> nodes.MatchOr:...
        @overload
        def visit(self, node:ast.TypeIgnore, parent:Optional[nodes.AST]) -> nodes.TypeIgnore:...
        @overload
        def visit(self, node:ast.mod, parent:Optional[nodes.AST]) -> nodes.mod:...
        @overload
        def visit(self, node:ast.type_ignore, parent:Optional[nodes.AST]) -> nodes.type_ignore:...
        @overload
        def visit(self, node:ast.stmt, parent:Optional[nodes.AST]) -> nodes.stmt:...
        @overload
        def visit(self, node:ast.expr, parent:Optional[nodes.AST]) -> nodes.expr:...
        @overload
        def visit(self, node:ast.expr_context, parent:Optional[nodes.AST]) -> nodes.expr_context:...
        @overload
        def visit(self, node:ast.boolop, parent:Optional[nodes.AST]) -> nodes.boolop:...
        @overload
        def visit(self, node:ast.operator, parent:Optional[nodes.AST]) -> nodes.operator:...
        @overload
        def visit(self, node:ast.unaryop, parent:Optional[nodes.AST]) -> nodes.unaryop:...
        @overload
        def visit(self, node:ast.cmpop, parent:Optional[nodes.AST]) -> nodes.cmpop:...
        @overload
        def visit(self, node:ast.excepthandler, parent:Optional[nodes.AST]) -> nodes.excepthandler:...
        @overload
        def visit(self, node:ast.pattern, parent:Optional[nodes.AST]) -> nodes.pattern:...
        @overload
        def visit(self, node:str, parent:Optional[nodes.AST]) -> str:...
        @overload
        def visit(self, node:bool, parent:Optional[nodes.AST]) -> bool:...
        @overload
        def visit(self, node:int, parent:Optional[nodes.AST]) -> int:...
        @overload
        def visit(self, node:Any, parent:Optional[nodes.AST]) -> Any:...
        def visit(self, node:_InputT, parent:Optional[_ParentT]) -> _OutputT:...

    def visit_Module(self, node:ast.Module, parent:nodes.AST) -> nodes.Module:
        newnode = self.nodes.Module(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        body = [self.visit(n, newnode) for n in node.body]
        type_ignores = [self.visit(n, newnode) for n in node.type_ignores]

        newnode._postinit(
            body = body,
            type_ignores = type_ignores,
        )

        return newnode

    def visit_Interactive(self, node:ast.Interactive, parent:nodes.AST) -> nodes.Interactive:
        newnode = self.nodes.Interactive(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        body = [self.visit(n, newnode) for n in node.body]

        newnode._postinit(
            body = body,
        )

        return newnode

    def visit_Expression(self, node:ast.Expression, parent:nodes.AST) -> nodes.Expression:
        newnode = self.nodes.Expression(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        body = self.visit(node.body, newnode)

        newnode._postinit(
            body = body,
        )

        return newnode

    def visit_FunctionType(self, node:ast.FunctionType, parent:nodes.AST) -> nodes.FunctionType:
        newnode = self.nodes.FunctionType(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        argtypes = [self.visit(n, newnode) for n in node.argtypes]
        returns = self.visit(node.returns, newnode)

        newnode._postinit(
            argtypes = argtypes,
            returns = returns,
        )

        return newnode

    def visit_FunctionDef(self, node:ast.FunctionDef, parent:nodes.AST) -> nodes.FunctionDef:
        newnode = self.nodes.FunctionDef(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        name = self.visit(node.name, newnode)
        args = self.visit(node.args, newnode)
        body = [self.visit(n, newnode) for n in node.body]
        decorator_list = [self.visit(n, newnode) for n in node.decorator_list]
        returns = self.visit(node.returns, newnode)
        type_comment = self.visit(node.type_comment, newnode)

        newnode._postinit(
            name = name,
            args = args,
            body = body,
            decorator_list = decorator_list,
            returns = returns,
            type_comment = type_comment,
        )

        return newnode

    def visit_AsyncFunctionDef(self, node:ast.AsyncFunctionDef, parent:nodes.AST) -> nodes.AsyncFunctionDef:
        newnode = self.nodes.AsyncFunctionDef(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        name = self.visit(node.name, newnode)
        args = self.visit(node.args, newnode)
        body = [self.visit(n, newnode) for n in node.body]
        decorator_list = [self.visit(n, newnode) for n in node.decorator_list]
        returns = self.visit(node.returns, newnode)
        type_comment = self.visit(node.type_comment, newnode)

        newnode._postinit(
            name = name,
            args = args,
            body = body,
            decorator_list = decorator_list,
            returns = returns,
            type_comment = type_comment,
        )

        return newnode

    def visit_ClassDef(self, node:ast.ClassDef, parent:nodes.AST) -> nodes.ClassDef:
        newnode = self.nodes.ClassDef(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        name = self.visit(node.name, newnode)
        bases = [self.visit(n, newnode) for n in node.bases]
        keywords = [self.visit(n, newnode) for n in node.keywords]
        body = [self.visit(n, newnode) for n in node.body]
        decorator_list = [self.visit(n, newnode) for n in node.decorator_list]

        newnode._postinit(
            name = name,
            bases = bases,
            keywords = keywords,
            body = body,
            decorator_list = decorator_list,
        )

        return newnode

    def visit_Return(self, node:ast.Return, parent:nodes.AST) -> nodes.Return:
        newnode = self.nodes.Return(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        value = self.visit(node.value, newnode)

        newnode._postinit(
            value = value,
        )

        return newnode

    def visit_Delete(self, node:ast.Delete, parent:nodes.AST) -> nodes.Delete:
        newnode = self.nodes.Delete(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        targets = [self.visit(n, newnode) for n in node.targets]

        newnode._postinit(
            targets = targets,
        )

        return newnode

    def visit_Assign(self, node:ast.Assign, parent:nodes.AST) -> nodes.Assign:
        newnode = self.nodes.Assign(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        targets = [self.visit(n, newnode) for n in node.targets]
        value = self.visit(node.value, newnode)
        type_comment = self.visit(node.type_comment, newnode)

        newnode._postinit(
            targets = targets,
            value = value,
            type_comment = type_comment,
        )

        return newnode

    def visit_AugAssign(self, node:ast.AugAssign, parent:nodes.AST) -> nodes.AugAssign:
        newnode = self.nodes.AugAssign(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        target = self.visit(node.target, newnode)
        op = self.visit(node.op, newnode)
        value = self.visit(node.value, newnode)

        newnode._postinit(
            target = target,
            op = op,
            value = value,
        )

        return newnode

    def visit_AnnAssign(self, node:ast.AnnAssign, parent:nodes.AST) -> nodes.AnnAssign:
        newnode = self.nodes.AnnAssign(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        target = self.visit(node.target, newnode)
        annotation = self.visit(node.annotation, newnode)
        value = self.visit(node.value, newnode)
        simple = self.visit(node.simple, newnode)

        newnode._postinit(
            target = target,
            annotation = annotation,
            value = value,
            simple = simple,
        )

        return newnode

    def visit_For(self, node:ast.For, parent:nodes.AST) -> nodes.For:
        newnode = self.nodes.For(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        target = self.visit(node.target, newnode)
        iter = self.visit(node.iter, newnode)
        body = [self.visit(n, newnode) for n in node.body]
        orelse = [self.visit(n, newnode) for n in node.orelse]
        type_comment = self.visit(node.type_comment, newnode)

        newnode._postinit(
            target = target,
            iter = iter,
            body = body,
            orelse = orelse,
            type_comment = type_comment,
        )

        return newnode

    def visit_AsyncFor(self, node:ast.AsyncFor, parent:nodes.AST) -> nodes.AsyncFor:
        newnode = self.nodes.AsyncFor(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        target = self.visit(node.target, newnode)
        iter = self.visit(node.iter, newnode)
        body = [self.visit(n, newnode) for n in node.body]
        orelse = [self.visit(n, newnode) for n in node.orelse]
        type_comment = self.visit(node.type_comment, newnode)

        newnode._postinit(
            target = target,
            iter = iter,
            body = body,
            orelse = orelse,
            type_comment = type_comment,
        )

        return newnode

    def visit_While(self, node:ast.While, parent:nodes.AST) -> nodes.While:
        newnode = self.nodes.While(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        test = self.visit(node.test, newnode)
        body = [self.visit(n, newnode) for n in node.body]
        orelse = [self.visit(n, newnode) for n in node.orelse]

        newnode._postinit(
            test = test,
            body = body,
            orelse = orelse,
        )

        return newnode

    def visit_If(self, node:ast.If, parent:nodes.AST) -> nodes.If:
        newnode = self.nodes.If(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        test = self.visit(node.test, newnode)
        body = [self.visit(n, newnode) for n in node.body]
        orelse = [self.visit(n, newnode) for n in node.orelse]

        newnode._postinit(
            test = test,
            body = body,
            orelse = orelse,
        )

        return newnode

    def visit_With(self, node:ast.With, parent:nodes.AST) -> nodes.With:
        newnode = self.nodes.With(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        items = [self.visit(n, newnode) for n in node.items]
        body = [self.visit(n, newnode) for n in node.body]
        type_comment = self.visit(node.type_comment, newnode)

        newnode._postinit(
            items = items,
            body = body,
            type_comment = type_comment,
        )

        return newnode

    def visit_AsyncWith(self, node:ast.AsyncWith, parent:nodes.AST) -> nodes.AsyncWith:
        newnode = self.nodes.AsyncWith(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        items = [self.visit(n, newnode) for n in node.items]
        body = [self.visit(n, newnode) for n in node.body]
        type_comment = self.visit(node.type_comment, newnode)

        newnode._postinit(
            items = items,
            body = body,
            type_comment = type_comment,
        )

        return newnode

    def visit_Match(self, node:ast.Match, parent:nodes.AST) -> nodes.Match:
        newnode = self.nodes.Match(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        subject = self.visit(node.subject, newnode)
        cases = [self.visit(n, newnode) for n in node.cases]

        newnode._postinit(
            subject = subject,
            cases = cases,
        )

        return newnode

    def visit_Raise(self, node:ast.Raise, parent:nodes.AST) -> nodes.Raise:
        newnode = self.nodes.Raise(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        exc = self.visit(node.exc, newnode)
        cause = self.visit(node.cause, newnode)

        newnode._postinit(
            exc = exc,
            cause = cause,
        )

        return newnode

    def visit_Try(self, node:ast.Try, parent:nodes.AST) -> nodes.Try:
        newnode = self.nodes.Try(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        body = [self.visit(n, newnode) for n in node.body]
        handlers = [self.visit(n, newnode) for n in node.handlers]
        orelse = [self.visit(n, newnode) for n in node.orelse]
        finalbody = [self.visit(n, newnode) for n in node.finalbody]

        newnode._postinit(
            body = body,
            handlers = handlers,
            orelse = orelse,
            finalbody = finalbody,
        )

        return newnode

    def visit_Assert(self, node:ast.Assert, parent:nodes.AST) -> nodes.Assert:
        newnode = self.nodes.Assert(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        test = self.visit(node.test, newnode)
        msg = self.visit(node.msg, newnode)

        newnode._postinit(
            test = test,
            msg = msg,
        )

        return newnode

    def visit_Import(self, node:ast.Import, parent:nodes.AST) -> nodes.Import:
        newnode = self.nodes.Import(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        names = [self.visit(n, newnode) for n in node.names]

        newnode._postinit(
            names = names,
        )

        return newnode

    def visit_ImportFrom(self, node:ast.ImportFrom, parent:nodes.AST) -> nodes.ImportFrom:
        newnode = self.nodes.ImportFrom(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        module = self.visit(node.module, newnode)
        names = [self.visit(n, newnode) for n in node.names]
        level = self.visit(node.level, newnode)

        newnode._postinit(
            module = module,
            names = names,
            level = level,
        )

        return newnode

    def visit_Global(self, node:ast.Global, parent:nodes.AST) -> nodes.Global:
        newnode = self.nodes.Global(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        names = [self.visit(n, newnode) for n in node.names]

        newnode._postinit(
            names = names,
        )

        return newnode

    def visit_Nonlocal(self, node:ast.Nonlocal, parent:nodes.AST) -> nodes.Nonlocal:
        newnode = self.nodes.Nonlocal(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        names = [self.visit(n, newnode) for n in node.names]

        newnode._postinit(
            names = names,
        )

        return newnode

    def visit_Expr(self, node:ast.Expr, parent:nodes.AST) -> nodes.Expr:
        newnode = self.nodes.Expr(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        value = self.visit(node.value, newnode)

        newnode._postinit(
            value = value,
        )

        return newnode

    def visit_Pass(self, node:ast.Pass, parent:nodes.AST) -> nodes.Pass:
        newnode = self.nodes.Pass(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_Break(self, node:ast.Break, parent:nodes.AST) -> nodes.Break:
        newnode = self.nodes.Break(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_Continue(self, node:ast.Continue, parent:nodes.AST) -> nodes.Continue:
        newnode = self.nodes.Continue(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_BoolOp(self, node:ast.BoolOp, parent:nodes.AST) -> nodes.BoolOp:
        newnode = self.nodes.BoolOp(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        op = self.visit(node.op, newnode)
        values = [self.visit(n, newnode) for n in node.values]

        newnode._postinit(
            op = op,
            values = values,
        )

        return newnode

    def visit_NamedExpr(self, node:ast.NamedExpr, parent:nodes.AST) -> nodes.NamedExpr:
        newnode = self.nodes.NamedExpr(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        target = self.visit(node.target, newnode)
        value = self.visit(node.value, newnode)

        newnode._postinit(
            target = target,
            value = value,
        )

        return newnode

    def visit_BinOp(self, node:ast.BinOp, parent:nodes.AST) -> nodes.BinOp:
        newnode = self.nodes.BinOp(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        left = self.visit(node.left, newnode)
        op = self.visit(node.op, newnode)
        right = self.visit(node.right, newnode)

        newnode._postinit(
            left = left,
            op = op,
            right = right,
        )

        return newnode

    def visit_UnaryOp(self, node:ast.UnaryOp, parent:nodes.AST) -> nodes.UnaryOp:
        newnode = self.nodes.UnaryOp(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        op = self.visit(node.op, newnode)
        operand = self.visit(node.operand, newnode)

        newnode._postinit(
            op = op,
            operand = operand,
        )

        return newnode

    def visit_Lambda(self, node:ast.Lambda, parent:nodes.AST) -> nodes.Lambda:
        newnode = self.nodes.Lambda(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        args = self.visit(node.args, newnode)
        body = self.visit(node.body, newnode)

        newnode._postinit(
            args = args,
            body = body,
        )

        return newnode

    def visit_IfExp(self, node:ast.IfExp, parent:nodes.AST) -> nodes.IfExp:
        newnode = self.nodes.IfExp(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        test = self.visit(node.test, newnode)
        body = self.visit(node.body, newnode)
        orelse = self.visit(node.orelse, newnode)

        newnode._postinit(
            test = test,
            body = body,
            orelse = orelse,
        )

        return newnode

    def visit_Dict(self, node:ast.Dict, parent:nodes.AST) -> nodes.Dict:
        newnode = self.nodes.Dict(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        keys = [self.visit(n, newnode) for n in node.keys]
        values = [self.visit(n, newnode) for n in node.values]

        newnode._postinit(
            keys = keys,
            values = values,
        )

        return newnode

    def visit_Set(self, node:ast.Set, parent:nodes.AST) -> nodes.Set:
        newnode = self.nodes.Set(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        elts = [self.visit(n, newnode) for n in node.elts]

        newnode._postinit(
            elts = elts,
        )

        return newnode

    def visit_ListComp(self, node:ast.ListComp, parent:nodes.AST) -> nodes.ListComp:
        newnode = self.nodes.ListComp(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        elt = self.visit(node.elt, newnode)
        generators = [self.visit(n, newnode) for n in node.generators]

        newnode._postinit(
            elt = elt,
            generators = generators,
        )

        return newnode

    def visit_SetComp(self, node:ast.SetComp, parent:nodes.AST) -> nodes.SetComp:
        newnode = self.nodes.SetComp(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        elt = self.visit(node.elt, newnode)
        generators = [self.visit(n, newnode) for n in node.generators]

        newnode._postinit(
            elt = elt,
            generators = generators,
        )

        return newnode

    def visit_DictComp(self, node:ast.DictComp, parent:nodes.AST) -> nodes.DictComp:
        newnode = self.nodes.DictComp(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        key = self.visit(node.key, newnode)
        value = self.visit(node.value, newnode)
        generators = [self.visit(n, newnode) for n in node.generators]

        newnode._postinit(
            key = key,
            value = value,
            generators = generators,
        )

        return newnode

    def visit_GeneratorExp(self, node:ast.GeneratorExp, parent:nodes.AST) -> nodes.GeneratorExp:
        newnode = self.nodes.GeneratorExp(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        elt = self.visit(node.elt, newnode)
        generators = [self.visit(n, newnode) for n in node.generators]

        newnode._postinit(
            elt = elt,
            generators = generators,
        )

        return newnode

    def visit_Await(self, node:ast.Await, parent:nodes.AST) -> nodes.Await:
        newnode = self.nodes.Await(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        value = self.visit(node.value, newnode)

        newnode._postinit(
            value = value,
        )

        return newnode

    def visit_Yield(self, node:ast.Yield, parent:nodes.AST) -> nodes.Yield:
        newnode = self.nodes.Yield(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        value = self.visit(node.value, newnode)

        newnode._postinit(
            value = value,
        )

        return newnode

    def visit_YieldFrom(self, node:ast.YieldFrom, parent:nodes.AST) -> nodes.YieldFrom:
        newnode = self.nodes.YieldFrom(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        value = self.visit(node.value, newnode)

        newnode._postinit(
            value = value,
        )

        return newnode

    def visit_Compare(self, node:ast.Compare, parent:nodes.AST) -> nodes.Compare:
        newnode = self.nodes.Compare(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        left = self.visit(node.left, newnode)
        ops = [self.visit(n, newnode) for n in node.ops]
        comparators = [self.visit(n, newnode) for n in node.comparators]

        newnode._postinit(
            left = left,
            ops = ops,
            comparators = comparators,
        )

        return newnode

    def visit_Call(self, node:ast.Call, parent:nodes.AST) -> nodes.Call:
        newnode = self.nodes.Call(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        func = self.visit(node.func, newnode)
        args = [self.visit(n, newnode) for n in node.args]
        keywords = [self.visit(n, newnode) for n in node.keywords]

        newnode._postinit(
            func = func,
            args = args,
            keywords = keywords,
        )

        return newnode

    def visit_FormattedValue(self, node:ast.FormattedValue, parent:nodes.AST) -> nodes.FormattedValue:
        newnode = self.nodes.FormattedValue(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        value = self.visit(node.value, newnode)
        conversion = self.visit(node.conversion, newnode)
        format_spec = self.visit(node.format_spec, newnode)

        newnode._postinit(
            value = value,
            conversion = conversion,
            format_spec = format_spec,
        )

        return newnode

    def visit_JoinedStr(self, node:ast.JoinedStr, parent:nodes.AST) -> nodes.JoinedStr:
        newnode = self.nodes.JoinedStr(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        values = [self.visit(n, newnode) for n in node.values]

        newnode._postinit(
            values = values,
        )

        return newnode

    def visit_Constant(self, node:ast.Constant, parent:nodes.AST) -> nodes.Constant:
        newnode = self.nodes.Constant(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        value = self.visit(node.value, newnode)
        kind = self.visit(node.kind, newnode)

        newnode._postinit(
            value = value,
            kind = kind,
        )

        return newnode

    def visit_Attribute(self, node:ast.Attribute, parent:nodes.AST) -> nodes.Attribute:
        newnode = self.nodes.Attribute(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        value = self.visit(node.value, newnode)
        attr = self.visit(node.attr, newnode)
        ctx = self.visit(node.ctx, newnode)

        newnode._postinit(
            value = value,
            attr = attr,
            ctx = ctx,
        )

        return newnode

    def visit_Subscript(self, node:ast.Subscript, parent:nodes.AST) -> nodes.Subscript:
        newnode = self.nodes.Subscript(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        value = self.visit(node.value, newnode)
        slice = self.visit(node.slice, newnode)
        ctx = self.visit(node.ctx, newnode)

        newnode._postinit(
            value = value,
            slice = slice,
            ctx = ctx,
        )

        return newnode

    def visit_Starred(self, node:ast.Starred, parent:nodes.AST) -> nodes.Starred:
        newnode = self.nodes.Starred(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        value = self.visit(node.value, newnode)
        ctx = self.visit(node.ctx, newnode)

        newnode._postinit(
            value = value,
            ctx = ctx,
        )

        return newnode

    def visit_Name(self, node:ast.Name, parent:nodes.AST) -> nodes.Name:
        newnode = self.nodes.Name(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        id = self.visit(node.id, newnode)
        ctx = self.visit(node.ctx, newnode)

        newnode._postinit(
            id = id,
            ctx = ctx,
        )

        return newnode

    def visit_List(self, node:ast.List, parent:nodes.AST) -> nodes.List:
        newnode = self.nodes.List(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        elts = [self.visit(n, newnode) for n in node.elts]
        ctx = self.visit(node.ctx, newnode)

        newnode._postinit(
            elts = elts,
            ctx = ctx,
        )

        return newnode

    def visit_Tuple(self, node:ast.Tuple, parent:nodes.AST) -> nodes.Tuple:
        newnode = self.nodes.Tuple(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        elts = [self.visit(n, newnode) for n in node.elts]
        ctx = self.visit(node.ctx, newnode)

        newnode._postinit(
            elts = elts,
            ctx = ctx,
        )

        return newnode

    def visit_Slice(self, node:ast.Slice, parent:nodes.AST) -> nodes.Slice:
        newnode = self.nodes.Slice(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        lower = self.visit(node.lower, newnode)
        upper = self.visit(node.upper, newnode)
        step = self.visit(node.step, newnode)

        newnode._postinit(
            lower = lower,
            upper = upper,
            step = step,
        )

        return newnode

    def visit_Load(self, node:ast.Load, parent:nodes.AST) -> nodes.Load:
        newnode = self.nodes.Load(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_Store(self, node:ast.Store, parent:nodes.AST) -> nodes.Store:
        newnode = self.nodes.Store(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_Del(self, node:ast.Del, parent:nodes.AST) -> nodes.Del:
        newnode = self.nodes.Del(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_And(self, node:ast.And, parent:nodes.AST) -> nodes.And:
        newnode = self.nodes.And(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_Or(self, node:ast.Or, parent:nodes.AST) -> nodes.Or:
        newnode = self.nodes.Or(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_Add(self, node:ast.Add, parent:nodes.AST) -> nodes.Add:
        newnode = self.nodes.Add(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_Sub(self, node:ast.Sub, parent:nodes.AST) -> nodes.Sub:
        newnode = self.nodes.Sub(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_Mult(self, node:ast.Mult, parent:nodes.AST) -> nodes.Mult:
        newnode = self.nodes.Mult(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_MatMult(self, node:ast.MatMult, parent:nodes.AST) -> nodes.MatMult:
        newnode = self.nodes.MatMult(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_Div(self, node:ast.Div, parent:nodes.AST) -> nodes.Div:
        newnode = self.nodes.Div(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_Mod(self, node:ast.Mod, parent:nodes.AST) -> nodes.Mod:
        newnode = self.nodes.Mod(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_Pow(self, node:ast.Pow, parent:nodes.AST) -> nodes.Pow:
        newnode = self.nodes.Pow(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_LShift(self, node:ast.LShift, parent:nodes.AST) -> nodes.LShift:
        newnode = self.nodes.LShift(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_RShift(self, node:ast.RShift, parent:nodes.AST) -> nodes.RShift:
        newnode = self.nodes.RShift(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_BitOr(self, node:ast.BitOr, parent:nodes.AST) -> nodes.BitOr:
        newnode = self.nodes.BitOr(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_BitXor(self, node:ast.BitXor, parent:nodes.AST) -> nodes.BitXor:
        newnode = self.nodes.BitXor(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_BitAnd(self, node:ast.BitAnd, parent:nodes.AST) -> nodes.BitAnd:
        newnode = self.nodes.BitAnd(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_FloorDiv(self, node:ast.FloorDiv, parent:nodes.AST) -> nodes.FloorDiv:
        newnode = self.nodes.FloorDiv(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_Invert(self, node:ast.Invert, parent:nodes.AST) -> nodes.Invert:
        newnode = self.nodes.Invert(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_Not(self, node:ast.Not, parent:nodes.AST) -> nodes.Not:
        newnode = self.nodes.Not(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_UAdd(self, node:ast.UAdd, parent:nodes.AST) -> nodes.UAdd:
        newnode = self.nodes.UAdd(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_USub(self, node:ast.USub, parent:nodes.AST) -> nodes.USub:
        newnode = self.nodes.USub(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_Eq(self, node:ast.Eq, parent:nodes.AST) -> nodes.Eq:
        newnode = self.nodes.Eq(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_NotEq(self, node:ast.NotEq, parent:nodes.AST) -> nodes.NotEq:
        newnode = self.nodes.NotEq(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_Lt(self, node:ast.Lt, parent:nodes.AST) -> nodes.Lt:
        newnode = self.nodes.Lt(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_LtE(self, node:ast.LtE, parent:nodes.AST) -> nodes.LtE:
        newnode = self.nodes.LtE(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_Gt(self, node:ast.Gt, parent:nodes.AST) -> nodes.Gt:
        newnode = self.nodes.Gt(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_GtE(self, node:ast.GtE, parent:nodes.AST) -> nodes.GtE:
        newnode = self.nodes.GtE(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_Is(self, node:ast.Is, parent:nodes.AST) -> nodes.Is:
        newnode = self.nodes.Is(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_IsNot(self, node:ast.IsNot, parent:nodes.AST) -> nodes.IsNot:
        newnode = self.nodes.IsNot(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_In(self, node:ast.In, parent:nodes.AST) -> nodes.In:
        newnode = self.nodes.In(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_NotIn(self, node:ast.NotIn, parent:nodes.AST) -> nodes.NotIn:
        newnode = self.nodes.NotIn(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )


        return newnode

    def visit_comprehension(self, node:ast.comprehension, parent:nodes.AST) -> nodes.comprehension:
        newnode = self.nodes.comprehension(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        target = self.visit(node.target, newnode)
        iter = self.visit(node.iter, newnode)
        ifs = [self.visit(n, newnode) for n in node.ifs]
        is_async = self.visit(node.is_async, newnode)

        newnode._postinit(
            target = target,
            iter = iter,
            ifs = ifs,
            is_async = is_async,
        )

        return newnode

    def visit_ExceptHandler(self, node:ast.ExceptHandler, parent:nodes.AST) -> nodes.ExceptHandler:
        newnode = self.nodes.ExceptHandler(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        type = self.visit(node.type, newnode)
        name = self.visit(node.name, newnode)
        body = [self.visit(n, newnode) for n in node.body]

        newnode._postinit(
            type = type,
            name = name,
            body = body,
        )

        return newnode

    def visit_arguments(self, node:ast.arguments, parent:nodes.AST) -> nodes.arguments:
        newnode = self.nodes.arguments(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        posonlyargs = [self.visit(n, newnode) for n in node.posonlyargs]
        args = [self.visit(n, newnode) for n in node.args]
        vararg = self.visit(node.vararg, newnode)
        kwonlyargs = [self.visit(n, newnode) for n in node.kwonlyargs]
        kw_defaults = [self.visit(n, newnode) for n in node.kw_defaults]
        kwarg = self.visit(node.kwarg, newnode)
        defaults = [self.visit(n, newnode) for n in node.defaults]

        newnode._postinit(
            posonlyargs = posonlyargs,
            args = args,
            vararg = vararg,
            kwonlyargs = kwonlyargs,
            kw_defaults = kw_defaults,
            kwarg = kwarg,
            defaults = defaults,
        )

        return newnode

    def visit_arg(self, node:ast.arg, parent:nodes.AST) -> nodes.arg:
        newnode = self.nodes.arg(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        arg = self.visit(node.arg, newnode)
        annotation = self.visit(node.annotation, newnode)
        type_comment = self.visit(node.type_comment, newnode)

        newnode._postinit(
            arg = arg,
            annotation = annotation,
            type_comment = type_comment,
        )

        return newnode

    def visit_keyword(self, node:ast.keyword, parent:nodes.AST) -> nodes.keyword:
        newnode = self.nodes.keyword(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        arg = self.visit(node.arg, newnode)
        value = self.visit(node.value, newnode)

        newnode._postinit(
            arg = arg,
            value = value,
        )

        return newnode

    def visit_alias(self, node:ast.alias, parent:nodes.AST) -> nodes.alias:
        newnode = self.nodes.alias(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        name = self.visit(node.name, newnode)
        asname = self.visit(node.asname, newnode)

        newnode._postinit(
            name = name,
            asname = asname,
        )

        return newnode

    def visit_withitem(self, node:ast.withitem, parent:nodes.AST) -> nodes.withitem:
        newnode = self.nodes.withitem(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        context_expr = self.visit(node.context_expr, newnode)
        optional_vars = self.visit(node.optional_vars, newnode)

        newnode._postinit(
            context_expr = context_expr,
            optional_vars = optional_vars,
        )

        return newnode

    def visit_match_case(self, node:ast.match_case, parent:nodes.AST) -> nodes.match_case:
        newnode = self.nodes.match_case(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        pattern = self.visit(node.pattern, newnode)
        guard = self.visit(node.guard, newnode)
        body = [self.visit(n, newnode) for n in node.body]

        newnode._postinit(
            pattern = pattern,
            guard = guard,
            body = body,
        )

        return newnode

    def visit_MatchValue(self, node:ast.MatchValue, parent:nodes.AST) -> nodes.MatchValue:
        newnode = self.nodes.MatchValue(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        value = self.visit(node.value, newnode)

        newnode._postinit(
            value = value,
        )

        return newnode

    def visit_MatchSingleton(self, node:ast.MatchSingleton, parent:nodes.AST) -> nodes.MatchSingleton:
        newnode = self.nodes.MatchSingleton(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        value = self.visit(node.value, newnode)

        newnode._postinit(
            value = value,
        )

        return newnode

    def visit_MatchSequence(self, node:ast.MatchSequence, parent:nodes.AST) -> nodes.MatchSequence:
        newnode = self.nodes.MatchSequence(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        patterns = [self.visit(n, newnode) for n in node.patterns]

        newnode._postinit(
            patterns = patterns,
        )

        return newnode

    def visit_MatchMapping(self, node:ast.MatchMapping, parent:nodes.AST) -> nodes.MatchMapping:
        newnode = self.nodes.MatchMapping(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        keys = [self.visit(n, newnode) for n in node.keys]
        patterns = [self.visit(n, newnode) for n in node.patterns]
        rest = self.visit(node.rest, newnode)

        newnode._postinit(
            keys = keys,
            patterns = patterns,
            rest = rest,
        )

        return newnode

    def visit_MatchClass(self, node:ast.MatchClass, parent:nodes.AST) -> nodes.MatchClass:
        newnode = self.nodes.MatchClass(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        cls = self.visit(node.cls, newnode)
        patterns = [self.visit(n, newnode) for n in node.patterns]
        kwd_attrs = [self.visit(n, newnode) for n in node.kwd_attrs]
        kwd_patterns = [self.visit(n, newnode) for n in node.kwd_patterns]

        newnode._postinit(
            cls = cls,
            patterns = patterns,
            kwd_attrs = kwd_attrs,
            kwd_patterns = kwd_patterns,
        )

        return newnode

    def visit_MatchStar(self, node:ast.MatchStar, parent:nodes.AST) -> nodes.MatchStar:
        newnode = self.nodes.MatchStar(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        name = self.visit(node.name, newnode)

        newnode._postinit(
            name = name,
        )

        return newnode

    def visit_MatchAs(self, node:ast.MatchAs, parent:nodes.AST) -> nodes.MatchAs:
        newnode = self.nodes.MatchAs(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        pattern = self.visit(node.pattern, newnode)
        name = self.visit(node.name, newnode)

        newnode._postinit(
            pattern = pattern,
            name = name,
        )

        return newnode

    def visit_MatchOr(self, node:ast.MatchOr, parent:nodes.AST) -> nodes.MatchOr:
        newnode = self.nodes.MatchOr(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        patterns = [self.visit(n, newnode) for n in node.patterns]

        newnode._postinit(
            patterns = patterns,
        )

        return newnode

    def visit_TypeIgnore(self, node:ast.TypeIgnore, parent:nodes.AST) -> nodes.TypeIgnore:
        newnode = self.nodes.TypeIgnore(
            parent = parent,
            lineno = getattr(node, 'lineno', -1),
            col_offset = getattr(node, 'col_offset', -1),
            end_lineno = getattr(node, 'end_lineno', -1),
            end_col_offset = getattr(node, 'end_col_offset', -1),
        )

        lineno = self.visit(node.lineno, newnode)
        tag = self.visit(node.tag, newnode)

        newnode._postinit(
            lineno = lineno,
            tag = tag,
        )

        return newnode



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


