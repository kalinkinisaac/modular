from .procedure import Decompositor

def decompose(*args, **kwargs):
    dcp = Decompositor(*args, **kwargs)
    return dcp.decompose()
