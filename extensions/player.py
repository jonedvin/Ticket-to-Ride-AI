from extensions.graph import Color, Node, Route
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

        self.tickets = {}  # {Ticket, Route}
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


    def find_optimal_routes(self):
        """ Finds the combination of routes for each ticket that combine to the least used trains. """
        # Find all possible routes for all tickets
        possibilities = {}
        for ticket in self.tickets:
            found_routes = []
            self.find_all_possible_routes(ticket.start_node, ticket.end_node, found_routes=found_routes)
            possibilities[ticket] = [route for route in found_routes]

        # Find best combination
        for ticket, routes_list in possibilities.items():
            for route in routes_list:
                pass


    def find_all_possible_routes(self, start_node: Node, end_node: Node, found_routes: list[Route], current_route: Route = None):
        """
        Fills the found_routes list with all possible routes for player between start_node and end_nodes.
        """
        # Init routes
        if not current_route:
            current_route = Route(start_node)

        for edge in start_node.edges:

            # Can't cross edges bought by others
            if edge.bought_by:
                if edge.bought_by != self:
                    continue

            # Don't go in circles
            if edge.other_node in current_route.nodes:
                continue

            # Don't allow too long routes
            if current_route.length + edge.length > self.train_count:
                continue


            # Copy route and add edge
            expanded_route = Route.copy(current_route)
            expanded_route.add_edge(edge)

            # Add completed route or continue
            if edge.other_node == end_node:
                found_routes.append(expanded_route)
            else:
                self.find_all_possible_routes(expanded_route.last_node(), end_node, found_routes, expanded_route)
