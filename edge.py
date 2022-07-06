# library imports

# project imports


class Edge:
    """
    A edge in the graph
    """

    def __init__(self,
                 s_id: int,
                 t_id: int,
                 w: int):
        self.s_id = s_id
        self.t_id = t_id
        self.w = w

    def __hash__(self):
        return (self.s_id, self.t_id).__hash__()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return "<Edge: {}->{}>".format(self.s_id,
                                       self.t_id)
