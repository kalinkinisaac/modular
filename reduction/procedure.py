from fimath.geodesic import Geodesic

def procedure(poly, invs, z, w):
    line = Geodesic(w, z)
    poly = cyclic_sorted(poly)



# O(n^2)
def get_cross_edges(polygon, line : Geodesic):
    edges = []
    for edge in polygon:
        if is_crossing(edge, line):
            edges.append(edge)
    return edges

# O(1)
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

# O(n*log(n))
def cyclic_sorted(geos):
    geo_list = geos2tuples(geos)
    transfer = tuples2dict(geo_list)

    sorted = []

    geo = geo_list[0]

    for _ in geos:
        sorted.append(geo)

        start, end = geo

        variants = transfer[end]
        next = variants[0] if variants[1] == start else variants[1]

        geo = (end, next)

    return tuples2geos(sorted)

def tuples2dict(tuples):
    transfer = dict()
    for l, r in tuples:
        if l not in transfer:
            transfer[l] = [r]
        else:
            transfer[l].append(r)
        if r not in transfer:
            transfer[r] = [l]
        else:
            transfer[r].append(l)
    return transfer

def geos2tuples(geos):
    tuples = []
    for geo in geos:
        tuples.append((geo.begin, geo.end))
    return tuples

def tuples2geos(tuples):
    geos = []
    for pair in tuples:
        geos.append(Geodesic(pair[0], pair[1]))
    return geos