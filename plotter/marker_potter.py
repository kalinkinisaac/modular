import matplotlib.lines as mlines


class MarkerPlotter(object):
    ALPHA = 0.75
    Z_ORDER = 10
    SIZE = 30

    def __init__(self, ax):
        self._ax = ax

    def plot(self, white, black, cut):

        if white:
            self._ax.scatter(
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
            self._ax.scatter(
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
            self._ax.scatter(
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

        self._ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), numpoints=1, prop={'size': 5})
