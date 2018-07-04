import matplotlib.pyplot as plt

fig = plt.figure(num=1, figsize=(4, 3), dpi=240, facecolor='gray', edgecolor='k')
ax = fig.add_subplot(111)
ax.set_axis_off()
ax.set_aspect('equal')

from .graph_drawer import bipartite_draw_graph as draw_graph