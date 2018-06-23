from .gamma import Gamma
from .gamma_zero import GammaBottomZero
from .subgroup import subgroup_action
from .algo import gcd, inv_element
import numpy as np

def gamma_one_bot(N):
    # Generating set of orbit representatives
    # of action $\Gamma_1(N)$ on $\Gamma_0(N)$

    _reprs = []
    for a in range(1, N // 2):
        if gcd(a, N) == 1:
            _reprs.append(np.matrix([[a, 0], [0, inv_element(a, N)]]))
    # Constructing reduction procedure
    def _reduced(mat : np.matrix):
        a, b = mat.item(0, 0), mat.item(1, 1)
        return np.matrix([[a, 0], [0, b]])

    SubGammaOne = Gamma(N=N, reprs=_reprs, reduced=_reduced)

    reprs, reduced = subgroup_action(SubGammaOne, GammaBottomZero(N))

    return Gamma(N=N, reprs=reprs, reduced=reduced)