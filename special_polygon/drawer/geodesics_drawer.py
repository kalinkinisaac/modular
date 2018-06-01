from matplotlib.patches import Arc
from special_polygon.geodesic import Geodesic

class PolygonDrawer(object):
    def __init__(self, ax, polygon):
        self.ax = ax
        self.gd = GeodesicDrawer(self.ax)
        self.polygon = polygon

    def draw(self, *args, **kwargs):
        for edge in self.polygon:
            self.gd.plot_geodesic(geodesic=Geodesic(edge[0], edge[1]), *args, **kwargs)

class GeodesicDrawer(object):
    Y_MAX_INF = 10.0
    def __init__(self, ax):
        self.ax = ax

    def plot_geodesic(self, geodesic=None, *args, **kwargs):

        if geodesic.is_vertical():
            if geodesic.has_inf():
                self.ax.vlines(x=geodesic.x(),
                               ymin=geodesic.y_min(),
                               ymax=GeodesicDrawer.Y_MAX_INF,
                               *args, **kwargs)
            else:
                self.ax.vlines(x=geodesic.x(),
                               ymin=geodesic.y_min(),
                               ymax=geodesic.y_max(),
                               *args, **kwargs)
        else:
            self.ax.add_patch(Arc(
                xy=(geodesic.center,0),
                width=2*geodesic.radius,
                height=2*geodesic.radius,
                theta1=geodesic.theta1,
                theta2=geodesic.theta2,
                *args, **kwargs
            ))
