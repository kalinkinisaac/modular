import numpy as np

def inv(mat : np.matrix):
    a, b, c, d = np.array(mat).flatten().tolist()

    return (a*d - b*c)*np.matrix([[d, -b], [-c, a]], dtype=np.int)