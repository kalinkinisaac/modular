from .plotter import Plotter


class MarkerPlotter(Plotter):
    ALPHA = 0.7
    Z_ORDER = 10
    SIZE = 20
    LINE_WIDTH = 4

    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)
        self._ax_whites = None
        self._ax_blacks = None
        self._ax_cuts = None
        self._ax_legend = None
        self._visible = True

    def plot(self, white, black, cut, legend=False):
        if white:
            if self._ax:
                self._ax_whites = self._ax.scatter(
                    [p.real for p in white], [p.imag for p in white],
                    marker='o',
                    c='white',
                    alpha=MarkerPlotter.ALPHA,
                    edgecolors='black',
                    zorder=MarkerPlotter.Z_ORDER,
                    label='white vertices',
                    s=MarkerPlotter.SIZE
                )
            if self._bokeh_fig:
                self._bokeh_fig.circle(
                    [float(p.real) for p in white],
                    [float(p.imag) for p in white],
                    color='white',
                    line_color='black',
                    fill_alpha=MarkerPlotter.ALPHA,
                    line_alpha=MarkerPlotter.ALPHA,
                    line_width=self.LINE_WIDTH,
                    size=MarkerPlotter.SIZE
                )
        if black:
            if self._ax:
                self._ax_blacks = self._ax.scatter(
                    [float(p.real) for p in black],
                    [float(p.imag) for p in black],
                    marker='o',
                    color='black',
                    alpha=MarkerPlotter.ALPHA,
                    edgecolors='black',
                    zorder=MarkerPlotter.Z_ORDER,
                    label='black vertices',
                    s=MarkerPlotter.SIZE
                )
            if self._bokeh_fig:
                self._bokeh_fig.circle(
                    [float(p.real) for p in black],
                    [float(p.imag) for p in black],
                    color='black',
                    fill_alpha=MarkerPlotter.ALPHA,
                    line_alpha=MarkerPlotter.ALPHA,
                    line_width=self.LINE_WIDTH,
                    size=MarkerPlotter.SIZE
                )
        if cut:
            if self._ax:
                self._ax_cuts = self._ax.scatter(
                    [p.real for p in cut],
                    [p.imag for p in cut],
                    marker='x',
                    color='black',
                    alpha=MarkerPlotter.ALPHA,
                    edgecolors='black',
                    zorder=MarkerPlotter.Z_ORDER,
                    label='cut vertices',
                    s=MarkerPlotter.SIZE
                )
            if self._bokeh_fig:
                self._bokeh_fig.x(
                    [float(p.real) for p in cut],
                    [float(p.imag) for p in cut],
                    color='black',
                    fill_alpha=MarkerPlotter.ALPHA,
                    line_alpha=MarkerPlotter.ALPHA,
                    line_width=self.LINE_WIDTH,
                    size=MarkerPlotter.SIZE
                )
        if legend:
            if self._ax:
                self._ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), numpoints=1, prop={'size': 5})

    def change_visible(self):
        self._visible = not self._visible
        if self._ax_whites:
            self._ax_whites.set_visible(self._visible)
        if self._ax_blacks:
            self._ax_blacks.set_visible(self._visible)
        if self._ax_cuts:
            self._ax_cuts.set_visible(self._visible)
        if self._ax_legend:
            self._ax_legend.set_visible(self._visible)
