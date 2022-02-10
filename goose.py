"""
Ce fichier contient toutes les définitions de fonctions et de classe,
ainsi que les déclarations de variables en rapport avec l'élément 'oie'.
"""

# Import de 'common.py'
from common import *

# Import d'autres fichiers
import board


# Définition des classes

# todo: documentation
class Goose(pygame.sprite.Sprite, Savable):
    """
    Classe représentant l'oie que contrôle le joueur.
    """

    def __init__(self, player, color: list or tuple):
        """
        """
        super().__init__()

        self.player = player
        self.color = color

        self.image = pygame.image.load("assets/goose.png").convert_alpha()
        self.change_color(self.color, (255, 255, 255))

        self.rect = self.image.get_rect()
        self.rect.x = board.Tile.WIDTH
        self.rect.y = 0

        self.finished = False
        self.position = 1
        self.last_position = 0

    def __getstate__(self) -> dict:
        state = self.__dict__.copy()
        state.update(
            {
                'color': self.color,
                'position': self.position,
                'last_position': self.last_position
            }
        )
        return state

    def __setstate__(self, state: dict):
        self.__init__(None, state['color'])
        self.position = state['position']
        self.last_position = state['last_position']

    def change_color(self, new: str or tuple, old: str or tuple):
        """"""
        for x in range(self.image.get_width()):
            for y in range(self.image.get_height()):
                if self.image.get_at((x, y)) == old:
                    self.image.set_at((x, y), new)
    
    def goto(self, position: int) -> bool:
        """
        Déplace l'oie sur une case en particulier.
        """
        if 0 < position < self.player.game.board.size:
            self.last_position = self.position
            self.position = position
            return True
        return False
    
    def move_back(self, tiles: int) -> bool:
        """
        Fait reculer l'oie d'un certain nombre de case.
        """
        return self.goto(self.position - tiles)
    
    def move_forward(self, tiles: int) -> bool:
        """
        Fait avancer l'oie d'un certain nombre de cases.
        """
        return self.goto(self.position + tiles)
    
    def update(self, event: pygame.event.Event):
        """
        Met à jour l'oie (placement).
        """

        # todo : supprimer et remplacer par les jetés de dés
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.move_back(1)
            elif event.key == pygame.K_RIGHT:
                self.move_forward(1)

        tile = self.player.game.board.tiles.get(self.position)
        self.rect.x = board.Tile.WIDTH * tile.x
        self.rect.y = board.Tile.HEIGHT * tile.y
