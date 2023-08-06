from enum import unique, IntEnum

@unique
class DeviceCommunicationType(IntEnum):
    time_comm = 1
    bio_time_8 = 2