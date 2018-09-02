fig_config = dict({
    'figsize': (4, 3),
    'dpi': 240,
    'facecolor': 'gray',
    'edgecolor': 'k'
})


def ax_config(ax):
    ax.set_aspect('equal')
    ax.set_axis_on()
    ax.grid(alpha=0.5)
    ax.set_xlim(-0.2, 3.8)
    ax.set_ylim(-0.2, 1.5)
    ax.autoscale(enable=True)