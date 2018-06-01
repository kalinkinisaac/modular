import numpy as np

def inv(matrix : np.matrix):
    a, b, c, d = list(map(int, [matrix.item(0, 0), matrix.item(0, 1), matrix.item(1, 0), matrix.item(1, 1)]))
    return (a*d-b*c)*np.matrix([[d, -b], [-c, a]], dtype=np.int)