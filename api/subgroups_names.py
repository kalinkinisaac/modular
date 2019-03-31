import enum
from subgroups import (GammaBotZero, GammaTopZero, GammaBotOne, GammaTopOne, Gamma)
gui_names = dict({
    0: 'Gamma_0 ',
    1: 'Gamma^0 ',
    2: 'Gamma^1 ',
    3: 'Gamma_1 ',
    4: 'Gamma'
})

gui_names.update({v: k for k, v in gui_names.items()})


class ClassicalSubgroups(enum.Enum):
    GammaBotZero = 0
    GammaTopZero = 1
    GammaBotOne = 2
    GammaTopOne = 3
    Gamma = 4

    @staticmethod
    def from_str(name):
        return ClassicalSubgroups(gui_names[name])

    @staticmethod
    def get_all_names():
        return list(map(str, ClassicalSubgroups))

    def to_class(self):
        if self is ClassicalSubgroups.GammaBotZero:
            return GammaBotZero
        elif self is ClassicalSubgroups.GammaTopZero:
            return GammaTopZero
        elif self is ClassicalSubgroups.GammaTopOne:
            return GammaTopOne
        elif self is ClassicalSubgroups.GammaBotOne:
            return GammaBotOne
        elif self is ClassicalSubgroups.Gamma:
            return Gamma

    def __str__(self):
        return gui_names[self.value]
