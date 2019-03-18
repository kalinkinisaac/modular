class ApiError(Exception):
    pass


class FormatError(ApiError):
    pass


class ValueRangeError(ApiError):
    pass
