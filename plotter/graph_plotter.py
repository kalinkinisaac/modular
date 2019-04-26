from graph import BCGraph
from matplotlib import collections as mc
from matplotlib.path import Path
import matplotlib.patches as patches
from matplotlib.lines import Line2D


class GraphPlotter(object):
    FONT_SIZE = 4
    CYCLE_COLORS = ('darkblue', 'blue', 'lightblue')

    def __init__(self, ax):
        self._ax = ax

    def draw_vertex(self, xy, color='w'):
        self._ax.add_patch(patches.Circle(xy, radius=0.045, facecolor=color, edgecolor='black'))

    def plot(self, graph: BCGraph, cycle_colors=CYCLE_COLORS, cycle_text=False):
        black_delta = 0.25
        height = black_delta * (len(graph.V0) + 1)
        white_delta = height / (len(graph.V1) + 1)

        self._ax.set_xlim(-0.2, 1.2)
        self._ax.set_ylim(height - 1.2, height + 0.2)

        blacks = []
        whites = []

        for i in range(len(graph.V0)):
            pos = (0, height - black_delta - black_delta * i)
            blacks.append(pos)
            self.draw_vertex(pos, color='black')

        for i in range(len(graph.V1)):
            pos = (1, height - white_delta - white_delta * i)
            whites.append(pos)
            self.draw_vertex(pos, color='w')

        line_width = 1.45

        for i in range(len(graph.V0)):
            neighbors = graph.V0[i]

            if GraphPlotter.has_parallel(neighbors):
                mid1 = GraphPlotter.lerp(blacks[i], whites[neighbors[0]], y_shift=0.075)
                mid2 = GraphPlotter.lerp(blacks[i], whites[neighbors[0]], y_shift=-0.075)

                vertices_1 = [
                    blacks[i],
                    mid1,
                    mid1,
                    whites[neighbors[0]]
                ]
                vertices_2 = [
                    blacks[i],
                    mid2,
                    mid2,
                    whites[neighbors[0]]
                ]
                codes = [
                    Path.MOVETO,
                    Path.CURVE4,
                    Path.CURVE4,
                    Path.CURVE4
                ]

                path1 = Path(vertices_1, codes)

                if cycle_text:
                    self._ax.text(
                        mid1[0],
                        mid1[1],
                        '1',
                        fontsize=GraphPlotter.FONT_SIZE,
                        bbox=dict(facecolor='w', edgecolor='black', boxstyle='round')
                    )
                path2 = Path(vertices_2, codes)
                if cycle_text:
                    self._ax.text(
                        mid2[0],
                        mid2[1],
                        '2',
                        fontsize=GraphPlotter.FONT_SIZE,
                        bbox=dict(facecolor='w', edgecolor='black', boxstyle='round')
                    )

                patch1 = patches.PathPatch(
                    path1,
                    edgecolor=cycle_colors[0],
                    facecolor='none',
                    linewidth=line_width,
                    zorder=-10
                )

                patch2 = patches.PathPatch(
                    path2,
                    edgecolor=cycle_colors[1],
                    facecolor='none',
                    linewidth=line_width,
                    zorder=-10
                )

                self._ax.add_patch(patch1)
                self._ax.add_patch(patch2)
            else:
                for n in neighbors:
                    color = None
                    if len(graph.V1[n]) == 3:
                        if GraphPlotter.has_parallel(graph.V1[n]):
                            pos = GraphPlotter.lerp(blacks[i], whites[n], 0.5)
                            if cycle_text:
                                self._ax.text(
                                    pos[0],
                                    pos[1],
                                    '3',
                                    fontsize=GraphPlotter.FONT_SIZE,
                                    bbox=dict(facecolor='w', edgecolor='black', boxstyle='round')
                                )
                            color = cycle_colors[2]
                        else:
                            pos = GraphPlotter.lerp(blacks[i], whites[n], 0.35)
                            if cycle_text:
                                self._ax.text(
                                    pos[0],
                                    pos[1],
                                    str(graph.V1[n].index(i) + 1),
                                    fontsize=GraphPlotter.FONT_SIZE,
                                    bbox=dict(facecolor='w', edgecolor='black', boxstyle='round')
                                )
                            color = cycle_colors[graph.V1[n].index(i)]
                    else:
                        color = 'black'
                    x_min = whites[n][0]
                    x_max = blacks[i][0]
                    y_min = whites[n][1]
                    y_max = blacks[i][1]
                    self._ax.add_line(Line2D([x_min, x_max], [y_min, y_max], color=color, zorder=-10, linewidth=line_width))

        #lc = mc.LineCollection(lines, linewidths=line_width, colors=colors, zorder=-10)
        #self._ax.add_collection(lc)

    @staticmethod
    def lerp(start, end, t=0.5, x_shift=0.0, y_shift=0.0):
        return (1 - t)*start[0] + t*end[0] + x_shift, (1 - t)*start[1] + t*end[1] + y_shift

    @staticmethod
    def has_parallel(nei):
        return len(set(nei)) != len(nei)
