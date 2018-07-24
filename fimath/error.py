# Base class for mmath exceptions
class FimathException(Exception):
    pass

class NotUnitDeterminant(FimathException):
    pass

class UnsupportedTypeError(FimathException):
    def __init__(self, other):
        super(__class__, self).__init__(f'Unsupported type for multiplication: {type(other)}.')

class NanError(FimathException):
    def __init__(self):
        super(__class__, self).__init__(f'Not-a-number.')