"""
Un fichier qui contient toutes les fonctions que peuvent utiliser les oies lorsqu'elles atterrissent
sur des cases spéciales.
"""

# Import de 'common.py'
from common import *

# Import d'autres fichiers
import player


# Définition des classes


class Action(abc.ABC):
    """
    Représente une action qu'un joueur peut activer en atterrissant sur une case spéciale.
    """

    def __init__(self, identifier: int, p: player.Player):
        """"""
        self.id = identifier
        self.player = p

    def activate(self):
        """
        Cette méthode est appelée lorsque le joueur vient d'arriver sur la case.
        Ceci est une méthode par défaut et ne lèvera pas d'erreur si elle n'est pas réécrite,
        même si elle est conçue pour.
        """
        pass

    def discard(self):
        """
        Cette méthode supprime l'action de la liste des effets du joueur.
        """


class Bridge(Action):
    """
    Permet de téléporter le joueur au pont suivant.
    """


class Dices(Action):
    """
    Permet au joueur de relancer les dés.
    """


class End(Action):
    """
    Met fin au jeu.
    """


class Goose(Action):
    """
    Permet à une oie d'avancer une deuxième fois du nombre de cases qu'elle a déjà parcouru.
    """


class Hotel(Action):
    """
    Fait passer son tour au joueur.
    """


class Jail(Action):
    """"""


class Maze(Action):
    """
    Le joueur recule de 12 cases.
    """


class Skull(Action):
    """
    Fait recommencer le joueur à 0.
    """


class Well(Action):
    """
    Le joueur doit attendre qu'un autre joueur prenne sa place.
    """


DEFAULTS = {
    'bridge': Bridge,
    'dices': Dices,
    'end': End,
    'goose': Goose,
    'hotel': Hotel,
    'jail': Jail,
    'maze': Maze,
    'skull': Skull,
    'well': Well
}
