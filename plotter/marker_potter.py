import matplotlib as mpl

class MarkerPlotter(object):
    def __init__(self, ax):
        self._ax = ax

    def plot(self, white, black, cut):
        print(black)
        if white:
            self._ax.scatter([p.real for p in white], [p.imag for p in white], marker='o', color='gray')
        if black:
            self._ax.plot([p.real for p in black], [p.imag for p in black], marker='o', color='black')
        if cut:
            self._ax.plot([p.real for p in cut], [p.imag for p in cut], marker='x', color='black')