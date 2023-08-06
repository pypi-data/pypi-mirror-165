from pathlib import Path
import ast
from typing import Iterator, List, Tuple, Type

from ast_nodes import nodes, rewriter

def parse_mod(folder:str, modname:str, 
              nodes:rewriter.NodesT=nodes, 
              rewritercls:Type[rewriter.Rewriter]=rewriter.Rewriter) -> Tuple[ast.Module, nodes.Module]:
    
    file = Path(__file__).parent / folder / f"{modname}.py"
    contents = file.read_text()
    old_mod = ast.parse(contents)
    new_mod = rewritercls(nodes=nodes).visit(old_mod, parent=None)
    assert ast.dump(old_mod) == ast.dump(new_mod)

    return old_mod, new_mod

def parse_randommodules(nodes:rewriter.NodesT=nodes, 
                            rewritercls:Type[rewriter.Rewriter]=rewriter.Rewriter) -> Iterator[Tuple[ast.Module, nodes.Module]]:
    for entry in (Path(__file__).parent / 'randommodules').iterdir():
        if entry.is_file():
            yield parse_mod('randommodules', entry.stem, nodes=nodes, rewritercls=rewritercls)
