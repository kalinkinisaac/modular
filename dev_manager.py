from special_polygon.drawer import draw_lines
from special_polygon import get_all
from graph_constructor import get_graph
from subgroups import *
from graph_drawer import draw_graph

gamma = Gamma(4)
graph = get_graph(gamma)
domain, tree, involutions = get_all(graph)

s1, s2, generators = zip(*involutions)
print(generators)

draw_graph(graph)

draw_lines(domain, linewidth=1.0)
draw_lines(tree, color='red', alpha=0.8, linewidth=0.75, linestyle='--')

