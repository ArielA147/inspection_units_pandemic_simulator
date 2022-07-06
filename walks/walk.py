# library imports

# project imports
from graph import Graph
from population import Population


class Walk:
    """
    An abstract class for the walk operation
    """

    def __init__(self):
        pass

    def run(self,
            population: Population,
            graph: Graph) -> Population:
        """
        Changes the locations of the individuals according to some logic
        """
        return population

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<Walk - abstract class>"
