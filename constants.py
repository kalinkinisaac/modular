import numpy as np

IDM = np.matrix([[1, 0], [0, 1]], dtype=np.int64)
G0 = np.matrix([[0, -1], [1, 0]], dtype=np.int64)
G1 = np.matrix([[0, 1], [-1, 1]], dtype=np.int64)
G1_2 = G1.dot(G1)

G0_ = np.matrix([[0, 1], [-1, 0]], dtype=np.int64)
G1_ = np.matrix([[1, 1], [-1, 0]], dtype=np.int64)
G1_2_ = G1_.dot(G1_)

G_ = np.matrix([[1, -1], [0, 1]], dtype=np.int64)
G__ = np.matrix([[1, 0], [-1, 1]], dtype=np.int64)

ZERO = 0
ONE = 1
INF = 1j*np.inf

V0 = 1j
V1 = np.exp(np.pi*1j/3)

