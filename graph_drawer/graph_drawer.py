from graph import BCGraph
import networkx as nx
from networkx.algorithms import bipartite
from networkx.drawing.nx_pydot import write_dot

def bipartite_draw_graph(bc_graph : BCGraph):
    bipartite_graph = nx.MultiGraph()
    bipartite_graph.add_nodes_from(list(map(lambda n: str(n), range(len(bc_graph.V0)))), bipartite=0)
    bipartite_graph.add_nodes_from(list(map(lambda n: str(n) + '_', range(len(bc_graph.V1)))), bipartite=1)
    for i, v in enumerate(bc_graph.V1):
        for v0 in v:
            v1 = str(i) + '_'
            bipartite_graph.add_edges_from([(v1, str(v0))])



    write_dot(bipartite_graph, 'graph.dot')


