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


    def run(self, last_player = None):
        """ Main game loop, run recursively. """
        # Finish the game after the final round
        if last_player:
            if self.current_player == last_player:
                return

        # Stop loop if we reached the final round
        for player in self.players:
            if player.train_count <= 2:
                last_player = self.current_player


        # Player turn
        if type(self.current_player) == Player:
            pass
        
        # AI turn
        else:
            pass


        # Next turn
        self.current_player = self.players[self.players.index(self.current_player)+1]
        self.run(last_player)
