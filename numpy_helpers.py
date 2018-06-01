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
