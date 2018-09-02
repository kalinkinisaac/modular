from geo_drawer import geo_drawer
from special_polygon import get_all
from graph_constructor import get_graph
from subgroups import *
#from graph_drawer import draw_graph
from reduction import decompose
from fimath import Matrix, Field

gamma = GammaBotOne(5)
graph = get_graph(gamma)

domain, tree, involutions = get_all(graph)

s1, s2, generators = zip(*involutions)

print(f'Generators: {list(map(lambda m: m.inv(), generators))}')
print(f'Involutions: {involutions}')
geo_drawer.draw(domain, linewidth=1.0)
geo_drawer.draw(tree, color='red', alpha=0.8, linewidth=0.75, linestyle='--')
#draw_graph(graph)
p = Field(0.5+1.5j)
m = Matrix(6, 13,
           5, 11)
w=m.moe(p)
print(p, w)
decomposition = decompose(polygon=domain, involutions=involutions, z=p, w=w)
dec = '\n'.join(map(str, decomposition))
print(f'Decompostion of matrix\n{m}\n\n{dec}')
print('check')
r = Matrix.identity()
for m in decomposition:
    r *= m
print(r)


geo_drawer.show()