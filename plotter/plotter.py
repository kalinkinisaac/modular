import abc
from bokeh.plotting import figure


class Plotter(abc.ABC):

    def __init__(self, ax=None, bokeh_fig: figure = None):
        if not ax and not bokeh_fig:
            raise ValueError('ax or bokeh_fig should be provided.')
        self._ax = ax
        self._bokeh_fig = bokeh_fig

    def plot(self, *args, **kwargs):
        raise NotImplementedError
