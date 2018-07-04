from .special_polygon import SpecialPolygon

def get_all(graph):
    sp = SpecialPolygon(graph)
    return sp.construct_polygon()
