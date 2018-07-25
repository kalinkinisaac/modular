from fimath.geodesic import Geodesic
def procedure(polygon, involutions, z, w):
    line = Geodesic(w, z)

# O(n^2)
def get_cross_edges(polygon, line : Geodesic):
    edges = []
    for edge in polygon:
        if is_crossing(edge, line):
            edges.append(edge)
    return edges

def is_crossing(line1 : Geodesic, line2 : Geodesic):
    if line1.is_vertical() or line2.is_vertical():
        if line1.is_vertical():
            if line2.is_vertical():
                return line1.x() == line2.x()
            else:
                return line2.left().real <= line1.x() <= line2.right().real

        else:
            return line1.left().real <= line2.x() <= line1.right().real
    else:
        if abs(line1.center - line2.center) > line1.radius + line2.radius:
            return False
        else:
            total_cross_x = 0.5 * (line1.center + line2.center +
                                 (line1.radius ** 2 - line2.radius ** 2) / (line2.center - line1.center))

            if complex(line1.left()).real <= total_cross_x <= complex(line1.right()).real and \
                    complex(line2.left()).real <= total_cross_x <= complex(line2.right()).real:
                return True
            else:
                return False


