from enum import Enum, unique

@unique
class ErrorCode(int, Enum):
    GENERAL_1001_UNEXPECTED_ERROR = 1001
    GENERAL_1002_REQUEST_VALIDATION_FAILED = 1002
    GENERAL_1003_QUERY_PARAMS_VALIDATION_FAILED = 1003

    RESOURCE_2001_NOT_FOUND = 2001

class CurrencyEnum(str, Enum):
    TWD = 'TWD'
    JPY = 'JPY'
    USD = 'USD'