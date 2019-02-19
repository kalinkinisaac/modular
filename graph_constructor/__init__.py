from .algorithm import GraphConstructor


def get_graph(gamma):
    gc = GraphConstructor(
        l=gamma.reprs,
        reduced=gamma.reduced,
        sort_key=gamma.sort_key,
        n=gamma.N)

    return gc.construct()


__all__ = ['get_graph', 'GraphConstructor']
