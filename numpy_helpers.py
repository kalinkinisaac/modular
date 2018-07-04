import numpy as np

def np_index(e, array):
    for i in range(len(array)):
        if np.array_equal(array[i], e):
            return i

    return -1

def np_count(e, array):
    c = 0
    for i in range(len(array)):
        if np.array_equal(array[i], e):
            c += 1

    return c

def inv(mat : np.matrix):
    a, b, c, d = np.array(mat).flatten().tolist()

    return (a*d - b*c)*np.matrix([[d, -b], [-c, a]], dtype=np.int)