import matplotlib.pyplot as plt
from .graph_drawer import GraphDrawer
from mpl_canvas import MplCanvas
from .config import fig_config, ax_config

def draw_graph(graph, _show=True):
    fig = plt.figure(**fig_config)
    ax = fig.add_subplot(111)
    ax_config(ax)

    gd = GraphDrawer(ax)
    gd.draw(graph)

    if _show:
        plt.show()


__all__ = ['draw_graph', 'GraphDrawer']