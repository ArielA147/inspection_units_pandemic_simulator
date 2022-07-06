# library imports
import random

# project imports
from walks.walk import Walk
from graph import Graph
from population import Population
from epidemiological_state import EpidemiologicalState


class WalkRandom(Walk):
    """
    A population random walk
    """

    def __init__(self):
        Walk.__init__(self)

    def run(self,
            population: Population,
            graph: Graph) -> Population:
        """
        Changes the locations of the individuals according to some logic
        """
        for agent in population.agents:
            if agent.e_state != EpidemiologicalState.D:
                possible_locations, weights = graph.next_nodes_with_weight(id=agent.location)
                if len(possible_locations) > 0:
                    picked_location = random.choices(possible_locations, weights)[0]
                    agent.location = picked_location
        return population

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<WalkRandom>"
