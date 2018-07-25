from matplotlib.patches import Arc
from fimath.geodesic import Geodesic
from math import degrees
from cmath import phase

class GeodesicDrawer:

    PRECISION = 16
    Y_MAX_INF = 5.0
    ax = None

    def __init__(self, ax):
        self.ax = ax

    def plot(self, geodesics, *args, **kwargs):
        if type(geodesics) == list:
            for geodesic in geodesics:
                self._plot(geodesic, *args, **kwargs)

        elif type(geodesics) == Geodesic:
                self._plot(geodesics, *args, **kwargs)

        else:
            raise TypeError()

    def _plot(self, geodesic : Geodesic, *args, **kwargs):
        # Check if geodesic is vertical
        if geodesic.has_inf():
            self.vertical_inf(geodesic, *args, **kwargs)

        elif geodesic.a.real == geodesic.b.real:
            self.vertical_not_inf(geodesic, *args, **kwargs)

        else:
            self.not_vertical(geodesic, *args, **kwargs)


    def vertical_inf(self, geodesic : Geodesic,  *args, **kwargs):
        self.ax.vlines(x=geodesic.x(),
                  ymin=GeodesicDrawer.y_min(geodesic),
                  ymax=GeodesicDrawer.Y_MAX_INF,
                  *args, **kwargs)

    def vertical_not_inf(self, geodesic : Geodesic, *args, **kwargs):
        self.ax.vlines(x=geodesic.x(),
                  ymin=GeodesicDrawer.y_min(geodesic),
                  ymax=GeodesicDrawer.y_max(geodesic),
                  *args, **kwargs)

    def not_vertical(self, geo : Geodesic, *args, **kwargs):
        theta1 = degrees(phase(complex(geo.a - geo.center)))
        theta2 = degrees(phase(complex(geo.b - geo.center)))

        theta1, theta2 = min(theta1, theta2), max(theta1, theta2)

        center = float(geo.center.approx(GeodesicDrawer.PRECISION))
        radius = float(geo.sq_radius.sqrt_approx(GeodesicDrawer.PRECISION))

        self.ax.add_patch(Arc(
            xy=(center,0),
            width=2*radius,
            height=2*radius,
            theta1=theta1,
            theta2=theta2,
            *args, **kwargs
        ))

    @classmethod
    def y_min(cls, geodesic):
        approx_a = geodesic.a.imag.approx(GeodesicDrawer.PRECISION)
        approx_b = geodesic.b.imag.approx(GeodesicDrawer.PRECISION)

        if geodesic.has_inf():
            if geodesic.a.is_inf:
                return approx_b
            else:
                return approx_a
        else:
            return min(approx_a, approx_b)

    @classmethod
    def y_max(cls, geodesic):
        approx_a = geodesic.a.imag.approx(GeodesicDrawer.PRECISION)
        approx_b = geodesic.b.imag.approx(GeodesicDrawer.PRECISION)

        return max(approx_a, approx_b)