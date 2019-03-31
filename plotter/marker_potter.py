class MarkerPlotter(object):
    ALPHA = 0.75
    Z_ORDER = 10
    SIZE = 30

    def __init__(self, ax):
        self._ax = ax
        self.white_markers = None
        self.black_markers = None
        self.cut_markers = None
        self.legend = None
        self._visible = True

    def plot(self, white, black, cut, legend=False):

        if white:
            self.white_markers = self._ax.scatter(
                [p.real for p in white], [p.imag for p in white],
                marker='o',
                c='white',
                alpha=MarkerPlotter.ALPHA,
                edgecolors='black',
                zorder=MarkerPlotter.Z_ORDER,
                label='white vertices',
                s=MarkerPlotter.SIZE
            )
        if black:
            self.black_markers = self._ax.scatter(
                [p.real for p in black],
                [p.imag for p in black],
                marker='o',
                color='black',
                alpha=MarkerPlotter.ALPHA,
                edgecolors='black',
                zorder=MarkerPlotter.Z_ORDER,
                label='black vertices',
                s=MarkerPlotter.SIZE
            )
        if cut:
            self.cut_markers = self._ax.scatter(
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
        if legend:
            self._ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), numpoints=1, prop={'size': 5})

    def change_visible(self):
        self._visible = not self._visible
        if self.white_markers:
            self.white_markers.set_visible(self._visible)
        if self.black_markers:
            self.black_markers.set_visible(self._visible)
        if self.cut_markers:
            self.cut_markers.set_visible(self._visible)
        if self.legend:
            self.legend.set_visible(self._visible)
