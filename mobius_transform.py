import numpy as np

# def geodesic_mt(pair, matrix):
#     a, b = pair
#     return [mobius_transform(a, matrix), mobius_transform(b, matrix)]
def geodesic_mt(pair, matrix):
     a, b = pair
     return [matrix * a, matrix * b]

def mobius_transform(z, matrix=np.eye(2)):
    a, b, c, d = matrix.reshape((1,4)).tolist()[0]
    if a*d == b*c:
        return a / c
    else:
        if c != 0:
            if z == -d / c:
                return 1j*np.inf
            elif np.isinf(z):
                return a / c

        if np.isinf(z):
            return 1j*np.inf

    return (a * z + b) / (c * z + d)
