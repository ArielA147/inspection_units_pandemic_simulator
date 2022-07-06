# library imports
import os
import time
import random
import numpy as np

# project imports
from sim import Simulator
from plotter import Plotter
from multi_sim import MultiSim
from sim_generator import SimulatorGenerator
from walks.normalized_density import WalkNormalizedDensity
from pips.single_aggressive_pip import PIPSignleAggressive


class Main:
    """
    Single entry point of the project
    """

    RESULTS_FOLDER = os.path.join(os.path.dirname(__file__), "results")

    def __init__(self):
        pass

    @staticmethod
    def run():
        """
        Run all the experiments one after the other
        """
        Main.io_prepare()
        Main.simple_seird()
        Main.run_random()
        Main.fully_controlled()
        Main.run_random_single_aggressive_pip()
        Main.max_infected_over_edge_count()
        Main.mean_r_zero_over_aggressive_pip()

    @staticmethod
    def simple_seird():
        """
        The simplest case - single node, the population well-mixed
        """
        print("Main.simple_seird: running")
        sim = SimulatorGenerator.simple_random(node_count=1,
                                               edge_count=0,
                                               max_time=200,
                                               population_count=1000)
        sim.run()
        Plotter.basic_sim_plots(sim=sim,
                                save_path=os.path.join(Main.RESULTS_FOLDER, "simple_seird.png"))

    @staticmethod
    def run_random():
        """
        Analyze random graph - the most simple case
        """
        print("Main.run_random: running")
        sim = SimulatorGenerator.simple_random()
        sim.run()
        Plotter.basic_sim_plots(sim=sim,
                                save_path=os.path.join(Main.RESULTS_FOLDER, "run_random.png"))

    @staticmethod
    def fully_controlled():
        """
        All the nodes in a fully connected are with control units (or less) - just a sanity check
        """
        # values
        node_count = 20
        max_time = 150
        population_count = 1000
        control_units = node_count
        print("Main.fully_controled: running random walk")
        sim = SimulatorGenerator.full_connected_aggressive_controled(node_count=node_count,
                                                                     max_time=max_time,
                                                                     population_count=population_count,
                                                                     control_units=control_units,
                                                                     found_exposed=False)
        sim.run()
        Plotter.basic_sim_plots(sim=sim,
                                save_path=os.path.join(Main.RESULTS_FOLDER, "fully_controlled_random_walk.png"))
        print("Main.fully_controled: running normalized density walk")
        sim = SimulatorGenerator.full_connected_aggressive_controled(node_count=node_count,
                                                                     max_time=max_time,
                                                                     population_count=population_count,
                                                                     control_units=control_units,
                                                                     found_exposed=False)
        sim.walk_policy = WalkNormalizedDensity()
        sim.run()
        Plotter.basic_sim_plots(sim=sim,
                                save_path=os.path.join(Main.RESULTS_FOLDER, "fully_controlled_normalized_density_walk.png"))

    @staticmethod
    def run_random_single_aggressive_pip():
        """
        Analyze random graph, this time with a single control unit that finds everyone PIP
        """
        print("Main.run_random_single_aggressive_pip: running")
        sim = SimulatorGenerator.simple_random()
        sim.pip = PIPSignleAggressive(random.randint(0, sim.graph.get_size() - 1))
        sim.run()
        Plotter.basic_sim_plots(sim=sim,
                                save_path=os.path.join(Main.RESULTS_FOLDER, "run_random_single_aggressive_pip.png"))

    @staticmethod
    def max_infected_over_edge_count():
        """
        Analyze random graph - the most simple case
        """
        # default values
        control_units = 0
        repeat_times = 10
        node_count = 20
        max_time = 100
        population_count = 100
        # prepare the stuff we store the answers in
        means = []
        stds = []
        labels = []
        for edge_count in range(round(node_count*node_count/5), node_count*node_count, round(node_count*node_count/5)):
            print("Main.run_multi_random: Working on {} edges case".format(edge_count))
            max_infected_values_random = MultiSim.run(sim_generator_function=SimulatorGenerator.simple_random,
                                                      sim_info_extraction_function=Simulator.get_max_infected_portion,
                                                      repeat_times=repeat_times,
                                                      node_count=node_count,
                                                      edge_count=edge_count,
                                                      max_time=max_time,
                                                      control_units=control_units,
                                                      population_count=population_count)
            means.append(np.mean(max_infected_values_random))
            stds.append(np.std(max_infected_values_random))
            labels.append("{}".format(edge_count))
        # run the fully connected as baseline to compare with
        print("Main.run_multi_random: Working on fully connected")
        max_infected_values_fully = MultiSim.run(sim_generator_function=SimulatorGenerator.full_connected,
                                                 sim_info_extraction_function=Simulator.get_max_infected_portion,
                                                 repeat_times=repeat_times,
                                                 node_count=node_count,
                                                 edge_count=node_count*node_count,
                                                 max_time=max_time,
                                                  control_units=control_units,
                                                 population_count=population_count)
        means.append(np.mean(max_infected_values_fully))
        stds.append(np.std(max_infected_values_fully))
        labels.append("{}".format(node_count*node_count))
        # plot results
        Plotter.compare_plot(x=labels,
                             y=means,
                             y_err=stds,
                             y_label="Max infected portion",
                             x_label="Edge count",
                             normalized=True,
                             save_path=os.path.join(Main.RESULTS_FOLDER, "max_infected_over_edge_count.png"))

    @staticmethod
    def mean_r_zero_over_aggressive_pip():
        """
        Analyze random graph - the most simple case
        """
        # default values
        repeat_times = 10
        node_count = 50
        max_time = 100
        population_count = 500
        # prepare the stuff we store the answers in
        means = []
        stds = []
        labels = []
        for control_units in range(0, node_count+1, round(node_count/10)):
            print("Main.max_infected_over_aggressive_pip: Working on {} control units".format(control_units))
            start = time.time()
            max_infected_values_random = MultiSim.run(sim_generator_function=SimulatorGenerator.simple_random_aggressive_controled,
                                                      sim_info_extraction_function=Simulator.mean_r_zero,
                                                      repeat_times=repeat_times,
                                                      node_count=node_count,
                                                      edge_count=round(node_count*node_count/10),
                                                      max_time=max_time,
                                                      control_units=control_units,
                                                      population_count=population_count)
            means.append(np.mean(max_infected_values_random))
            stds.append(np.std(max_infected_values_random))
            labels.append("{:.2f}".format(control_units/node_count))
            end = time.time()
            print("Main.max_infected_over_aggressive_pip: {} control units computed during {} seconds".format(control_units, end - start))
        # plot results
        Plotter.compare_plot(x=labels,
                             y=means,
                             y_err=stds,
                             y_label="$E[R_0]$",
                             x_label="Control units coverage",
                             normalized=False,
                             save_path=os.path.join(Main.RESULTS_FOLDER, "mean_r_zero_over_aggressive_pip.png"))

    @staticmethod
    def io_prepare():
        """
        Make sure we have all the IO stuff we need
        """
        try:
            os.mkdir(Main.RESULTS_FOLDER)
        except:
            pass


if __name__ == '__main__':
    Main.run()
