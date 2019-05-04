from matplotlib.patches import Arc
from fimath.geodesic import Geodesic
from math import (degrees, sqrt)
from cmath import phase
from .plotter import Plotter


class GeodesicPlotter(Plotter):

    Y_MAX_INF = 2.5

    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)

    def plot(self, geodesics, *args, **kwargs):
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
            pass
        else:
            self._not_vertical(geodesic, *args, **kwargs)

    def _vertical_inf(self, geodesic: Geodesic, *args, **kwargs):
        x = float(geodesic.vertical_x)
        y_min = self._y_min(geodesic),
        y_max = GeodesicPlotter.Y_MAX_INF

        if self._ax:
            self._ax.vlines(x=x, ymin=y_min, ymax=y_max, *args, **kwargs)
        if self._bokeh_fig:
            self._bokeh_fig.ray([x], [y_min], angle=[90], angle_units="deg", length=0)

    def _vertical_not_inf(self, geodesic: Geodesic, *args, **kwargs):
        x = float(geodesic.vertical_x)
        y_min = self._y_min(geodesic)
        y_max = self._y_max(geodesic)

        if self._ax:
            self._ax.vlines(x=x, ymin=y_min, ymax=y_max, *args, **kwargs)
        if self._bokeh_fig:
            self._bokeh_fig.ray([x], [y_min], angle=[90], angle_units="deg", length=y_max-y_min)

    def _not_vertical(self, geo: Geodesic, *args, **kwargs):
        theta1 = phase(geo.begin - geo.center)
        theta2 = phase(geo.end - geo.center)
        theta1, theta2 = min(theta1, theta2), max(theta1, theta2)
        theta1_deg = degrees(theta1)
        theta2_deg = degrees(theta2)

        center = float(geo.center)
        radius = sqrt(float(geo.sq_radius))

        if self._ax:
            self._ax.add_patch(Arc(
                xy=(center, 0),
                width=2*radius,
                height=2*radius,
                theta1=theta1_deg,
                theta2=theta2_deg,
                *args, **kwargs
            ))
        if self._bokeh_fig:
            self._bokeh_fig.arc(x=center, y=0, radius=radius, start_angle=theta1, end_angle=theta2)

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
