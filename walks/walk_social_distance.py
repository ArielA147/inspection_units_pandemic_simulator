# library imports
import random

# project imports
from walks.walk import Walk
from graph import Graph
from population import Population
from epidemiological_state import EpidemiologicalState


class WalkSocialDistance(Walk):
    """
    A population random walk that allows to stay in the same node
    """

    def __init__(self,
                 obey_rate: float):
        Walk.__init__(self)
        self.obey_rate = obey_rate

    def run(self,
            population: Population,
            graph: Graph) -> Population:
        """
        Changes the locations of the individuals according to some logic
        """
        for agent in population.agents:
            if agent.e_state != EpidemiologicalState.D:
                if random.random() < self.obey_rate:
                    possible_locations = graph.next_nodes(id=agent.location)
                    possible_locations.append(agent.location)
                    best_node = 0
                    best_node_size = 0
                    for node_id in possible_locations:
                        size = population.count_node(node_id=node_id)
                        if best_node_size < size:
                            best_node = node_id
                            best_node_size = size
                    agent.location = best_node
                else:
                    possible_locations, weights = graph.next_nodes_with_weight(id=agent.location)
                    if len(possible_locations) > 0:
                        possible_locations.append(agent.location)
                        weights.append(1/len(weights))
                        picked_location = random.choice(possible_locations)
                        agent.location = picked_location
        return population

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<WalkSocialDistance>"
