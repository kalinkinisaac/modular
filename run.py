from geo_drawer import geo_drawer
from special_polygon import get_all
from graph_constructor import get_graph
from subgroups import *
#from graph_drawer import draw_graph
from reduction import decompose
from fimath import Mat, Field

gamma = GammaTopZero(24)
graph = get_graph(gamma)

domain, tree, involutions = get_all(graph)

s1, s2, generators = zip(*involutions)

print(f'Generators: {list(map(lambda m: m.inv(), generators))}')

geo_drawer.plot(domain, linewidth=1.0)
geo_drawer.plot(tree, color='red', alpha=0.8, linewidth=0.75, linestyle='--')

p = Field(0.5+2j)
m = Mat(0,1,-1,0)
decomposition = decompose(polygon=domain, involutions=involutions, z=p, w=m.moe(p))
# dec = '\n'.join(map(str, decompose(polygon=domain, involutions=involutions, z=p, w=m.moe(p))))
# print(f'Decompostion of matrix\n{m}\n\n{dec}')
# print('check')
# r = Mat.identity()
# for m in decomposition:
#     r = r * m
# print(r)


geo_drawer.show()