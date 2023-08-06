from enum import unique, IntEnum

@unique
class ApiAuthorisationType(IntEnum):
    device_communication = 1
    third_party = 2