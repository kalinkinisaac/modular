from enum import Enum

class VertexType(Enum):
    Black = 0
    White = 1
    @staticmethod
    def inverse(vertex_type):
        if vertex_type == VertexType.Black:
            return VertexType.White
        else:
            return VertexType.Black
