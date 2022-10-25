# library imports
import random

# project imports
from graph import Graph
from pips.pip import PIP
from population import Population
from epidemiological_state import EpidemiologicalState


class PIPMultiAggressive(PIP):
    """
    A PIP operation with only one or more nodes that get out all infected individuals
    """

    def __init__(self,
                 control_node_ids: list,
                 find_probability: float = 0.95,
                 found_exposed: bool = False):
        PIP.__init__(self)
        self.control_node_ids = control_node_ids
        self.found_exposed = found_exposed
        self.find_probability = find_probability

    def run(self,
            graph: Graph,
            population: Population) -> Population:
        """
        All infected in a given node are taken away
        """
        for agent in population.agents:
            if (agent.location in self.control_node_ids and agent.e_state == EpidemiologicalState.I and random.random() < self.find_probability) or (self.found_exposed and agent.location in self.control_node_ids and agent.e_state == EpidemiologicalState.E  and random.random() < self.find_probability):
                agent.location = graph.get_size()
            elif agent.location == graph.get_size() and agent.e_state not in [EpidemiologicalState.E, EpidemiologicalState.I]:
                agent.location = random.randint(0, graph.get_size()-1)
        return population

