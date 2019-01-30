from graph import BCGraph
from matplotlib import collections as mc
from matplotlib.path import Path
import matplotlib.patches as patches

class GraphPlotter(object):
    FONT_SIZE = 4

    def __init__(self, ax):
        self._ax = ax


    def draw_vertex(self, xy, color='w'):
        self._ax.add_artist(patches.Circle(xy, radius=0.045, facecolor=color, edgecolor='black'))

    def plot(self, graph: BCGraph):
        margin = 0.1
        black_delta = 0.25
        height = black_delta * (len(graph.V0) + 1)
        white_delta = height / (len(graph.V1) + 1)

        self._ax.set_xlim(-0.2, 1.2)
        self._ax.set_ylim(height - 1.2, height + 0.2)


        black = []
        white = []

        for i in range(len(graph.V0)):
            pos = (0, height - black_delta - black_delta * i)
            black.append(pos)
            self.draw_vertex(pos, color='black')

        for i in range(len(graph.V1)):
            pos = (1, height - white_delta - white_delta * i)
            white.append(pos)
            self.draw_vertex(pos, color='w')

        lines = []

        linewidth = 1.45

        for i in range(len(graph.V0)):
            nei = graph.V0[i]

            if GraphPlotter.has_parallel(nei):
                sx, sy = black[i]
                ex, ey = white[nei[0]]
                # mid1 = ((sx + ex)/2, (sy + ey)/2 + 0.075)
                # mid2 = ((sx + ex) / 2, (sy + ey) / 2 - 0.075)
                mid1 = GraphPlotter.lerp(black[i], white[nei[0]], y_shift=0.075)
                mid2 = GraphPlotter.lerp(black[i], white[nei[0]], y_shift=-0.075)

                vertices_1 = [
                    black[i],
                    mid1,
                    mid1,
                    white[nei[0]]
                ]
                vertices_2 = [
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
                path1 = Path(vertices_1, codes)
                self._ax.text(
                    mid1[0],
                    mid1[1],
                    '1',
                    fontsize=GraphPlotter.FONT_SIZE,
                    bbox=dict(facecolor='w', edgecolor='black', boxstyle='round')
                )
                path2 = Path(vertices_2, codes)
                self._ax.text(
                    mid2[0],
                    mid2[1],
                    '2',
                    fontsize=GraphPlotter.FONT_SIZE,
                    bbox=dict(facecolor='w', edgecolor='black', boxstyle='round')
                )

                patch1 = patches.PathPatch(path1, facecolor='none', linewidth=linewidth, zorder=-10)
                patch2 = patches.PathPatch(path2, facecolor='none', linewidth=linewidth, zorder=-10)

                self._ax.add_patch(patch1)
                self._ax.add_patch(patch2)
            else:
                for n in nei:
                    if len(graph.V1[n]) == 3:
                        if GraphPlotter.has_parallel(graph.V1[n]):
                            pos = GraphPlotter.lerp(black[i], white[n], 0.5)
                            self._ax.text(
                                pos[0],
                                pos[1],
                                '3',
                                fontsize=GraphPlotter.FONT_SIZE,
                                bbox=dict(facecolor='w', edgecolor='black', boxstyle='round')
                            )
                        else:
                            pos = GraphPlotter.lerp(black[i], white[n], 0.35)
                            self._ax.text(
                                pos[0],
                                pos[1],
                                str(graph.V1[n].index(i) + 1),
                                fontsize=GraphPlotter.FONT_SIZE,
                                bbox=dict(facecolor='w', edgecolor='black', boxstyle='round')
                            )
                    lines.append([white[n], black[i]])

        lc = mc.LineCollection(lines, linewidths=linewidth, colors=['black'] * len(lines), zorder=-10)
        self._ax.add_collection(lc)

    @staticmethod
    def lerp(start, end, t=0.5, x_shift=0.0, y_shift=0.0):
        return ((1 - t)*start[0] + t*end[0] + x_shift, (1 - t)*start[1] + t*end[1] + y_shift)

    @staticmethod
    def has_parallel(nei):
        return len(set(nei)) != len(nei)
