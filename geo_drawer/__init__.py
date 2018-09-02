from .config import fig_config, ax_config
from .geodesic_drawer import GeodesicDrawer
from matplotlib import pyplot as plt


def draw_geodesics(geodesics, _show=True):
    fig = plt.figure(**fig_config)
    ax = fig.add_subplot(111)
    ax_config(ax)
    gd = GeodesicDrawer(geodesics)
    gd.draw()

    if _show:
        plt.show()


__all__ = ['draw_geodesics', 'GeodesicDrawer']

