# library imports
import math
import random
import itertools
import numpy as np

# project imports
from graph import Graph
from sim import Simulator
from pips.pip import PIP
from walks.walk import Walk
from multi_sim import MultiSim
from population import Population
from seird_parms import SEIRDparameter
from epidemiological_state import EpidemiologicalState


class OptimalInspectionUnitsAllocation:
    """
    A brute-force approach to find the best IU allocation on a graph
    """

    def __init__(self):
        pass

    @staticmethod
    def simple_brute_force(sim: Simulator,
                           iu_count: int,
                           repeat_stochastic: int = 1):
        """
        Try (|IU| choose |N|) options (multiplied by Z - a number to reduce stochastic noise)
        """
        best_score = 100
        best_allocation = None
        for allocation in itertools.combinations(list(range(sim.graph.get_size())), iu_count):
            this_sim = sim.copy()
            this_sim.allocate_iu(allocation=allocation)
            allocations_scores = []
            for _ in range(repeat_stochastic):
                this_sim_runner = this_sim.copy()
                this_sim_runner.run()
                allocations_scores.append(this_sim_runner.mean_r_zero())
            score = np.mean(allocations_scores)
            if score < best_score:
                best_score = score
                best_allocation = allocation
        return best_allocation

    @staticmethod
    def greedy_brute_force(sim: Simulator,
                           iu_count: int,
                           repeat_stochastic: int = 1):
        """
        Try |IU| * |N| options (multiplied by Z - a number to reduce stochastic noise)
        """
        best_allocation = []
        this_sim = sim.copy()
        for allocation_index in range(iu_count):
            best_current_score = 100
            best_new_allocation = None
            for node_index in range(sim.graph.get_size()):
                if node_index in best_allocation:
                    continue
                this_allocation = best_allocation.copy()
                this_allocation.append(node_index)
                this_sim.allocate_iu(allocation=this_allocation)
                allocations_scores = []
                for _ in range(repeat_stochastic):
                    this_sim_runner = this_sim.copy()
                    this_sim_runner.run()
                    allocations_scores.append(this_sim_runner.mean_r_zero())
                score = np.mean(allocations_scores)
                if score < best_current_score:
                    best_current_score = score
                    best_new_allocation = node_index
            best_allocation.append(best_new_allocation)
        return best_allocation
