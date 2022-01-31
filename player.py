"""
"""

# Import de 'common.py'
from common import *

import goose


class Player(Savable):
    """
    Une classe représentant un joueur. Un joueur est en général plus qu'une simple oie,
    et contiendra des informations plus diverses, comme des statistiques ou l'adresse IPv4.
    """

    def __init__(self, game, identifier: int, color: list[int] or tuple[int]):
        self.game = game
        self.id = identifier
        self.goose = goose.Goose(self, color)
    
    def play(self): ...

    def __setstate__(self, state: dict):
        self.id = state['id']
        self.goose = state['goose']

    def __getstate__(self) -> dict:
        state = self.__dict__.copy()
        state.update(
            {
                'id': self.id,
                'goose': self.goose
            }
        )
        return state
