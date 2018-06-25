class Gamma(object):

    def __init__(self, N=2, reduced=None):
        self.N = N

        if reduced:
            self.non_cached_reduced = reduced

        self.reprs = []
        self.cache = dict()



    def element_hash(self, mat):
        return repr(mat)

    def reduced(self, mat):
        mat = mat % self.N
        e_hash = self.element_hash(mat)
        if e_hash not in self.cache:
            self.cache[e_hash] = self.not_cached_reduced(mat)

        return self.cache[e_hash]

    def not_cached_reduced(self, mat):
        return 'not set reduction procedure'

    def gen_reprs(self):
        pass