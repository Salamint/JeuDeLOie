"""
Ce fichier contient toutes les définitions de classe et de fonctions
en rapport avec le plateu de jeu.
"""

# Import de 'common.py'
from common import *


# Définition des classes

class Board(pygame.sprite.Group):
    """
    Une classe qui représente le plateau du jeu.
    """

    @staticmethod
    def from_file(file_name: str):
        """
        Crée un objet Board depuis un fichier JSON.
        """

        with open(file_name, "r") as file:
            file.close()
    
    @staticmethod
    def defaut(width, height):
        board = Board(
            pygame.Surface(Tile.get_size(width, height), pygame.SRCALPHA),
            (width, height)
        )
        for x in range(width):
            for y in range(height):
                board.add(Tile(board, "assets/tiles/tile.png", (x, y), lambda: print("action!")))
        return board
    
    def __init__(self, surface: pygame.Surface, size: tuple[int] or list[int]):
        """
        Construit un objet Board avec les tuiles du plateau en paramètre.
        `size`: Définit la taille du plateau de jeu, en donnant le nombre de tuile
        en hauteur et en largeur, et une tuile a une taillepar défaut de 128px par 128px.
        `tiles`: Les tuiles déjà chargés sont fournies en argument.
        """
        super().__init__()
        self.surface = surface
        self.width, self.height = size
    
    def display(self) -> pygame.Surface:
        """"""
        self.draw(self.surface)
        return self.surface


class Tile(pygame.sprite.Sprite):
    """
    Une classe qui représente une tuile du plateau.
    """

    WIDTH = 128
    HEIGHT = 128

    @staticmethod
    def get_size(width: int, height: int):
        """"""
        return width * Tile.WIDTH, height * Tile.HEIGHT

    def __init__(self, board: Board, image: str, position: tuple[int] or list[int], action: callable):
        super().__init__(board)

        self.action = action
        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = position[0] * Tile.WIDTH
        self.rect.y = position[1] * Tile.HEIGHT
