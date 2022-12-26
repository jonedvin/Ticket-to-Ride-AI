import enum

class TrackType(enum.Enum):
    normal = enum.auto()
    tunnel = enum.auto()

class Color(enum.Enum):
    red = enum.auto()
    blue = enum.auto()
    green = enum.auto()
    yellow = enum.auto()
    orange = enum.auto()
    pink = enum.auto()
    white = enum.auto()
    black = enum.auto()
    grey = enum.auto()
    locomotive = enum.auto()


class Node():
    def __init__(self, name: str, add_to: list = None, x: int = None, y: int = None):
        """ Class for representing a node in a graph. Equivalent to a city in TtR. """
        self.name = name
        self.edges = []

        self.x = x
        self.y = y

        if type(add_to) == list:
            add_to.append(self)

    def __repr__(self):
        return self.name
    
    def add_edge(self, edge):
        """ Adds an edge to the node. """
        self.edges.append(edge)


class Edge():
    def __init__(self, end_nodes: list[Node], color: Color, length: int, locomotive_count: int = 0, track_type: TrackType = TrackType.normal):
        """ Class for representing an edge in a graph. Equivalent to a single path between two bordering cities. """
        self.end_nodes = end_nodes
        self.color = color
        self.length = length
        self.locomotive_count = locomotive_count
        self.track_type = track_type
        self.bought_by = None

        # Add edge to list of edges in each end node
        for node in self.end_nodes:
            node.add_edge(self)
    
    def buy(self, player):
        """ Registers that the edge has been bought by player. """
        self.bought_by = player

    def other_node(self, one_node: Node):
        """
        Returns the other node of the edge to the one provided.\n
        Returns None if edge doesn not connect to provided node.
        """
        if one_node not in self.end_nodes:
            return None

        for node in self.end_nodes:
            if node != one_node:
                return node


class Path():
    def __init__(self, start_node: Node):
        """ Class for representing a full path from start_node to an end node. """
        self.edges = list[Edge]
        self.nodes = list[Node]
        self.length = 0
        self.necessary_color_count = dict[Color: int]
        
        for color in Color:
            self.necessary_color_count[color] = 0
        self.nodes.append(start_node)


    @classmethod
    def copy(cls, original):
        """ Returns a copy of the original path. """
        self = cls()
        
        self.edges = [edge for edge in original.edges]
        self.nodes = [node for node in original.nodes]
        self.length = original.length

        return self


    def add_edge(self, edge: Edge):
        """ Adds an edge to the path. """
        # Add edge and length
        self.edges.append(edge)
        self.length += edge.length

        # Add new node
        for node in edge.end_nodes:
            if node != self.nodes[-1]:
                self.nodes.append(node)

        # Increase color count
        self.necessary_color_count[edge.color] += edge.length - edge.locomotive_count
        self.necessary_color_count[edge.locomotive_count] += edge.locomotive_count


    def last_node(self):
        """ Returns the last node included in the path. """
        return self.nodes[-1]
