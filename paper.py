# library imports
import os
import json
import random
import numpy as np
import pandas as pd

# project imports
from sim import Simulator
from plotter import Plotter
from sim_generator import SimulatorGenerator
from pips.multi_aggressive_pip import PIPMultiAggressive
from walks.walk_social_distance import WalkSocialDistance
from find_optimal_iu_allocation import OptimalInspectionUnitsAllocation


class Paper:
    """
    All the plots that goes to the results section in the paper
    """

    # CONSTS #
    MINI_REPEAT = 50
    SAMLL_REPEAT = 100
    LARGE_REPEAT = SAMLL_REPEAT * 10
    DEFAULT_POPULATION_SIZE = 1000

    PAPER_PLOTS_FOLDER = "paper_results"
    PAPER_PLOTS_PATH = os.path.join(os.path.dirname(__file__), PAPER_PLOTS_FOLDER)

    # END - CONSTS #

    def __init__(self):
        pass

    @staticmethod
    def run_all():
        # just technical method to make sure the needed folders are exciting
        Paper.io_prepare()

        # Printing the sensitivity analysis of five tests which is figure 3 in the paper
        Paper.figure_3()

        # Printing the baseline SEIRD run which is figure 4 in the paper
        Paper.figure_4()

        # Printing the IU allocation options (random and optimal) which is figure 5 in the paper
        Paper.figure_5()

        # Printing the PIP comparison analysis which is figure 6 in the paper
        Paper.figure_6()

        # the appendix graph of the real-world topology
        Paper.appendix()

    @staticmethod
    def io_prepare():
        try:
            os.mkdir(Paper.PAPER_PLOTS_PATH)
        except:
            pass

    @staticmethod
    def figure_3():
        print("Working on Paper.figure_3")
        parameter_list = ["iu_coverage",
                          "graph_density",
                          "population_density",
                          "population_mobility",
                          "iu_performance"]
        cols = {"iu_coverage": [0.1 * i for i in range(11)],
                "graph_density": [0.05 * i for i in range(21)],
                "population_density": [0.5 * i for i in range(21)],
                "population_mobility": [0.1 * i for i in range(11)],
                "iu_performance": [0.05 * i for i in range(21)]}
        for metric_index, metric_name in enumerate(["r_zero", "max_infected"]):
            for index, parameter in enumerate(parameter_list):
                parameter_mean_row = []
                parameter_std_row = []
                for portion_index, portion in enumerate(cols[parameter]):
                    metric = []
                    for i in range(Paper.SAMLL_REPEAT):
                        print(
                            "Paper.figure_3: {} (#{}), {} (#{}), on portion {:.2f} (#{}) | iteration {}/{} ({:.2f}%)".format(
                                metric_name, metric_index + 1, parameter, index + 1, portion, portion_index + 1, i + 1,
                                Paper.SAMLL_REPEAT, 100 * (i + 1) / Paper.SAMLL_REPEAT))
                        # create configuration for analysis
                        sim = None
                        if parameter == "iu_coverage":
                            sim = SimulatorGenerator.sensitivity_random(iu_coverage=portion)
                        elif parameter == "graph_density":
                            sim = SimulatorGenerator.sensitivity_random(graph_density=portion)
                        elif parameter == "population_density":
                            sim = SimulatorGenerator.sensitivity_random(population_density=portion)
                        elif parameter == "population_mobility":
                            sim = SimulatorGenerator.sensitivity_random(population_density=portion)
                        elif parameter == "iu_performance":
                            sim = SimulatorGenerator.sensitivity_random(find_probability=portion)
                        # Run simulator
                        sim.run()
                        # recall data
                        if metric_name == "r_zero":
                            metric.append(sim.mean_r_zero())
                        elif metric_name == "max_infected":
                            metric.append(sim.get_max_infected_portion())
                    # compute this place in the heatmap
                    parameter_mean_row.append(np.nanmean(metric, axis=0))
                    parameter_std_row.append(np.nanstd(metric, axis=0))
                # save raw game
                with open(os.path.join(Paper.PAPER_PLOTS_PATH, "sensitivity_{}_{}.json".format(metric_name, parameter)),
                          "w") as raw_file:
                    json.dump({"mean": [val for val in parameter_mean_row], "std": [val for val in parameter_std_row]},
                              raw_file,
                              indent=2)
                Plotter.sensitivity_line(x=cols[parameter],
                                         mean=parameter_mean_row,
                                         std=parameter_std_row,
                                         x_label="{}".format(parameter),
                                         y_label="{}".format(metric_name),
                                         save_path=os.path.join(Paper.PAPER_PLOTS_PATH,
                                                                "sensitivity_{}_{}.pdf".format(metric_name, parameter)))

    @staticmethod
    def figure_4():
        print("Working on Paper.figure_4")
        epi_dists = []
        for i in range(Paper.SAMLL_REPEAT):
            print("Paper.figure_4: working on {}/{} ({:.2f}%)".format(i + 1, Paper.SAMLL_REPEAT,
                                                                      100 * (i + 1) / Paper.SAMLL_REPEAT))
            # generate settings for the simulator
            sim = SimulatorGenerator.real_world(population_count=Paper.DEFAULT_POPULATION_SIZE,
                                                max_time=30)
            # Run simulator
            sim.run()
            # recall data
            epi_dists.append(np.asarray(sim.epi_dist) / sim.population.get_size())
        Plotter.multi_basic_sim_plots(epi_dists=epi_dists,
                                      save_path=os.path.join(Paper.PAPER_PLOTS_PATH, "mean_seird.pdf"))

    @staticmethod
    def figure_5():
        print("Working on Paper.figure_5")
        iu_coverages = [0, 0.1, 0.25, 0.5]
        for allocation_strategy in ["random", "optimal"]:
            print("Working on Paper.figure_5: allocation strategy = {}".format(allocation_strategy))
            for index, iu_coverage in enumerate(iu_coverages):
                print("Paper.figure_5: working on IU {}/{} ({:.2f}%)".format(index + 1, len(iu_coverages),
                                                                             100 * (index + 1) / len(iu_coverages)))
                epi_dists = []
                for i in range(Paper.SAMLL_REPEAT):
                    print("Paper.figure_5: inside IU #{}, working on {}/{} ({:.2f}%)".format(index + 1, i + 1,
                                                                                             Paper.SAMLL_REPEAT, 100 * (
                                                                                                         i + 1) / Paper.SAMLL_REPEAT))
                    # generate settings for the simulator
                    sim = SimulatorGenerator.real_world(population_count=Paper.DEFAULT_POPULATION_SIZE,
                                                        max_time=30)
                    # allocate CU to nodes
                    if allocation_strategy == "random":
                        sim.pip = PIPMultiAggressive(
                            control_node_ids=random.sample(population=list(range(sim.graph.get_size())),
                                                           k=round(sim.graph.get_size() * iu_coverage)),
                            found_exposed=False)
                    elif allocation_strategy == "optimal":
                        OptimalInspectionUnitsAllocation.simple_brute_force(sim=sim,
                                                                            iu_count=round(
                                                                                sim.graph.get_size() * iu_coverage))
                    # Run simulator
                    sim.run()
                    # recall data
                    epi_dists.append(np.asarray(sim.epi_dist) / sim.population.get_size())
                Plotter.multi_basic_sim_plots(epi_dists=epi_dists,
                                              save_path=os.path.join(Paper.PAPER_PLOTS_PATH,
                                                                     "mean_seird_with_iu_{}_percent_{}.pdf".format(
                                                                         iu_coverage * 100,
                                                                         allocation_strategy)))

    @staticmethod
    def figure_6():
        print("Working on Paper.figure_6")
        for metric_name in ["r_zero", "max_infected"]:
            pip_list = ["iu_random", "iu_optimal", "sd", "masks"]
            cols = [0.1 * i for i in range(11)]
            data_mean = []
            data_std = []
            for index, pip in enumerate(pip_list):
                pip_mean_row = []
                pip_std_row = []
                for portion_index, portion in enumerate(cols):
                    metric = []
                    for i in range(Paper.SAMLL_REPEAT):
                        print("Paper.figure_6: "
                              "working on pip = {} (#{}), on portion {:.1f} (#{}) "
                              "with iteration {}/{} ({:.2f}%)".format(pip, index + 1,
                                                                      portion, portion_index + 1,
                                                                      i + 1, Paper.SAMLL_REPEAT,
                                                                      100 * (i + 1) / Paper.SAMLL_REPEAT))
                        # generate settings for the simulator
                        sim = SimulatorGenerator.real_world(population_count=Paper.DEFAULT_POPULATION_SIZE,
                                                            max_time=30)
                        # allocate the right PIP to nodes
                        if pip == "iu_random":
                            sim.pip = PIPMultiAggressive(
                                control_node_ids=random.sample(population=list(range(sim.graph.get_size())),
                                                               k=round(sim.graph.get_size() * portion)),
                                found_exposed=False)
                        if pip == "iu_optimal":
                            OptimalInspectionUnitsAllocation.greedy_brute_force(iu_count=len(sim.pip.control_node_ids),
                                                                                sim=sim)
                        elif pip == "sd":
                            sim.walk_policy = WalkSocialDistance(obey_rate=portion)
                        else:  # elif pip == "masks"
                            [agent.put_mask() for agent in
                             sim.population.agents[:round(portion) * sim.population.get_size()]]
                        # Run simulator
                        sim.run()
                        # recall data
                        if metric_name == "r_zero":
                            metric.append(sim.mean_r_zero())
                        elif metric_name == "max_infected":
                            metric.append(sim.get_max_infected_portion())
                    # compute this place in the heatmap
                    pip_mean_row.append(np.nanmean(metric, axis=0))
                    pip_std_row.append(np.nanstd(metric, axis=0))
                # set all the row of this pip
                data_mean.append(pip_mean_row)
                data_std.append(pip_std_row)
            # plot mean and std heatmaps
            data_mean = pd.DataFrame(data=data_mean,
                                     index=pip_list,
                                     columns=["{:.1f}".format(0.1 * i) for i in range(11)])
            data_mean.to_csv(os.path.join(Paper.PAPER_PLOTS_PATH, "pip_compare_mean_{}.csv".format(metric_name)))
            Plotter.sensitivity_heatmap(data=data_mean,
                                        x_label="Portion of the nodes/population that obey the PIP",
                                        y_label="Pandemic intervention policy",
                                        save_path=os.path.join(Paper.PAPER_PLOTS_PATH,
                                                               "pip_compare_mean_{}.pdf".format(metric_name)))
            # plot mean and std heatmaps
            data_std = pd.DataFrame(data=data_std,
                                    index=pip_list,
                                    columns=["{:.1f}".format(0.1 * i) for i in range(11)])
            data_std.to_csv(os.path.join(Paper.PAPER_PLOTS_PATH, "pip_compare_std_{}.csv".format(metric_name)))
            Plotter.sensitivity_heatmap(data=data_std,
                                        x_label="Portion of the nodes/population that obey the PIP",
                                        y_label="Pandemic intervention policy",
                                        save_path=os.path.join(Paper.PAPER_PLOTS_PATH,
                                                               "pip_compare_std_{}.pdf".format(metric_name)))

    @staticmethod
    def appendix():
        print("Working on Paper.appendix")
        sim = SimulatorGenerator.real_world(population_count=Paper.DEFAULT_POPULATION_SIZE,
                                            max_time=30)
        Plotter.show_graph(graph=sim.graph,
                           save_path=os.path.join(Paper.PAPER_PLOTS_PATH, "real_world_appendix_plot.pdf"))


if __name__ == '__main__':
    Paper.run_all()
