from extensions.graph import Color, Node, Path, PathSet, Edge, TrackType
from extensions.cards import Ticket
from collections import OrderedDict
import random
import enum


class PlayerColor(enum.Enum):
    red = enum.auto()
    blue = enum.auto()
    green = enum.auto()
    yellow = enum.auto()
    black = enum.auto()


class LastAction(enum.Enum):
    drew_cards = enum.auto()
    bought_route = enum.auto()
    failed_tunnel = enum.auto()


colors_dict = {
    PlayerColor.red: "#b50505",
    PlayerColor.blue: "#031c96",
    PlayerColor.green: "#018347",
    PlayerColor.yellow: "#f5e905",
    PlayerColor.black: "#262626"
}


class Player():
    def __init__(self, name: str, color: PlayerColor, train_count: int):
        """ Class for representing a player. """
        self.name = name
        self.color = color
        self.train_count = train_count
        self.last_action = None
        self.bought_routes = []  # [Edge]
    
    def __repr__(self):
        return f"{self.name}, {self.color}, {self.train_count} trains left"

    @property
    def get_color(self):
        return colors_dict[self.color]



class AI(Player):
    MaxDepth = 21
    TicketTrainLimit = 8

    def __init__(self, name: str, color: PlayerColor, train_count: int):
        """ CLass for the AI. """
        super().__init__(name, color, train_count)
        
        self.gameplay_widget = None

        self.best_path_set = PathSet()
        self.best_path_set_temp = None

        self.tickets = []  # [Ticket]
        self.hand = {}  # {Color, int}
        for color_ in Color:
            self.hand[color_] = 0


    def set_gameplay_widget(self, widget):
        """ Sets the gameplay widget. Must be run before self.draw_tickets can be run. """
        self.gameplay_widget = widget


    def has_enough_cards(self, route: Edge, extra_count: int = 0):
        """ Returns True if AI has enough cards to buy the route, False if not. """
        # Enough locomotives?
        if self.hand[Color.locomotive] < route.locomotive_count:
            return False

        # Extra locomotives?
        extra_locomotives = self.hand[Color.locomotive] - route.locomotive_count

        # Grey is not actually a color
        if route.color == Color.grey:
            for color in Color:
                if self.hand[color] + extra_locomotives > route.length - route.locomotive_count + extra_count:
                    return True
            return False

        # Has enough cards?
        elif self.hand[route.color] + extra_locomotives < route.length - route.locomotive_count + extra_count:
                return False

        return True

    
    def can_buy_route(self, route: Edge):
        """ Returns True if route can be bought, False if not. """
        if route.bought_by:
            return False
        if self.train_count < route.length:
            return False
        if not self.has_enough_cards(route):
            return False
        return True



######## Draw cards functions ####################################################################################

    def draw_cards(self, count: int = 2):
        """ Adds count random cards to self.hand. """
        self.last_action = LastAction.drew_cards
        for _ in range(count):
            self.hand[Color(random.randint(1, len(Color)-1))] += 1


    def draw_tickets(self, max_tickets: int, min_tickets: int, blue_tickets: int = 0):
        """ Draws tickets and picks which ones to keep. """
        self.last_action = LastAction.drew_cards

        # Blue tickets
        for _ in range(blue_tickets):
            ticket = self.gameplay_widget.map.blue_tickets.pop(random.randint(0, len(self.gameplay_widget.map.blue_tickets)-1))
            self.tickets.append(ticket)
            self.find_optimal_path_set(possible_new_tickets=[ticket])
            self.best_path_set = PathSet.copy_from(self.best_path_set_temp)
            self.best_path_set_temp = None  # Avoid later confusion

        # Normal tickets
        for _ in range(min_tickets):

            # Get optimal paths for all tickets
            tickets_path_set_dict = {}
            for _ in range(max_tickets):
                ticket = self.gameplay_widget.map.tickets[random.randint(0, len(self.gameplay_widget.map.tickets)-1)]
                self.find_optimal_path_set(possible_new_tickets=[ticket])
                tickets_path_set_dict[ticket] = PathSet.copy_from(self.best_path_set_temp)
                self.best_path_set_temp = None  # Avoid later confusion

            # Get best one
            tickets_path_set_dict = OrderedDict(sorted(tickets_path_set_dict.items(), key=lambda item: item[1].additional_trains_needed))
            tickets_path_set_dict = OrderedDict(sorted(tickets_path_set_dict.items(), key=lambda item: item[0].points, reverse=True))
            best_ticket = next(iter(tickets_path_set_dict))
            best = (best_ticket, tickets_path_set_dict[best_ticket])

            # Remove taken ticket from list of tickets
            print(best[0])
            self.gameplay_widget.map.tickets.remove(best[0])
            
            # Take best found
            self.tickets.append(best[0])
            self.best_path_set = best[1]



######## Best path functions ####################################################################################

    def find_all_possible_paths(self, start_node: Node, end_node: Node, found_paths: list[Path], current_path: Path = None):
        """
        Fills the found_paths list with all possible paths for player between start_node and end_nodes.
        """
        # print(current_path)
        # Init paths
        if not current_path:
            current_path = Path(start_node)

        for edge in start_node.edges:

            # Can't cross edges bought by others
            already_bought = False
            if edge.bought_by:
                if edge.bought_by == self:
                    already_bought = True
                else:
                    continue

            # Don't go in circles
            if edge.other_node(start_node) in current_path.nodes:
                continue

            # Don't allow too long paths
            if current_path.length + edge.length > self.MaxDepth:
                continue


            # Copy path and add edge
            expanded_path = Path.copy(current_path)
            expanded_path.add_edge(edge, already_bought=already_bought)

            # Add completed path or continue
            if edge.other_node(start_node) == end_node:
                if expanded_path not in found_paths:
                    found_paths.append(expanded_path)
            else:
                self.find_all_possible_paths(expanded_path.last_node(), end_node, found_paths, expanded_path)

    
    def get_best_combination(self, possibilities: dict, path_set: PathSet, temp_save: bool = False):
        """ Recursively tests all combinations of possible routes, and saves the best one. """
        for path in possibilities[list(possibilities.keys())[len(path_set.paths)]]:
            extended_path_set = PathSet.copy_from(path_set)
            extended_path_set.add_path(path)

            # Don't contunie if it's already too expensive
            if (self.best_path_set.additional_trains_needed != 0 and
                extended_path_set.additional_trains_needed >= self.best_path_set.additional_trains_needed):
                continue

            # Continue looking if the path set is not complete
            if len(extended_path_set.paths) < len(possibilities):
                self.get_best_combination(possibilities, extended_path_set, temp_save=temp_save)
                continue

            # Save path set if it's complete and cheaper than prevous best
            if temp_save:
                self.best_path_set_temp = extended_path_set
            else:
                self.best_path_set = extended_path_set


    def find_optimal_path_set(self, possible_new_tickets: list[Ticket] = None):
        """ Finds the combination of paths for each ticket that combine to the least used trains. """
        # Find all possible paths for all tickets
        possibilities = {}
        for_loop_count = -1
        for ticket in self.tickets:
            for_loop_count += 1

            if ticket.is_completed:
                continue

            found_paths = []
            self.find_all_possible_paths(ticket.start_node, ticket.end_node, found_paths=found_paths)
            possibilities[ticket] = [path for path in found_paths]
            
            sorted_paths = sorted(found_paths, key = lambda path: path.length)
            print()
            print(ticket, for_loop_count)
            for path in sorted_paths:
                print(path)

        # Add possible ticket if given
        temp_save = False
        if possible_new_tickets:
            temp_save = True
            for ticket in possible_new_tickets:
                found_paths = []
                self.find_all_possible_paths(ticket.start_node, ticket.end_node, found_paths=found_paths)
                possibilities[ticket] = [path for path in found_paths]

        # Find best combination
        self.best_path_set = PathSet()
        self.get_best_combination(possibilities, PathSet(), temp_save=temp_save)



######## Gameplay functions ####################################################################################

    def take_turn(self, map):
        """
        AI finds it's best path set, and decides what to do in its turn.\n
        Returns the route to buy if it chooses to buy a route, None if not.
        """
        # Get more tickets if we're out
        completed_all_tickets = True
        for ticket in self.tickets:
            if not ticket.is_completed:
                completed_all_tickets = False
                break

        if completed_all_tickets: 
            # Buy another route if we have enough trains
            if self.train_count > self.TicketTrainLimit:
                self.draw_tickets(max_tickets=3, min_tickets=1)
                return
            
            # If we don't have enough trains for tickets, buy random routes for points
            else:
                for edge in map.edges:
                    if not self.can_buy_route(edge):
                        continue
                    self.last_action = LastAction.bought_route
                    return route
                
                # If we get here, there's nothing to do, so we draw cards
                self.draw_cards()

        # Find optimal routes
        self.find_optimal_path_set()

        # Try to buy a route
        for route in self.best_path_set.routes_included:
            if not self.can_buy_route(route):
                continue
            self.last_action = LastAction.bought_route
            return route
    
        # Draw cards if we can't buy a route
        self.draw_cards()