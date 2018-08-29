import enum

gui_names = dict({
    0: 'Gamma bot zero',
    1: 'Gamma top zero',
    2: 'Gamma top one',
    3: 'Gamma bot one',
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

    def __str__(self):
        return gui_names[self.value]


