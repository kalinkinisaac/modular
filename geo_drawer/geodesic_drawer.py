from matplotlib import pyplot as plt
from matplotlib.patches import Arc
from fimath.geodesic import Geodesic
from math import (degrees, sqrt)
from cmath import phase
from mpl_canvas import PlotCanvas
from .config import fig_config, ax_config


class GeodesicDrawer(object):

    Y_MAX_INF = 2.5

    def __init__(self, ax):
        self._ax = ax

    # TODO: remove or make static
    def show(self):
        plt.show()

    def draw(self, geodesics, *args, **kwargs):
        if type(geodesics) == list:
            for geodesic in geodesics:
                self._plot(geodesic, *args, **kwargs)

        elif type(geodesics) == Geodesic:
                self._plot(geodesics, *args, **kwargs)

        else:
            raise TypeError('geodesic should be Geodesic or list instance')

    def _plot(self, geodesic: Geodesic, *args, **kwargs):
        if type(geodesic) != Geodesic:
            raise TypeError('geodesic should be Geodesic instance')

        if geodesic.is_vertical:
            if geodesic.has_inf:
                self._vertical_inf(geodesic, *args, **kwargs)
            else:
                self._vertical_not_inf(geodesic, *args, **kwargs)
        else:
            self._not_vertical(geodesic, *args, **kwargs)

    def _vertical_inf(self, geodesic: Geodesic, *args, **kwargs):
        self._ax.vlines(x=geodesic.vertical_x,
                        ymin=GeodesicDrawer._y_min(geodesic),
                        ymax=GeodesicDrawer.Y_MAX_INF,
                        *args, **kwargs)

    def _vertical_not_inf(self, geodesic: Geodesic, *args, **kwargs):
        self._ax.vlines(x=geodesic.vertical_x,
                        ymin=GeodesicDrawer._y_min(geodesic),
                        ymax=GeodesicDrawer._y_max(geodesic),
                        *args, **kwargs)

    def _not_vertical(self, geo: Geodesic, *args, **kwargs):
        theta1 = degrees(phase(geo.begin - geo.center))
        theta2 = degrees(phase(geo.end - geo.center))

        theta1, theta2 = min(theta1, theta2), max(theta1, theta2)

        center = float(geo.center)
        radius = sqrt(float(geo.sq_radius))

        self._ax.add_patch(Arc(
            xy=(center, 0),
            width=2*radius,
            height=2*radius,
            theta1=theta1,
            theta2=theta2,
            *args, **kwargs
        ))

    @staticmethod
    def _y_min(geodesic):
        if geodesic.has_inf:
            if geodesic.begin.is_inf:
                return float(geodesic.end.imag)
            else:
                return float(geodesic.begin.imag)
        else:
            approx_a = float(geodesic.begin.imag)
            approx_b = float(geodesic.end.imag)

            return min(approx_a, approx_b)

    @staticmethod
    def _y_max(geodesic):
        approx_a = float(geodesic.begin.imag)
        approx_b = float(geodesic.end.imag)

        return max(approx_a, approx_b)


class GeodesicCanvas(PlotCanvas):
    def __init__(self, parent=None, geodesics=None):
        super(__class__, self).__init__(parent=parent, **fig_config)
        self._geodesics = geodesics
        self.ax = self.figure.add_subplot(111)
        ax_config(self.ax)


    def cla(self):
        self.ax.clear()
        ax_config(self.ax)