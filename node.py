# library imports

# project imports


class Node:
    """
    A node in the graph
    """

    def __init__(self,
                 id: int):
        self.id = id

    def copy(self):
        return Node(id=self.id)

    def __hash__(self):
        return self.id.__hash__()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<Node: {}>".format(self.id)
