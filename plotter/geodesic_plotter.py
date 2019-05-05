from matplotlib.patches import Arc
from fimath.geodesic import Geodesic
from math import (degrees, sqrt)
from cmath import phase
from .plotter import Plotter


class GeodesicPlotter(Plotter):

    Y_MAX_INF = 2.5

    def __init__(self, *args, **kwargs):
        super(__class__, self).__init__(*args, **kwargs)

    @staticmethod
    def bokeh_params(color='black', alpha=1, line_width=2, dashed=False):
        params = dict({'color': color, 'line_alpha': alpha, 'line_width': line_width})
        if dashed:
            params['line_dash'] = [6, 3]
        return params

    @staticmethod
    def mpl_params(color='black', alpha=1, line_width=2, dashed=False):
        params = dict({'color': color, 'alpha': alpha, 'line_width': line_width})
        if dashed:
            params['line_style'] = '--'
        return params

    def plot(self, geodesics, color='black', alpha=1, line_width=2, dashed=False):
        if type(geodesics) == list:
            for geodesic in geodesics:
                self._plot(geodesic, color=color, alpha=alpha, line_width=line_width, dashed=dashed)

        elif type(geodesics) == Geodesic:
                self._plot(geodesics, color=color, alpha=alpha, line_width=line_width, dashed=dashed)

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

    def _vertical_inf(self, geodesic: Geodesic, color, alpha, line_width, dashed):
        x = float(geodesic.vertical_x)
        y_min = self._y_min(geodesic),
        y_max = GeodesicPlotter.Y_MAX_INF

        if self._ax:
            self._ax.vlines(
                x=x,
                ymin=y_min,
                ymax=y_max,
                **self.mpl_params(color=color, alpha=alpha, line_width=line_width, dashed=dashed)
            )
        if self._bokeh_fig:
            self._bokeh_fig.ray(
                [x],
                [y_min],
                angle=[90],
                angle_units="deg",
                length=0,
                **self.bokeh_params(color=color, alpha=alpha, line_width=line_width, dashed=dashed)
            )

    def _vertical_not_inf(self, geodesic: Geodesic, color, alpha, line_width, dashed):
        x = float(geodesic.vertical_x)
        y_min = self._y_min(geodesic)
        y_max = self._y_max(geodesic)

        if self._ax:
            self._ax.vlines(
                x=x,
                ymin=y_min,
                ymax=y_max,
                **self.mpl_params(color=color, alpha=alpha, line_width=line_width, dashed=dashed)
            )

        if self._bokeh_fig:
            self._bokeh_fig.ray(
                [x],
                [y_min],
                angle=[90],
                angle_units="deg",
                length=y_max-y_min,
                **self.bokeh_params(color=color, alpha=alpha, line_width=line_width, dashed=dashed)
            )

    def _not_vertical(self, geo: Geodesic, color, alpha, line_width, dashed):
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
                **self.mpl_params(color=color, alpha=alpha, line_width=line_width, dashed=dashed)
            ))
        if self._bokeh_fig:
            self._bokeh_fig.arc(
                x=center,
                y=0,
                radius=radius,
                start_angle=theta1,
                end_angle=theta2,
                **self.bokeh_params(color=color, alpha=alpha, line_width=line_width, dashed=dashed)
            )

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
