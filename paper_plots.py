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


class PaperPlots:
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
        PaperPlots.io_prepare()
        """
        PaperPlots.real_world_appendix_graph()
        PaperPlots.baseline_seird()
        PaperPlots.baseline_cu_line()
        PaperPlots.pip_compare()
        PaperPlots.pip_bar_plots_all()
        """
        PaperPlots.sensitivity_analysis()

    @staticmethod
    def io_prepare():
        try:
            os.mkdir(PaperPlots.PAPER_PLOTS_PATH)
        except:
            pass

    @staticmethod
    def real_world_appendix_graph():
        print("Paperplot.real_world_appendix_graph")
        sim = SimulatorGenerator.real_world(population_count=PaperPlots.DEFAULT_POPULATION_SIZE,
                                            max_time=30)
        Plotter.show_graph(graph=sim.graph,
                           save_path=os.path.join(PaperPlots.PAPER_PLOTS_PATH, "real_wolrd_appendix_plot.pdf"))

    @staticmethod
    def baseline_seird():
        epi_dists = []
        for i in range(PaperPlots.SAMLL_REPEAT):
            print("PaperPlots.baseline_seird: working on {}/{} ({:.2f}%)".format(i+1, PaperPlots.SAMLL_REPEAT, 100*(i+1)/PaperPlots.SAMLL_REPEAT))
            # generate settings for the simulator
            sim = SimulatorGenerator.real_world(population_count=PaperPlots.DEFAULT_POPULATION_SIZE,
                                                max_time=30)
            # Run simulator
            sim.run()
            # recall data
            epi_dists.append(np.asarray(sim.epi_dist)/sim.population.get_size())
        Plotter.multi_basic_sim_plots(epi_dists=epi_dists,
                                      save_path=os.path.join(PaperPlots.PAPER_PLOTS_PATH, "mean_seird.pdf"))

    @staticmethod
    def baseline_cu_line():
        cu_counts = [0, 0.1, 0.25, 0.5]
        for index, cu_count in enumerate(cu_counts):
            print("PaperPlots.baseline_cu_line: working on cu {}/{} ({:.2f}%)".format(index+1, len(cu_counts), 100*(index+1)/len(cu_counts)))
            epi_dists = []
            for i in range(PaperPlots.SAMLL_REPEAT):
                print("PaperPlots.baseline_cu_line: inside cu #{}, working on {}/{} ({:.2f}%)".format(index+1, i + 1, PaperPlots.SAMLL_REPEAT, 100 * (i + 1) / PaperPlots.SAMLL_REPEAT))
                # generate settings for the simulator
                sim = SimulatorGenerator.real_world(population_count=PaperPlots.DEFAULT_POPULATION_SIZE,
                                                    max_time=30)
                # allocate CU to nodes
                sim.pip = PIPMultiAggressive(control_node_ids=random.sample(population=list(range(sim.graph.get_size())),
                                                                            k=round(sim.graph.get_size()*cu_count)),
                                             found_exposed=False)
                # Run simulator
                sim.run()
                # recall data
                epi_dists.append(np.asarray(sim.epi_dist)/sim.population.get_size())
            Plotter.multi_basic_sim_plots(epi_dists=epi_dists,
                                          save_path=os.path.join(PaperPlots.PAPER_PLOTS_PATH, "mean_seird_with_cu_{}_percent.pdf".format(cu_count*100)))

    @staticmethod
    def pip_compare():
        for metric_name in ["r_zero", "max_infected", "mortality_rate"]:
            pip_list = ["cu", "sd", "masks"]
            cols = [0.1*i for i in range(11)]
            data_mean = []
            data_std = []
            for index, pip in enumerate(pip_list):
                pip_mean_row = []
                pip_std_row = []
                for portion_index, portion in enumerate(cols):
                    metric = []
                    for i in range(PaperPlots.SAMLL_REPEAT):
                        print("PaperPlots.pip_compare: "
                              "working on pip = {} (#{}), on portion {:.1f} (#{}) "
                              "with iteration {}/{} ({:.2f}%)".format(pip, index+1,
                                                                      portion, portion_index+1,
                                                                      i + 1, PaperPlots.SAMLL_REPEAT, 100 * (i + 1) / PaperPlots.SAMLL_REPEAT))
                        # generate settings for the simulator
                        sim = SimulatorGenerator.real_world(population_count=PaperPlots.DEFAULT_POPULATION_SIZE,
                                                            max_time=30)
                        # allocate the right PIP to nodes
                        if pip == "cu":
                            sim.pip = PIPMultiAggressive(control_node_ids=random.sample(population=list(range(sim.graph.get_size())),
                                                                                        k=round(sim.graph.get_size()*portion)),
                                                         found_exposed=False)
                        elif pip == "sd":
                            sim.walk_policy = WalkSocialDistance(obey_rate=portion)
                        else:  # elif pip == "masks"
                            [agent.put_mask() for agent in sim.population.agents[:round(portion)*sim.population.get_size()]]
                        # Run simulator
                        sim.run()
                        # recall data
                        if metric_name == "r_zero":
                            metric.append(sim.mean_r_zero())
                        elif metric_name == "max_infected":
                            metric.append(sim.get_max_infected_portion())
                        else: # elif metric_name == "mortality_rate":
                            metric.append(sim.mortality_rate())
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
            data_mean.to_csv(os.path.join(PaperPlots.PAPER_PLOTS_PATH, "pip_compare_mean_{}.csv".format(metric_name)))
            Plotter.sensitivity_heatmap(data=data_mean,
                                        x_label="Portion of the nodes/population that obey the PIP",
                                        y_label="Pandemic intervention policy",
                                        save_path=os.path.join(PaperPlots.PAPER_PLOTS_PATH, "pip_compare_mean_{}.pdf".format(metric_name)))
            # plot mean and std heatmaps
            data_std = pd.DataFrame(data=data_std,
                                    index=pip_list,
                                    columns=["{:.1f}".format(0.1 * i) for i in range(11)])
            data_std.to_csv(os.path.join(PaperPlots.PAPER_PLOTS_PATH, "pip_compare_std_{}.csv".format(metric_name)))
            Plotter.sensitivity_heatmap(data=data_std,
                                        x_label="Portion of the nodes/population that obey the PIP",
                                        y_label="Pandemic intervention policy",
                                        save_path=os.path.join(PaperPlots.PAPER_PLOTS_PATH, "pip_compare_std_{}.pdf".format(metric_name)))

    @staticmethod
    def pip_bar_plots_all():
        PaperPlots.pip_bar_plots(mean_path=os.path.join(PaperPlots.PAPER_PLOTS_PATH, "pip_compare_mean_r_zero.csv"),
                                 std_path=os.path.join(PaperPlots.PAPER_PLOTS_PATH, "pip_compare_std_r_zero.csv"),
                                 y_name="r_zero",
                                 save_path=os.path.join(PaperPlots.PAPER_PLOTS_PATH, "pip_compare_bar_r_zero.pdf"))
        PaperPlots.pip_bar_plots(
            mean_path=os.path.join(PaperPlots.PAPER_PLOTS_PATH, "pip_compare_mean_max_infected.csv"),
            std_path=os.path.join(PaperPlots.PAPER_PLOTS_PATH, "pip_compare_std_max_infected.csv"),
            y_name="max_infected",
            save_path=os.path.join(PaperPlots.PAPER_PLOTS_PATH, "pip_compare_bar_max_infected.pdf"))
        PaperPlots.pip_bar_plots(
            mean_path=os.path.join(PaperPlots.PAPER_PLOTS_PATH, "pip_compare_mean_mortality_rate.csv"),
            std_path=os.path.join(PaperPlots.PAPER_PLOTS_PATH, "pip_compare_std_mortality_rate.csv"),
            y_name="mortality_rate",
            save_path=os.path.join(PaperPlots.PAPER_PLOTS_PATH, "pip_compare_bar_mortality_rate.pdf"))

    @staticmethod
    def pip_bar_plots(mean_path: str,
                      std_path: str,
                      save_path: str,
                      y_name: str):
        mean_data = pd.read_csv(mean_path)
        try:
            mean_data.set_index(['Unnamed: 0'], drop=1, inplace=True)
        except:
            pass
        std_data = pd.read_csv(std_path)
        try:
            std_data.set_index(['Unnamed: 0'], drop=1, inplace=True)
        except:
            pass
        Plotter.compare_plot(x=list(mean_data),
                             y_list=[row for row_index, row in mean_data.iterrows()],
                             y_err_list=[row for row_index, row in std_data.iterrows()],
                             label_list=list(mean_data.index),
                             x_label="Portion",
                             y_label=y_name,
                             save_path=save_path)

    @staticmethod
    def sensitivity_analysis():
        parameter_list = ["cu",
                          "graph_density",
                          "population_density",
                          "population_mobility"]
        cols = {"cu": [0.1 * i for i in range(11)],
                "graph_density": [0.05 * i for i in range(21)],
                "population_density": [0.5 * i for i in range(21)],
                "population_mobility": [0.1 * i for i in range(11)]}
        for metric_index, metric_name in enumerate(["r_zero", "max_infected", "mortality_rate"]):
            for index, parameter in enumerate(parameter_list):
                parameter_mean_row = []
                parameter_std_row = []
                for portion_index, portion in enumerate(cols[parameter]):
                    metric = []
                    for i in range(PaperPlots.SAMLL_REPEAT):
                        print("PaperPlots.sensitivity_analysis: {} (#{}), {} (#{}), on portion {:.2f} (#{}) | iteration {}/{} ({:.2f}%)".format(
                            metric_name, metric_index+1, parameter, index+1, portion, portion_index+1, i + 1, PaperPlots.SAMLL_REPEAT, 100 * (i + 1) / PaperPlots.SAMLL_REPEAT))
                        # create configuration for analysis
                        if parameter == "cu":
                            sim = SimulatorGenerator.sensativity_random(cu_portion=portion)
                        elif parameter == "graph_density":
                            sim = SimulatorGenerator.sensativity_random(graph_density=portion)
                        elif parameter == "population_density":
                            sim = SimulatorGenerator.sensativity_random(population_density=portion)
                        else:  # elif parameter == "population_mobility"
                            sim = SimulatorGenerator.sensativity_random(population_mobility=portion)
                        # Run simulator
                        sim.run()
                        # recall data
                        if metric_name == "r_zero":
                            metric.append(sim.mean_r_zero())
                        elif metric_name == "max_infected":
                            metric.append(sim.get_max_infected_portion())
                        else: # elif metric_name == "mortality_rate":
                            metric.append(sim.mortality_rate())
                    # compute this place in the heatmap
                    parameter_mean_row.append(np.nanmean(metric, axis=0))
                    parameter_std_row.append(np.nanstd(metric, axis=0))
                # save raw game
                with open(os.path.join(PaperPlots.PAPER_PLOTS_PATH, "sensativity_{}_{}.json".format(metric_name, parameter)), "w") as raw_file:
                    json.dump({"mean": [val for val in parameter_mean_row], "std": [val for val in parameter_std_row]},
                              raw_file,
                              indent=2)
                Plotter.sensitivity_line(x=cols[parameter],
                                         mean=parameter_mean_row,
                                         std=parameter_std_row,
                                         x_label="{}".format(parameter),
                                         y_label="{}".format(metric_name),
                                         save_path=os.path.join(PaperPlots.PAPER_PLOTS_PATH, "sensitivity_{}_{}.pdf".format(metric_name,parameter)))


if __name__ == '__main__':
    PaperPlots.run_all()
