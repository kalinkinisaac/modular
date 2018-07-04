from matplotlib.patches import Arc
from special_polygon.geodesic import Geodesic
from . import ax

Y_MAX_INF = 5.0

def draw_lines(lines, *args, **kwargs):
    for line in lines:
        draw_geodesic(geodesic=Geodesic(line[0], line[1]), *args, **kwargs)


def draw_geodesic(geodesic=None, *args, **kwargs):

    if geodesic.is_vertical():
        if geodesic.has_inf():
            ax.vlines(x=geodesic.x(),
                           ymin=geodesic.y_min(),
                           ymax=Y_MAX_INF,
                           *args, **kwargs)
        else:
            ax.vlines(x=geodesic.x(),
                           ymin=geodesic.y_min(),
                           ymax=geodesic.y_max(),
                           *args, **kwargs)
    else:
        ax.add_patch(Arc(
            xy=(geodesic.center,0),
            width=2*geodesic.radius,
            height=2*geodesic.radius,
            theta1=geodesic.theta1,
            theta2=geodesic.theta2,
            *args, **kwargs
        ))
