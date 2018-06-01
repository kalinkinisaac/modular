import matplotlib.pyplot as plt
from .graph_drawer import bipartite_draw_graph as bgd


# fig = plt.figure(num=None, figsize=(10, 6), dpi=120, facecolor='w', edgecolor='k')
# ax = fig.add_subplot(111)
# ax.set_aspect('equal')
# ax.set_xlim(-1.5, 1.5)
# ax.set_ylim(-2, 2)


def draw_graph(bc_graph):
    bgd(bc_graph)
    # plt.savefig('test.png')
    plt.show()