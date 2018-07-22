# Base class for mmath exceptions
class MmathException(Exception):
    pass

class UnsupportedTypeError(MmathException):
    def __init__(self, other):
        super(__class__, self).__init__(f'Unsupported type for multiplication: {type(other)}.')

class NanError(MmathException):
    def __init__(self):
        super(__class__, self).__init__(f'Not-a-number.')