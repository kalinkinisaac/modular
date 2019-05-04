from graph import BCGraph
from .plotter import Plotter
from matplotlib.path import Path
import matplotlib.patches as patches
from matplotlib.lines import Line2D
import numpy as np
from scipy import interpolate


class GraphPlotter(Plotter):
    FONT_SIZE = 4
    CYCLE_COLORS = ('darkblue', 'blue', 'lightblue')

    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)

    def draw_vertex(self, xy, color='white'):
        if self._ax:
            self._ax.add_patch(patches.Circle(xy, radius=0.045, facecolor=color, edgecolor='black'))
        if self._bokeh_fig:
            x, y = xy
            self._bokeh_fig.circle(x, y, radius=0.045, color=color, line_color='black')

    def patch_bokeh(self, start, mid, end, *args, **kwargs):
        xs = [start[0], mid[0], end[0]]
        ys = [start[1], mid[1], end[1]]

        x2 = np.linspace(xs[0], xs[-1], 100)
        y2 = interpolate.pchip_interpolate(xs, ys, x2)
        self._bokeh_fig.line(x2, y2, *args, **kwargs)

    def plot(self, graph: BCGraph, cycle_colors=CYCLE_COLORS):
        black_delta = 0.25
        height = black_delta * (len(graph.V0) + 1)
        white_delta = height / (len(graph.V1) + 1)

        if self._ax:
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
            self.draw_vertex(pos, color='white')

        line_width = 1.45

        for i in range(len(graph.V0)):
            neighbors = graph.V0[i]

            if GraphPlotter.has_parallel(neighbors):
                start = blacks[i]
                end = whites[neighbors[0]]
                mid_top = GraphPlotter.lerp(start, end, y_shift=0.075)
                mid_bot = GraphPlotter.lerp(start, end, y_shift=-0.075)
                mid_top2 = GraphPlotter.lerp(start, end, y_shift=0.03)
                mid_bot2 = GraphPlotter.lerp(start, end, y_shift=-0.03)

                if self._ax:
                    codes = [
                        Path.MOVETO,
                        Path.CURVE4,
                        Path.CURVE4,
                        Path.CURVE4
                    ]

                    path1 = Path([start, mid_top, mid_top, end], codes)
                    path2 = Path([start, mid_bot, mid_bot, end], codes)

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

                if self._bokeh_fig:
                    self.patch_bokeh(
                        start,
                        mid_top2,
                        end,
                        color=cycle_colors[0],
                        line_width=line_width,
                        level='underlay'
                    )
                    self.patch_bokeh(
                        start,
                        mid_bot2,
                        end,
                        color=cycle_colors[1],
                        line_width=line_width,
                        level='underlay'
                    )

            else:
                for n in neighbors:
                    if len(graph.V1[n]) == 3:
                        if GraphPlotter.has_parallel(graph.V1[n]):
                            color = cycle_colors[2]
                        else:
                            color = cycle_colors[graph.V1[n].index(i)]
                    else:
                        color = 'black'
                    x_min = whites[n][0]
                    x_max = blacks[i][0]
                    y_min = whites[n][1]
                    y_max = blacks[i][1]

                    if self._ax:
                        self._ax.add_line(
                            Line2D(
                                [x_min, x_max],
                                [y_min, y_max],
                                color=color,
                                zorder=-10,
                                linewidth=line_width
                            )
                        )

                    if self._bokeh_fig:
                        self._bokeh_fig.line(
                            [x_min, x_max],
                            [y_min, y_max],
                            color=color,
                            line_width=line_width,
                            level='underlay'
                        )

    @staticmethod
    def lerp(start, end, t=0.5, x_shift=0.0, y_shift=0.0):
        return (1 - t)*start[0] + t*end[0] + x_shift, (1 - t)*start[1] + t*end[1] + y_shift

    @staticmethod
    def has_parallel(nei):
        return len(set(nei)) != len(nei)
