# library imports
import os

# project imports


class MultiSim:
    """
    Run the simulation for multiple times and save some results
    """

    RESULTS_FOLDER = os.path.join(os.path.dirname(__file__), "results")

    def __init__(self):
        pass

    @staticmethod
    def run(sim_generator_function,
            sim_info_extraction_function,
            repeat_times: int,
            node_count: int,
            edge_count: int,
            max_time: int,
            control_units: int,
            population_count: int):
        answer = []
        for _ in range(repeat_times):
            sim = sim_generator_function(node_count=node_count,
                                         edge_count=edge_count,
                                         max_time=max_time,
                                         control_units=control_units,
                                         population_count=population_count)
            sim.run()
            answer.append(sim_info_extraction_function(sim))
        return answer
