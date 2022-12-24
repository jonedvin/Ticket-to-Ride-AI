from extensions.player import Player
from extensions.maps import Map


class Game():
    def __init__(self, players: list[Player], map: Map):
        """ Class for representing a game. """
        self.players = players
        self.current_player = players[0]
        self.map = map

        # Keep track of who did what when, so we can go back in case of a misclick
        self.starting_player = self.current_player
        self.actions = []

    def __repr__(self):
        repr = f"Map: {self.map}"
        repr += "\nPlayers:"
        for player in self.players:
            repr += f"\n - {player}"
        return repr
