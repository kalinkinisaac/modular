from fimath.geodesic import Geodesic

# Average Case : O(n), Amortized Worst Case: O(n^2)
def cyclic_sorted(geos):
    oriented = dict([((geo.begin, geo.end), geo) for geo in geos] + [((geo.end, geo.begin), geo) for geo in geos])
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



    oriented_sorted = []

    for geo in sorted:
        oriented_sorted.append(oriented[geo])

    return oriented_sorted

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