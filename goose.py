"""
Ce fichier contient toutes les définitions de fonctions et de classe,
ainsi que les déclarations de variables en rapport avec l'élément 'oie'.
"""

# Import de 'common.py'
from common import *

# Import d'autres fichiers
import board


# Définition des classes

class Goose(pygame.sprite.Sprite):
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
        for x in range(self.image.get_width()):
            for y in range(self.image.get_height()):
                if self.image.get_at((x, y)) == (255, 255, 255):
                    self.image.set_at((x, y), self.color)

        self.rect = self.image.get_rect()
        self.rect.x = 32
        self.rect.y = 32

        self.position = 0
        self.last_position = 0
        self.score = 0
    
    def goto(self, tile: int):
        """
        Déplace l'oie sur une case en particulier.
        """
        if 0 <= tile < self.player.game.board.size:
            self.last_position = self.position
            self.position = tile
    
    def move_back(self, tiles: int):
        """
        Fait reculer l'oie d'un certain nombre de case.
        """
        self.goto(self.position - tiles)
    
    def move_forward(self, tiles: int):
        """
        Fait avancer l'oie d'un certain nombre de cases.
        """
        self.goto(self.position + tiles)
    
    def update(self, event: pygame.event.Event):
        """
        Met à jour l'oie (placement).
        """
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.move_back(1)
            elif event.key == pygame.K_RIGHT:
                self.move_forward(1)
        
        self.update_rect()

    def update_rect(self):
        """
        Met à jour uniquement le rectangle de l'oie (placement), ces modifications sont assez nombreuses
        et spécifiques, elles ont donc été placés dans une méthode à part de la méthode update.
        """
        coordinates = self.player.game.board.get_at(self.position)
        width = board.Tile.WIDTH
        height = board.Tile.HEIGHT
        self.rect.x = width * coordinates[0]
        self.rect.y = height * coordinates[1]

        index = len(self.player.game.geese) - self.player.id
        self.rect.y -= 8 * index
