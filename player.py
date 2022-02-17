"""
"""

# Import de 'common.py'
from common import *

# Imports d'autres fichiers
import actions
import game
import goose


# Définition des classes

class Player(Savable):
    """
    Une classe représentant un joueur. Un joueur est en général plus qu'une simple oie,
    et contiendra des informations plus diverses, comme des statistiques ou l'adresse IPv4.
    """

    def __init__(self, game: 'game.Game', identifier: int, color: list[int] or tuple[int]):
        self.game = game
        self.id = identifier
        self.effects: dict[str, 'actions.Action'] = {}
        self.stopped = False
        self.goose = goose.Goose(self, color)
    
    def move_of(self, distance: int):
        """
        Semblable à self.goose.move_of() mais fait reculer l'oie lorsqu'elle va trop loin.
        """

        # Si le joueur n'est pas stoppé et que la distance à parcourir n'est pas nulle
        if not self.stopped and distance != 0:
            
            # Avancer
            if not self.goose.move_of(distance):
                
                # Si il est impossible d'avancer, reculer
                self.goose.move_of(-distance)

    def update(self):
        """
        Met à jour le joueur. Ne nécessite aucun événement.
        """

        # Marque la distance à parcourir
        distance = 0

        # Parcours tous les dés du jeu
        for dice in self.game.dices:

            # Si le dé à été lancé durant le tour
            if dice.rolled:

                # Ajoute la valeur du dé  la distance et réinitialise l'état du dé
                distance += dice.get_value()
        
        # Fait avancer le joueur
        self.move_of(distance)

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
