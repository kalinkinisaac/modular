import matplotlib.pyplot as plt

fig = plt.figure(num=2, figsize=(4, 3), dpi=240, facecolor='gray', edgecolor='k')
ax = fig.add_subplot(111)

ax.set_aspect('equal')
ax.set_axis_on()

# major_ticks = np.linspace(0, 1, 5)
# minor_ticks = np.linspace(0, 1, 9)
#
# ax.set_xticks(major_ticks)
# ax.set_xticks(minor_ticks, minor=True)
# ax.set_yticks(major_ticks)
# ax.set_yticks(minor_ticks, minor=True)
#
# #ax.grid(b=True, color='black', linestyle=':', linewidth = 0.5, which='both')
# ax.grid(which='minor', alpha=0.2)

ax.grid(alpha=0.5)

ax.set_xlim(-0.2, 3.8)
ax.set_ylim(-0.2, 1.5)
ax.autoscale(enable=True)

from .lines_drawer import draw_lines
