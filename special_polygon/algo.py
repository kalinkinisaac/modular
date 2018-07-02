import numpy as np

def inv(mat : np.matrix):
    a, b, c, d = np.array(mat).flatten().tolist()

    #if np.abs(a*d - b*c) != 1:
        #print(mat)
        #raise Exception('Determinant of the matrix is not equal to -1 or 1')


    return (a*d - b*c)*np.matrix([[d, -b], [-c, a]], dtype=np.int)