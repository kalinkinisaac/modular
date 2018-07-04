from graph import BCGraph
from matplotlib import collections  as mc
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches
from matplotlib.patches import Circle
from . import ax

def draw_vertex(xy, color='w'):
    ax.add_patch(Circle(xy, radius=0.05, linewidth=0.005,  color=color))

def bipartite_draw_graph(graph : BCGraph):
    margin = 0.1

    x_min, x_max = ax.get_xbound()
    y_min, y_max = ax.get_ybound()

    margin_x_min = x_min + margin * (x_max - x_min)
    margin_x_max = x_max + margin * (x_min - x_max)
    margin_y_min = y_min + margin * (y_max - y_min)
    margin_y_max = y_max + margin * (y_min - y_max)


    black = [[] for i in graph.V0]
    white = [[] for i in graph.V1]

    for i in range(len(graph.V0)):
        pos = (i + 1) / (len(graph.V0) + 1)
        y = margin_y_max + pos * (margin_y_min - margin_y_max)
        black[i] = [margin_x_min, y]
        draw_vertex((margin_x_min, y), color='black')

    for i in range(len(graph.V1)):
        pos = (i + 1) / (len(graph.V1) + 1)
        y = margin_y_max + pos * (margin_y_min - margin_y_max)
        white[i] = [margin_x_max, y]
        draw_vertex((margin_x_max, y), color='w')

    lines = []
    for i in range(len(graph.V0)):
        nei = graph.V0[i]
        if has_parallel(nei):
            sx, sy = black[i]
            ex, ey = white[nei[0]]
            mid1 = ((sx + ex)/2, (sy + ey)/2 + 0.05)
            mid2 = ((sx + ex) / 2, (sy + ey) / 2 - 0.05)
            verts1 = [
                black[i],
                mid1,
                mid1,
                white[nei[0]]
            ]
            verts2 = [
                black[i],
                mid2,
                mid2,
                white[nei[0]]
            ]
            codes = [Path.MOVETO,
                     Path.CURVE4,
                     Path.CURVE4,
                     Path.CURVE4,
                     ]
            path1 = Path(verts1, codes)
            path2 = Path(verts2, codes)
            patch1 = patches.PathPatch(path1, facecolor='none', lw=2, zorder=-10)
            patch2 = patches.PathPatch(path2, facecolor='none', lw=2, zorder=-10)
            ax.add_patch(patch1)
            ax.add_patch(patch2)
        else:
            for n in nei:
                lines.append([white[n], black[i]])

    lc = mc.LineCollection(lines, linewidths=2, colors=['black' for l in lines], zorder=-10)
    ax.add_collection(lc)

    plt.show()

def has_parallel(nei):
    return len(set(nei)) != len(nei)

