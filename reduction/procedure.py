from geodesic import Geodesic
def procedure(polygon, involutions, z, w):
    line = Geodesic(w, z)

def get_cross_edge(polygon, line : Geodesic):
    pass

def cross_point(line1 : Geodesic, line2 : Geodesic):
    if line1.is_vertical() or line2.is_vertical():
        if line1.is_vertical():
            pass
        else:
            return
    else:
        if abs(line1.center - line2.center) > line1.radius + line2.radius:
            return False
        else:
            total_cross_x = 0.5 * (line1.center + line2.center +
                                 (line1.radius ** 2 - line2.radius ** 2) / (line2.center - line1.center))

            if complex(line1.left()).real < total_cross_x < complex(line1.right()).real and \
                    complex(line2.left()).real < total_cross_x < complex(line2.right()).real:
                return True
            else:
                return False


