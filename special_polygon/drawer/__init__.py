import matplotlib as mpl
import matplotlib.pyplot as plt
from .geodesics_drawer import PolygonDrawer
import numpy as np

fig = plt.figure(num=None, figsize=(4, 3), dpi=240, facecolor='gray', edgecolor='k')
ax = fig.add_subplot(111)

ax.set_aspect('equal')

#ax.spines['left'].set_position('zero')
# ax.spines['right'].set_color('none')
# ax.yaxis.tick_left()
# ax.spines['bottom'].set_position('zero')
# ax.spines['top'].set_color('none')
# ax.xaxis.tick_bottom()
# ax.set_frame_on(True)

major_ticks = np.linspace(0, 1, 5)
minor_ticks = np.linspace(0, 1, 9)

ax.set_xticks(major_ticks)
ax.set_xticks(minor_ticks, minor=True)
ax.set_yticks(major_ticks)
ax.set_yticks(minor_ticks, minor=True)

#ax.grid(b=True, color='black', linestyle=':', linewidth = 0.5, which='both')
ax.grid(which='minor', alpha=0.2)
ax.grid(which='major', alpha=0.5)


ax.set_xlim(-0.2, 3.8)
ax.set_ylim(-0.2, 1.5)

def draw_lines(polygon, *args, **kwargs):
    pd = PolygonDrawer(ax, polygon)
    pd.draw(*args, **kwargs)
    plt.show()
