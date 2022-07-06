# library imports
import random

# project imports
from walks.walk import Walk
from graph import Graph
from population import Population
from epidemiological_state import EpidemiologicalState


class WalkNormalizedDensity(Walk):
    """
    A population walk to the locations with minimal number of agents
    """

    def __init__(self):
        Walk.__init__(self)

    def run(self,
            population: Population,
            graph: Graph) -> Population:
        """
        Changes the locations of the individuals according to some logic
        """
        # find agents in each place
        loc_counters = {id: 0 for id in range(graph.get_size())}
        for agent in population.agents:
            if agent.location != graph.get_size():
                loc_counters[agent.location] +=1
        # updat locations
        for agent in population.agents:
            if agent.e_state != EpidemiologicalState.D:
                possible_locations = graph.next_nodes(id=agent.location)
                possible_locations.append(agent.location)
                if len(possible_locations) > 1:
                    # count the amount if agents in each node
                    min_pop_count = population.get_size()+1
                    min_pop_id = graph.get_size()
                    for possible_location in possible_locations:
                        if loc_counters[possible_location] < min_pop_count:
                            min_pop_count = loc_counters[possible_location]
                            min_pop_id = possible_location
                    # update so people can go to the right location
                    loc_counters[min_pop_id] += 1
                    loc_counters[agent.location] -= 1
                    agent.location = min_pop_id
        return population

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<WalkNormalizedDensity>"
