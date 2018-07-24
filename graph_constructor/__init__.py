from .algorithm import GraphConstructor

def get_graph(gamma):
    gc = GraphConstructor(
        L=gamma.reprs,
        reduced=gamma.reduced,
        sort_key=gamma.sort_key,
        N=gamma.N)

    return gc.construct()

__all__ = ['get_graph', 'GraphConstructor']
