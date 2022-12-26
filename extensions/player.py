from extensions.graph import Color, Node, Path
import random
import enum


class PlayerColor(enum.Enum):
    red = enum.auto()
    blue = enum.auto()
    green = enum.auto()
    yellow = enum.auto()
    black = enum.auto()


class Player():
    def __init__(self, name: str, color: PlayerColor, train_count: int):
        """ Class for representing a player. """
        self.name = name
        self.color = color
        self.train_count = train_count

        self.tickets = {}  # {Ticket, Path}
        self.hand = {}  # {Color, int}
        for color_ in Color:
            self.hand[color_] = 0
    
    def __repr__(self):
        return f"{self.name}, {self.color}, {self.train_count} trains left"



class AI(Player):
    def __init__(self, name: str, color: PlayerColor, train_count: int):
        """ CLass for the AI. """
        super().__init__(name, color, train_count)


    def draw_cards(self, count: int = 2):
        """ Adds count random cards to self.hand. """
        for _ in range(count):
            self.hand[Color(random.randint(1, len(Color)))] += 1


    def find_optimal_paths(self):
        """ Finds the combination of paths for each ticket that combine to the least used trains. """
        # Find all possible paths for all tickets
        possibilities = {}
        for ticket in self.tickets:
            found_paths = []
            self.find_all_possible_paths(ticket.start_node, ticket.end_node, found_paths=found_paths)
            possibilities[ticket] = [path for path in found_paths]

        # Find best combination
        for ticket, paths_list in possibilities.items():
            for path in paths_list:
                pass
        # NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE NOTE


    def find_all_possible_paths(self, start_node: Node, end_node: Node, found_paths: list[Path], current_path: Path = None):
        """
        Fills the found_paths list with all possible paths for player between start_node and end_nodes.
        """
        # Init paths
        if not current_path:
            current_path = Path(start_node)

        for edge in start_node.edges:

            # Can't cross edges bought by others
            if edge.bought_by:
                if edge.bought_by != self:
                    continue

            # Don't go in circles
            if edge.other_node in current_path.nodes:
                continue

            # Don't allow too long paths
            if current_path.length + edge.length > self.train_count:
                continue


            # Copy path and add edge
            expanded_path = Path.copy(current_path)
            expanded_path.add_edge(edge)

            # Add completed path or continue
            if edge.other_node == end_node:
                found_paths.append(expanded_path)
            else:
                self.find_all_possible_paths(expanded_path.last_node(), end_node, found_paths, expanded_path)
