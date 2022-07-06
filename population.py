# library imports
import random

# project imports
from agent import Agent, EpidemiologicalState
from graph import Graph


class Population:
    """
    The population in the simulator
    """

    def __init__(self,
                 agents: list):
        self.agents = agents

    def get_size(self):
        return len(self.agents)

    # smart getters #

    def count_node(self,
                   node_id: int):
        return len([True for agent in self.agents if agent.location == node_id])

    # end - smart getters #

    # smart setters #

    # end - smart setters #

    # logic #

    # end - logic #

    @staticmethod
    def random(population_count: int,
               graph: Graph,
               infect_portion: float = 0.02):
        """
        Random amount of individuals, random states, random locations
        """
        graph_size = graph.get_size()
        answer = Population(agents=[Agent.create_random(graph_size=graph_size,) for _ in range(population_count)])
        [agent.set_e_state(EpidemiologicalState.I if random.random() < infect_portion else EpidemiologicalState.S) for agent in answer.agents]
        return answer

    def __hash__(self):
        return self.agents.__hash__()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<Population: size={}>".format(len(self.agents))
