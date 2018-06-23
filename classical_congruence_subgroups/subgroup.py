from .gamma import Gamma
from numpy import dot
from numpy.linalg import inv

def subgroup_action(sub, group):

    # Generating set of orbit representatives
    reprs = []
    for h_j in sub.reprs:
        for x_i in group.reprs:
            reprs.append(dot(h_j, x_i))

    # Constructing reduction procedure for subgroup action
    def reduced(x):
        x_i = group.reduced(x)
        h = dot(x, inv(x_i))
        h_j = sub.reduced(h)

        return dot(h_j, x_i)

    return reprs, reduced
