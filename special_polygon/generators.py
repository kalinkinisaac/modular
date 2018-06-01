from graph import (BCGraph, VertexType)
from . import SPolygon
from constants import *
from numpy.linalg import inv

def get_gen_from_poly(polygon : SPolygon):
    return get_generators_set(polygon.graph, polygon.matrices)

def get_generators_set(graph : BCGraph, matrices=[]):
    generators = []
    used = [False] *graph.size()

    for vertex in graph.get_leaves():
        color = graph.vertex_type(vertex)
        if not used[vertex]:
            h = matrices[vertex]
            used[vertex] = True

            if color == VertexType.White:
                generators.append(h.dot(G1).dot(inv(h)))
            elif graph.is_corresponded(vertex):
                    cor_vertex = graph.get_correspond(vertex)
                    used[cor_vertex] = True
                    generators.append(matrices[cor_vertex].dot(G0).dot(inv(h)))
            else:
                generators.append(h.dot(G0).dot(inv(h)))

    return generators

