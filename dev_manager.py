from special_polygon.drawer import draw_polygon
from special_polygon import SPolygon
from graph_constructor import construct_g_0_graph
from classical_congruence_subgroups.gamma_zero import GammaBottomZero, GammaTopZero
from graph import BCGraph

# 2> ??? <300

g2 = GammaTopZero(3)
g2_graph = construct_g_0_graph(g2)

G_gr = BCGraph(V0=[[0, 1], [0, 1], [0, 1]], V1=[[0, 1, 2], [0, 1, 2]], dist_edge=[2, 0, 0])

sp = SPolygon(g2_graph)
E, T, inv = sp.construct_polygon()

s1 = list(map(lambda x: x[0], inv))
s2 = list(map(lambda x: x[1], inv))
gs = list(map(lambda x: x[2], inv))

print(gs)

draw_polygon(E, linewidth=1.0)
draw_polygon(T, color='red', alpha=0.8, linewidth=0.75, linestyle='--')



#from graph_drawer import draw_graph

#draw_graph(g2_graph)