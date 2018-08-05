from geo_drawer import geo_drawer
from special_polygon import get_all
from graph_constructor import get_graph
from subgroups import *
#from graph_drawer import draw_graph
from reduction import decompose
from fimath import Mat, Field

gamma = GammaBotZero(2)
graph = get_graph(gamma)

domain, tree, involutions = get_all(graph)

s1, s2, generators = zip(*involutions)

print(generators)

geo_drawer.plot(domain, linewidth=1.0)
geo_drawer.plot(tree, color='red', alpha=0.8, linewidth=0.75, linestyle='--')

p = Field(0.5+1j)
print(decompose(polygon=domain, involutions=involutions, z=p, w=Mat(1,0,2,1).moe(p)))


geo_drawer.show()