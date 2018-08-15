# Base class for mmath exceptions
class FimathException(Exception):
    pass

class NanError(FimathException):
    def __init__(self):
        super(__class__, self).__init__(f'Not-a-number.')