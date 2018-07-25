from geo_drawer import geo_drawer
from special_polygon import get_all
from graph_constructor import get_graph
from subgroups import *
from graph_drawer import draw_graph

gamma = GammaBotOne(2)
graph = get_graph(gamma)

domain, tree, involutions = get_all(graph)

s1, s2, generators = zip(*involutions)

geo_drawer.plot(domain, linewidth=1.0)
geo_drawer.plot(tree, color='red', alpha=0.8, linewidth=0.75, linestyle='--')

draw_graph(graph)
