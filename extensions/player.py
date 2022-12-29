from extensions.graph import Color, Node, Path, PathSet, Edge, TrackType
import random
import enum


class PlayerColor(enum.Enum):
    red = enum.auto()
    blue = enum.auto()
    green = enum.auto()
    yellow = enum.auto()
    black = enum.auto()


class LastAction(enum.Enum):
    drew_tickets = enum.auto()
    drew_cards = enum.auto()
    bought_route = enum.auto()


class Player():
    def __init__(self, name: str, color: PlayerColor, train_count: int):
        """ Class for representing a player. """
        self.name = name
        self.color = color
        self.train_count = train_count
    
    def __repr__(self):
        return f"{self.name}, {self.color}, {self.train_count} trains left"

    def buy_route(self, route: Edge):
        """ Buys the specified route. """
        # Check if they can buy tunnel
        if route.track_type == TrackType.tunnel:
            pass

        # Buy route
        route.bought_by = self
        self.train_count -= route.length

        # Display bought route
        pass



class AI(Player):
    MaxDepth = 20

    def __init__(self, name: str, color: PlayerColor, train_count: int):
        """ CLass for the AI. """
        super().__init__(name, color, train_count)

        self.tickets = []  # [Ticket]
        self.best_path_set = PathSet()
        self.hand = {}  # {Color, int}
        for color_ in Color:
            self.hand[color_] = 0

        self.last_action = None


    def draw_cards(self, count: int = 2):
        """ Adds count random cards to self.hand. """
        self.last_action = LastAction.drew_cards
        for _ in range(count):
            self.hand[Color(random.randint(1, len(Color)))] += 1

    
    def draw_tickets(self):
        """ Draws tickets and picks which ones to keep. """
        self.last_action = LastAction.drew_tickets
        pass


    def buy_route(self, route: Edge):
        """ Buys the specified route. """
        super().buy_route(route)

        # Take cards for route
        self.hand[Color.locomotive] -= route.locomotive_count
        self.hand[route.color] -= route.length - route.locomotive_count
        if self.hand[route.color] < 0:
            self.hand[Color.locomotive] -= abs(self.hand[route.color])
            self.hand[route.color] = 0


    def find_all_possible_paths(self, start_node: Node, end_node: Node, found_paths: list[Path], current_path: Path = None):
        """
        Fills the found_paths list with all possible paths for player between start_node and end_nodes.
        """
        print(current_path)
        # Init paths
        if not current_path:
            current_path = Path(start_node)

        for edge in start_node.edges:

            # Can't cross edges bought by others
            if edge.bought_by:
                if edge.bought_by != self:
                    continue

            # Don't go in circles
            if edge.other_node(start_node) in current_path.nodes:
                continue

            # Don't allow too long paths
            if current_path.length + edge.length > self.MaxDepth:
                continue


            # Copy path and add edge
            expanded_path = Path.copy(current_path)
            expanded_path.add_edge(edge)

            # Add completed path or continue
            if edge.other_node(start_node) == end_node:
                found_paths.append(expanded_path)
            else:
                self.find_all_possible_paths(expanded_path.last_node(), end_node, found_paths, expanded_path)

    
    def get_best_combination(self, possibilities: dict, path_set: PathSet):
        """ Recursively tests all combinations of possible routes, and saves the best one. """
        for path in possibilities[list(possibilities.keys())[len(path_set.paths)]]:
            extended_path_set = PathSet.copy_from(path_set)
            extended_path_set.add_path(path)

            # Don't contunie if it's already too expensive
            if self.best_path_set.trains_needed != 0:
                if extended_path_set.trains_needed >= self.best_path_set.trains_needed:
                    continue

            # Set as best if it's a full combination
            if len(extended_path_set.paths) == len(possibilities):
                self.best_path_set = extended_path_set
            else:
                self.get_best_combination(possibilities, extended_path_set)


    def find_optimal_path_set(self):
        """ Finds the combination of paths for each ticket that combine to the least used trains. """
        # Find all possible paths for all tickets
        possibilities = {}
        for ticket in self.tickets:
            found_paths = []
            self.find_all_possible_paths(ticket.start_node, ticket.end_node, found_paths=found_paths)
            possibilities[ticket] = [path for path in found_paths]

        # Find best combination
        self.best_path_set = PathSet()
        self.get_best_combination(possibilities, PathSet())


    def take_turn(self):
        """ AI finds it's best path set, and decides what to do in its turn. """
        # Get more tickets if we're out
        completed_all = True
        for ticket in self.tickets:
            if not ticket.is_completed:
                completed_all = False
                break
        if completed_all:
            self.draw_tickets()
            return

        # Find optimal routes
        self.find_optimal_path_set()

        # Try to buy a route
        for route in self.best_path_set.routes_included:
            # Route already bought?
            if route.bought_by:
                continue

            # Enough locomotives?
            if self.hand[Color.locomotive] < route.locomotive_count:
                continue

            # Enough other cards?
            extra_locomotives = self.hand[Color.locomotive] - route.locomotive_count
            if self.hand[route.color] + extra_locomotives < route.length - route.locomotive_count:
                continue

            # Have enough cards to buy route
            self.buy_route(route)
            return
    
        # Draw cards if we can't buy a route
        self.draw_cards()