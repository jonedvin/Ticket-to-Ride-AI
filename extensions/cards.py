from extensions.graph import Node


class Ticket():
    def __init__(self, start_node: Node, end_node: Node, points: int):
        self.start_node = start_node
        self.end_node = end_node
        self.points = points