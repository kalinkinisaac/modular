# Base class for GraphConstructor exceptions
class GraphConstructorError(Exception):
    pass

class ReprNotFoundError(GraphConstructorError):
    def __init__(self, mat):
        msg =  f'Matrix \n{mat}\ndoes not appear in the list of representatives.'
        super(__class__, self).__init__(msg)
