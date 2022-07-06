# library imports
import os
import numpy as np
import pandas as pd
import seaborn as sns
import networkx as nx
import matplotlib.pyplot as plt

# project imports
from graph import Graph
from sim import Simulator


class Plotter:
    """
    A class to generate graphs from the simulation's data
    """

    DPI = 600
    COLORS = ["#34A853", "#FBBC05", "#EA4335", "#4285F4", "#111111"]
    STYLES = ["-o", "-s", "-^", "-P", "-D"]
    LABELS = ["S", "E", "I", "R", "D"]

    def __init__(self):
        pass

    @staticmethod
    def sensitivity_line(x: list,
                         mean: list,
                         std: list,
                         x_label: str,
                         y_label: str,
                         save_path: str):
        """
        sensitivity analysis of line plot
        """
        plt.errorbar(x=x,
                     y=mean,
                     yerr=std,
                     fmt="-o",
                     color="#4285F4",
                     ecolor="#0d5bdd",
                     linewidth=1,
                     elinewidth=1,
                     capsize=3)
        plt.ylabel(y_label, fontsize=16)
        plt.xlabel(x_label, fontsize=16)
        plt.xticks(x)
        plt.grid(alpha=0.2,
                 color="gray")
        ax = plt.gca()
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()

    @staticmethod
    def show_graph_connectivity(graph: Graph,
                                save_path: str,
                                bins_count: int = 50):
        """
        Plot the graph's social and epidemiological connectivity
        """
        plt.hist([len(graph.next_nodes(id=node.id)) for node in graph.nodes],
                 bins_count,
                 density=False,
                 facecolor='b', alpha=0.5)
        plt.xlabel('Connections')
        plt.ylabel('Count')
        plt.grid(alpha=0.2,
                 color="black")
        plt.legend()
        plt.tight_layout()
        plt.savefig(save_path, dpi=Plotter.DPI)
        plt.close()

    @staticmethod
    def show_graph(graph: Graph,
                   save_path: str):
        """
        Plot the graph as both social and epidemiological graphs
        """
        G = nx.DiGraph()
        [G.add_node(node.id) for node in graph.nodes]
        [G.add_edge(u_of_edge=edge.s_id, v_of_edge=edge.t_id) for edge in graph.edges if edge.s_id != edge.t_id]
        # Draw image
        nx.draw_kamada_kawai(G,
                             font_color='white',
                             node_color="black",
                             edge_color="blue",
                             with_labels=True)
        plt.savefig(save_path, dpi=Plotter.DPI)
        plt.close()

    @staticmethod
    def compare_plot(x: list,
                     y_list: list,
                     y_err_list: list,
                     label_list: list,
                     y_label: str,
                     x_label: str,
                     save_path: str,
                     normalized: bool = False):
        """
        Plot a compare bar figure
        """
        count = len(y_list)
        for y_index, y in enumerate(y_list):
            plt.bar([val + 0.8*y_index/count for val in range(len(x))],
                    y,
                    width=0.8/count,
                    label=label_list[y_index],
                    color=Plotter.COLORS[y_index])
            plt.errorbar([val + 0.8*y_index/count for val in range(len(x))],
                         y,
                         yerr=y_err_list[y_index],
                         fmt="-o",
                         linewidth=0,
                         elinewidth=1,
                         markersize=1,
                         capsize=4,
                         color="black",
                         ecolor="black")
        plt.ylabel(y_label, fontsize=16)
        plt.xlabel(x_label, fontsize=16)
        plt.xticks(range(len(x)), x, fontsize=12)
        ax = plt.gca()
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        if normalized:
            plt.ylim((0, 1))
        plt.grid(alpha=0.2,
                 axis="y",
                 color="black")
        plt.legend()
        plt.tight_layout()
        plt.savefig(save_path, dpi=Plotter.DPI)
        plt.close()

    @staticmethod
    def basic_sim_plots(sim: Simulator,
                        save_path: str):
        """
        Plot distribution over time of the epidemiological states
        """
        data = np.asarray(sim.epi_dist)
        for epi_state in range(len(data[0])):
            plt.plot(range(len(data)),
                     data[:, epi_state] / sim.population.get_size(),
                     Plotter.STYLES[epi_state],
                     color=Plotter.COLORS[epi_state],
                     label=Plotter.LABELS[epi_state],
                     markersize=4)
        plt.xlabel("Simulation step", fontsize=16)
        plt.ylabel("Epidemiological state distribution", fontsize=16)
        plt.yticks([0.1 * i for i in range(11)])
        plt.xlim((-1, sim.max_time + 1))
        plt.grid(alpha=0.2,
                 color="black")
        plt.legend()
        ax = plt.gca()
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        plt.tight_layout()
        plt.savefig(save_path, dpi=Plotter.DPI)
        plt.close()

    @staticmethod
    def multi_basic_sim_plots(epi_dists: list,
                              save_path: str):
        """
        Plot distribution over time of the epidemiological states for a number of simulations
        """
        data_array = np.asarray(epi_dists)
        mean_data = np.nanmean(data_array, axis=0)
        std_data = np.nanstd(data_array, axis=0)
        for epi_state in range(mean_data.shape[1]):
            plt.plot(range(len(mean_data)),
                     mean_data[:, epi_state],
                     Plotter.STYLES[epi_state],
                     color=Plotter.COLORS[epi_state],
                     label=Plotter.LABELS[epi_state],
                     markersize=4)
            plt.fill_between(x=range(len(mean_data)),
                             y1=mean_data[:, epi_state] + std_data[:, epi_state],
                             y2=mean_data[:, epi_state] - std_data[:, epi_state],
                             alpha=0.2,
                             color=Plotter.COLORS[epi_state])
        plt.xlabel("Simulation step", fontsize=16)
        plt.ylabel("Epidemiological state distribution", fontsize=16)
        plt.yticks([0.1 * i for i in range(11)])
        plt.xlim((-1, mean_data.shape[0]))
        plt.grid(alpha=0.2,
                 color="black")
        plt.legend()
        ax = plt.gca()
        ax.spines['right'].set_visible(False)
        ax.spines['top'].set_visible(False)
        plt.tight_layout()
        plt.savefig(save_path, dpi=Plotter.DPI)
        plt.close()

    @staticmethod
    def sensitivity_heatmap(data: pd.DataFrame,
                            x_label: str,
                            y_label: str,
                            save_path: str):
        """
        Plot heatmap of the given data
        """
        sns.heatmap(data, annot=False, cmap="coolwarm")
        plt.xlabel(x_label, fontsize=16)
        plt.ylabel(y_label, fontsize=16)
        plt.savefig(save_path, dpi=Plotter.DPI)
        plt.close()
