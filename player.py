"""
Ce fichier contient la définition de la classe 'Player',
représentant un joueur.
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

    def __init__(self, game_: 'game.Game', identifier: int, color: list[int] or tuple[int]):
        """
        Construit une nouvelle instance de la classe 'Player' représentant un joueur.
        Un joueur est associé à un jeu, possède un identifiant correspondant à son indice dans le dictionnaire
        des joueurs du jeu, ainsi qu'une oie et des effets.
        """

        # Le jeu
        self.game = game_

        # L'identifiant
        self.id = identifier

        # Les effets du joueur
        self.effects: dict[str, 'actions.Action'] = {}

        # L'état du joueur (False lui permet de se mouvoir, et True non)
        self.stopped = False

        # L'oie du joueur
        self.goose = goose.Goose(self, color)

    def __getstate__(self) -> dict: ...

    def __setstate__(self, state: dict): ...
    
    def move_of(self, distance: int):
        """
        Semblable à self.goose.move_of() mais fait reculer l'oie lorsqu'elle va trop loin.
        """

        # Si le joueur n'est pas stoppé et que la distance à parcourir n'est pas nulle
        if not self.stopped and distance != 0:
            
            # Avancer
            if not self.goose.move_of(distance):
                
                # S'il est impossible d'avancer, reculer
                self.goose.move_of(-distance)

    def update(self):
        """
        Met à jour le joueur. Ne nécessite aucun événement.
        """

        # Marque la distance à parcourir
        distance = 0

        # Parcours tous les dés du jeu
        for dice in self.game.dices:

            # Si le dé a été lancé durant le tour
            if dice.rolled:

                # Ajoute la valeur du dé la distance et réinitialise l'état du dé
                distance += dice.get_value()
        
        # Fait avancer le joueur
        self.move_of(distance)
