from .special_polygon import SpecialPolygon

def get_all(graph):
    sp = SpecialPolygon(graph)
    return sp.construct_polygon()

__all__ = ['SpecialPolygon', 'get_all']