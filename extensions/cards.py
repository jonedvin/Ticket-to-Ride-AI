from extensions.graph import Node, Edge, Path


class Ticket():
    def __init__(self, start_node: Node, end_node: Node, points: int):
        self.start_node = start_node
        self.end_node = end_node
        self.points = points

        self.is_completed = False
        self.is_returning = False  # Used to return quickly in check_if_complete if route was found 

    def __repr__(self):
        completed = "X" if self.is_completed else "  "
        return f"{completed} {self.start_node} -> {self.end_node}, {self.points} points"
        
    def check_if_complete(self, player, start_node: Node = None, current_path: Path = None):
        """
        Looks though all given routes, and sees if they connect self.start_node and self.end_node.
        Sets self.is_completed to True if so.
        """
        # Init variables
        if not start_node:
            start_node = self.start_node
        if not current_path:
            current_path = Path(self.start_node)
            
        for edge in start_node.edges:

            # Return if we've found a path
            if self.is_returning:
                return

            # Can't cross edges not bought by player
            if not edge.bought_by:
                continue
            if edge.bought_by != player:
                continue

            # Don't go in circles
            if edge.other_node(start_node) in current_path.nodes:
                continue

            # Copy path and add edge
            expanded_path = Path.copy(current_path)
            expanded_path.add_edge(edge)

            # Add completed path or continue
            if edge.other_node(start_node) == self.end_node:
                self.is_completed = True
                self.is_returning = True
            else:
                self.check_if_complete(player, expanded_path.last_node(), expanded_path)
