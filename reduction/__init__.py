from .procedure import Decomposer

def decompose(*args, **kwargs):
    dcp = Decomposer(*args, **kwargs)
    return dcp.decompose()

__all__ = ['Decomposer', 'decompose']
