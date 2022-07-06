# library imports
import math
import random
import numpy as np

# project imports
from graph import Graph
from pips.pip import PIP
from walks.walk import Walk
from population import Population
from seird_parms import SEIRDparameter
from epidemiological_state import EpidemiologicalState


class Simulator:
    """
    The main class of the project - the simulator
    """

    def __init__(self,
                 population: Population,
                 graph: Graph,
                 walk_policy: Walk,
                 pip: PIP,
                 max_time: int):
        # sim settings
        self.population = population
        self.graph = graph
        self.walk_policy = walk_policy
        self.pip = pip

        # technical
        self.max_time = max_time

        # operation
        self.step = 0

        # later analysis
        self.epi_dist = []

    # logic #

    def run(self):
        while self.step <= self.max_time:
            # edge case
            if self.step > 0 and self.epi_dist[-1][int(EpidemiologicalState.I)] == 0:
                self.epi_dist.append(self.epi_dist[-1].copy())
                self.step += 1
            else:
                self.run_step()

    def run_step(self):
        """
        The main logic of the class, make a single
        """
        # split the population for nodes and run the epidemiological model
        agents_in_nodes = [[] for _ in range(self.graph.get_size()+1)]
        [agents_in_nodes[agent.location].append(agent) for agent in self.population.agents]
        # run SEIRD for each node
        [self.seird(node_pop=node_pop) if node_index < self.graph.get_size() else self.outside_seird(node_pop=node_pop)
         for node_index, node_pop in enumerate(agents_in_nodes)]
        # walk the population
        self.population = self.walk_policy.run(population=self.population,
                                               graph=self.graph)
        # PIP the population
        self.population = self.pip.run(population=self.population, graph=self.graph)
        # recall state for later
        self.epi_dist.append(self.gather_epi_state())
        # count this step
        self.step += 1

    def outside_seird(self,
                      node_pop: list):
        """
        Run a single SEIRD step but for agents outside the graph so not infection can happen
        """
        for agent in node_pop:
            # clock tic
            agent.tic()
            if agent.e_state == EpidemiologicalState.E and agent.timer >= SEIRDparameter.phi:
                agent.set_e_state(new_e_state=EpidemiologicalState.I)
            elif agent.e_state == EpidemiologicalState.I and agent.timer >= SEIRDparameter.gamma:
                agent.set_e_state(
                    new_e_state=EpidemiologicalState.D if random.random() < SEIRDparameter.psi else EpidemiologicalState.R)

    def seird(self,
              node_pop: list):
        """
        Run a single SEIRD step
        """
        # get population count
        s_count = 0
        i_count = 0
        i_mask = 0
        s_mask = 0
        for agent in node_pop:
            if agent.e_state == EpidemiologicalState.S:
                s_count += 1
                if agent.mask:
                    s_mask += 1
            if agent.e_state == EpidemiologicalState.I:
                i_count += 1
                if agent.mask:
                    i_mask += 1
        infect_count = math.ceil(SEIRDparameter.beta * s_count * i_count)
        infected_now = 0
        # reduce infection count due to masks
        s_mask_rate = (s_mask / s_count) * SEIRDparameter.s_mask_reduction if s_count > 0 else 0
        i_mask_rate = (i_mask / i_count) * SEIRDparameter.i_mask_reduction if i_count > 0 else 0
        infect_count *= (1 - s_mask_rate)
        infect_count *= (1 - i_mask_rate)
        infect_count = round(infect_count)
        # update e_state of each agent
        for agent in node_pop:
            # clock tic
            agent.tic()

            if agent.e_state == EpidemiologicalState.S and infected_now < infect_count:
                agent.set_e_state(new_e_state=EpidemiologicalState.E)
                infected_now += 1
            elif agent.e_state == EpidemiologicalState.E and agent.timer >= SEIRDparameter.phi:
                agent.set_e_state(new_e_state=EpidemiologicalState.I)
            elif agent.e_state == EpidemiologicalState.I and agent.timer >= SEIRDparameter.gamma:
                agent.set_e_state(
                    new_e_state=EpidemiologicalState.D if random.random() < SEIRDparameter.psi else EpidemiologicalState.R)

    def gather_epi_state(self):
        """
        add to memory the epi state
        """
        counters = [0 for i in range(5)]  # TODO: change magic number to the number of states in the epi model
        for agent in self.population.agents:
            counters[int(agent.e_state)] += 1
        return counters

    def get_loc_dist(self):
        """
        add to memory the epi state
        """
        counters = [0 for i in range(
            self.graph.get_size() + 1)]  # TODO: change magic number to the number of states in the epi model
        for agent in self.population.agents:
            counters[int(agent.location)] += 1
        return counters

    # end - logic #

    # analysis #

    def get_max_infected(self):
        return max([val[int(EpidemiologicalState.I)] for val in self.epi_dist])

    def mean_r_zero(self):
        return np.mean([(self.epi_dist[i + 1][int(EpidemiologicalState.I)] - self.epi_dist[i][
            int(EpidemiologicalState.I)]) / (self.epi_dist[i + 1][int(EpidemiologicalState.R)] - self.epi_dist[i][
            int(EpidemiologicalState.R)])
                        if (self.epi_dist[i + 1][int(EpidemiologicalState.R)] - self.epi_dist[i][
            int(EpidemiologicalState.R)]) else (
                    self.epi_dist[i + 1][int(EpidemiologicalState.I)] - self.epi_dist[i][int(EpidemiologicalState.I)])
                        for i in range(len(self.epi_dist) - 1)])

    def get_max_infected_portion(self):
        try:
            return self.get_max_infected() / self.population.get_size()
        except:
            return 1

    def mortality_rate(self):
        try:
            return self.epi_dist[-1][EpidemiologicalState.D] / self.population.get_size()
        except:
            return 0

    # end - analysis #

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<Sim: {}/{} ({:.2f}\%)>".format(self.step,
                                                self.max_time,
                                                100 * self.step / self.max_time)
