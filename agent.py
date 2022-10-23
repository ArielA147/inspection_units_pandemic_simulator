# library imports
import random

# project imports
from epidemiological_state import EpidemiologicalState


class Agent:
    """
    An agent in the population
    """

    def __init__(self,
                 epidimiological_state: EpidemiologicalState,
                 location: int,
                 timer: int,
                 mask: bool = False):
        self.e_state = epidimiological_state
        self.location = location
        self.timer = timer
        self.mask = mask

    @staticmethod
    def create_random(graph_size: int):
        return Agent(epidimiological_state=random.choice([EpidemiologicalState.S,
                                                          EpidemiologicalState.E,
                                                          EpidemiologicalState.I,
                                                          EpidemiologicalState.R,
                                                          EpidemiologicalState.D]),
                     location=random.randint(0, graph_size-1),
                     timer=0,
                     mask=False)

    def tic(self):
        self.timer += 1

    def set_e_state(self,
                    new_e_state: EpidemiologicalState):
        self.e_state = new_e_state
        self.timer = 0

    def put_mask(self):
        self.mask = True

    def copy(self):
        return Agent(epidimiological_state=self.e_state,
                     location=self.location,
                     timer=self.timer,
                     mask=self.mask)

    def __hash__(self):
        return (self.e_state, self.location).__hash__()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<Agent: State={}, Location={}>".format(self.e_state,
                                                       self.location)

