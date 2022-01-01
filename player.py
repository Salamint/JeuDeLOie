"""
"""

# Import de 'common.py'
from common import *

import goose


class Player:
    """
    Une classe représentant un joueur. Un joueur est en général plus qu'une simple oie,
    et contiendra des informations plus diverses, comme des statistiques ou l'adresse IPv4.
    """

    def __init__(self, game, identifier: int, color: list[int] or tuple[int]):
        self.game = game
        self.id = identifier
        self.goose = goose.Goose(self, color)
    
    def play(self): ...
