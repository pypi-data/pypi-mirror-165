from typing import Any
import ast

from ast_nodes import rewriter, nodes
from . import parse_randommodules

class Scope(nodes.stmt):
    ...

class CustomNodes(rewriter.Nodes):
    
    class Module(nodes.Module, Scope):
        def _postinit(self,**kwargs:Any) -> None:
            super()._postinit(**kwargs)
            self.custom_property = None
    
    class ClassDef(nodes.ClassDef, Scope):
        ...
    
    class FunctionDef(nodes.FunctionDef, Scope):
        ...


class CustomRewriter(rewriter.Rewriter):
    def visit_Module(self, node: ast.Module, parent: None) -> nodes.Module:
        m = super().visit_Module(node, parent)
        m.custom_property = '<test>'
        return m


def test_basic():

    mods = list(parse_randommodules())
    mods = list(parse_randommodules(nodes=CustomNodes, rewritercls=CustomRewriter))
    
    for old_mod, new_mod in mods:
        for node in ast.walk(new_mod):
            if isinstance(node, (ast.Module, ast.FunctionDef, ast.ClassDef)):
                assert isinstance(node, Scope)
            if not isinstance(node, ast.Module):
                assert node.parent is not None
            else:
                assert node.parent is None
                assert node.custom_property == '<test>'
