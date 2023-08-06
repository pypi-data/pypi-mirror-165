from .core import *

from .core.bp import GenerateGraphWidget


from yfiles_jupyter_graphs import GraphWidget


def generate_graph(d_nodes: dict, edges: list) -> GraphWidget:
    return GenerateGraphWidget().process(
        d_nodes=d_nodes,
        edges=edges,
        directed=True)
