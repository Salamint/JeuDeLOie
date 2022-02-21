"""
Ce fichier contient toutes les définitions de fonctions et de classe,
ainsi que les déclarations de variables en rapport avec l'élément 'oie'.
"""

# Import de 'common.py'
from common import *

# Import d'autres fichiers
import board
import player


# Définition des classes

class Goose(pygame.sprite.Sprite, Savable):
    """
    Classe représentant l'oie que contrôle le joueur.
    """

    def __init__(self, player_: 'player.Player', color: list or tuple):
        """
        Construit une nouvelle instance de la classe Goose représentant une oie.
        Une oie est associée à un joueur, possède une couleur, une position et d'autres attributs.
        Elle est aussi un sprite (possède donc un rectangle et une image) ainsi que des booléens
        renseignant sur ses animations.
        """
        # Appelle le constructeur de la superclasse
        super().__init__()

        # Le joueur associé à l'oie
        self.player = player_

        # Définit la couleur de l'oie
        self.color = color

        # Image de l'oie
        self.image = pygame.image.load("assets/goose.png").convert_alpha()
        self.change_color(self.color, (255, 255, 255))

        # Rectangle de l'oie
        self.rect = self.image.get_rect()
        self.rect.x = board.Tile.WIDTH
        self.rect.y = 0

        # Attributs relatifs à la position de l'oie
        self.position = 1
        self.last_position = 0
        self.finished = False

        # Attributs relatifs aux animations et à l'état de l'oie
        self.animating = False
        self.moving = False

    def __getstate__(self) -> dict: ...

    def __setstate__(self, state: dict): ...
    
    def able_to_move(self, position: int) -> bool:
        """
        Retourne un booléen précisant si l'oie est en capacité de se déplacer,
        ou plus génériquement, si elle est en capacité de réaliser une action
        qui demande de stopper l'animation en cours.
        """
        return not self.animating and not self.moving and 0 < position < self.player.game.board.size

    def change_color(self, new: str or tuple, old: str or tuple):
        """
        Remplace une couleur donnée de l'oie par une autre couleur donnée.
        Remplacer une couleur introuvable sur le bestiau ne causera aucune erreur.
        Les couleurs doivent être de type RGB ou RGBA, avec des valeurs comprises entre 0 et 255.
        Au-delà, une erreur est levée par pygame.
        """
        for x in range(self.image.get_width()):
            for y in range(self.image.get_height()):
                if self.image.get_at((x, y)) == old:
                    self.image.set_at((x, y), new)
    
    def go_to(self, position: int):
        """
        Déplace l'oie à une position donnée, si elle est atteignable.
        """
        if self.able_to_move(position):
            self.last_position = self.position
            self.position = position
            tile = self.player.game.board.tiles.get(self.position)
            tile.activate(self.position - self.last_position, self.player)
            return True
        return False
    
    def move_of(self, tiles: int) -> bool:
        """
        Fait avancer l'oie d'un certain nombre de cases.
        """
        return self.go_to(self.position + tiles)
    
    def update(self, event: pygame.event.Event):
        """
        Met à jour l'oie (placement).
        """

        # todo : supprimer et remplacer par les jetés de dés
        if event.type == pygame.KEYDOWN and self.player.stopped is False:
            if event.key == pygame.K_LEFT:
                self.move_of(-1)
            elif event.key == pygame.K_RIGHT:
                self.move_of(1)

        tile = self.player.game.board.tiles.get(self.position)
        self.rect.x = board.Tile.WIDTH * tile.x
        self.rect.y = board.Tile.HEIGHT * tile.y
