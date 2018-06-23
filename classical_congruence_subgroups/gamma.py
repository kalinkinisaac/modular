class Gamma(object):

    def __init__(self, N=2, reprs=None, reduced=None):
        self.N = N

        self.reprs = []

        if reprs:
            self.reprs = reprs
        else:
            self.gen_reprs()

        if reduced:
            self.reduced = reduced

        self.L = []
        self.cache = dict()



    def element_hash(self, mat):
        return repr(mat)

    def reduced(self, mat):
        if self.element_hash(mat) not in self.cache:
            self.cache[self.element_hash(mat)] = self.not_cached_reduced(mat)

        return self.cache[self.element_hash(mat)]

    def not_cached_reduced(self, mat):
        pass

    def gen_reprs(self):
        pass