# library imports
import random

# project imports
from graph import Graph
from pips.pip import PIP
from population import Population
from epidemiological_state import EpidemiologicalState


class PIPSignleAggressive(PIP):
    """
    A PIP operation with only one node but get out all infected individuals
    """

    def __init__(self,
                 control_node_id: int,
                 find_probability: float = 0.95,
                 found_exposed: bool = False):
        PIP.__init__(self)
        self.control_node_id = control_node_id
        self.found_exposed = found_exposed
        self.find_probability = find_probability

    def run(self,
            graph: Graph,
            population: Population) -> Population:
        """
        All infected in a given node are taken away
        """
        for agent in population.agents:
            if (agent.location == self.control_node_id and agent.e_state == EpidemiologicalState.I and random.random() < self.find_probability) or (self.found_exposed and agent.location == self.control_node_id and agent.e_state == EpidemiologicalState.E and random.random() < self.find_probability):
                agent.location = graph.get_size()
            elif agent.location == graph.get_size() and agent.e_state not in [EpidemiologicalState.E, EpidemiologicalState.I]:
                agent.location = random.randint(0, graph.get_size()-1)
        return population

