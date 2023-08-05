from enum import Enum, unique


@unique
class Url(Enum):
    internal = '/internal'
    batch_result = f'{internal}/batch_result'
