"""
Ce fichier contient toutes les définitions de fonctions et de classe,
ainsi que les déclarations de variables en rapport avec l'élément 'oie'.
"""

# Import de 'common.py'
from common import *


# Définition des classes

class Goose(pygame.sprite.Sprite):
    """
    Classe représentant l'oie que contrôle le joueur.
    """

    def __init__(self, board, color: list or tuple):
        """"""
        self.board = board
        self.color = color
        self.image = pygame.image.load("assets/goose.png").convert_alpha()
        for x in range(self.image.get_width()):
            for y in range(self.image.get_height()):
                if self.image.get_at((x, y)) == (255, 255, 255):
                    self.image.set_at((x, y)) == self.color
        self.rect = self.image.get_rect()
