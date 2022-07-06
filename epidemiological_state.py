# library imports
from enum import IntEnum

# project imports


class EpidemiologicalState(IntEnum):
    """
    Just to have fun
    """
    S = 0
    E = 1
    I = 2
    R = 3
    D = 4
