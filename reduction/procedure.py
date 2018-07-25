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
                return line2.left.real <= line1.x() <= line2.right.real

        else:
            return line1.left.real <= line2.x() <= line1.right.real
    else:
        if abs(line1.center - line2.center) > line1.radius + line2.radius:
            return False
        else:
            x_cross = 0.5 * (line1.center + line2.center +
                                 (line1.sq_radius - line2.sq_radius) / (line2.center - line1.center))

            if line1.left.real <= x_cross <= line1.right.real and line2.left.real <= x_cross <= line2.right.real:
                return True

            else:
                return False


