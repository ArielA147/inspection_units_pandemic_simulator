# library imports
import random
import itertools
import numpy as np

# project imports
from node import Node
from edge import Edge


class Graph:
    """
    A simple graph object - implemented using a list of nodes with IDs and edges of these IDs
    """

    def __init__(self,
                 nodes: list,
                 edges: list):
        self.nodes = nodes
        self.edges = edges

    def get_size(self) -> int:
        return len(self.nodes)

    def next_nodes(self,
                   id: int):
        return [edge.t_id for edge in self.edges if edge.s_id == id]

    def next_nodes_with_weight(self,
                   id: int):
        ids = []
        ws = []
        for edge in self.edges:
            if edge.s_id == id:
                ids.append(edge.t_id)
                ws.append(edge.w)
        return ids, ws

    @staticmethod
    def generate_random(node_count: int,
                        edge_count: int):
        """
        Generate random graph with a given number of nodes and edges
        """
        nodes = [Node(id=i) for i in range(node_count)]
        edges = []
        while len(edges) < edge_count:
            s_id = random.randint(0, node_count-1)
            t_id = random.randint(0, node_count-1)
            if s_id != t_id and Edge(s_id=s_id, t_id=t_id, w=0) not in edges:
                edges.append(Edge(s_id=s_id, t_id=t_id, w=1))
        return Graph(nodes=nodes,
                     edges=edges)

    @staticmethod
    def fully_connected(node_count: int):
        """
        Generate a fully connected graph with a given number of nodes
        """
        nodes = [Node(id=i) for i in range(node_count)]
        edges = []
        for i in range(node_count):
            for j in range(node_count):
                if i != j:
                    edges.append(Edge(s_id=i, t_id=j, w=1))
        return Graph(nodes=nodes,
                     edges=edges)

    @staticmethod
    def table_to_edges(data: np.ndarray):
        edges = [[Edge(row_index, col_index, val)
                  for col_index, val in enumerate(row) if val > 0]
                 for row_index, row in enumerate(data)]
        return list(itertools.chain.from_iterable(edges))

    def copy(self):
        return Graph(nodes=[node.copy() for node in self.nodes],
                     edges=[edge.copy() for edge in self.edges])

    def __hash__(self):
        return (self.nodes, self.edges).__hash__()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<Graph: V={}, E={}>".format(len(self.nodes),
                                            len(self.edges))
