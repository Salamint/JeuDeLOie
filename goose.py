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

    def __init__(self, player_: 'player.Player', color: str or list or tuple):
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

        # Stocke toutes les conditions
        conditions = (
            not self.animating,
            not self.moving,
            0 < position < self.player.game.board.size
        )

        # Vérifie que toutes les conditions sont vraies
        return all(conditions)

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

        # Permet de déterminer si le joueur a sauvé un autre joueur durant le calcul
        rescued = False
        # Permet de déterminer si le joueur a bougé
        moved = False

        # Si l'oie est capable de se déplacer sur la case à la position donnée
        if self.able_to_move(position):

            # Pour chaque joueur
            for player_ in self.player.game.players:

                # Si la position est déjà prise par un autre joueur
                if player_.goose.position == position:

                    # Pour chaque action du joueur
                    for action in player_.effects.values():

                        # Si l'action peut être désactivée par in autre joueur
                        if action.other_player_rescue:

                            # Envoyer des secours
                            action.rescue(self.player)
                            # Secourir le joueur
                            rescued = True

                    # Sauvegarde la dernière position du joueur
                    current_last_position = self.last_position

                    # Va à la dernière position du joueur
                    self.last_position = self.position
                    self.position = player_.goose.last_position

                    # Indique que le joueur s'est déplacé
                    moved = True

                    # Si le joueur à sauvé un autre joueur
                    if rescued:

                        # Déplacer le joueur sauvé à la dernière position
                        player_.goose.last_position = player_.goose.position
                        player_.goose.position = current_last_position

                    # Stoppe la boucle, il est inutile de continuer, il ne peut y avoir plus d'un joueur par case
                    break

            # Si le joueur ne s'est pas encore déplacé
            if not moved:

                # Sinon, va à la position de la case
                self.last_position = self.position
                self.position = position

            # Si le joueur n'a sauvé personne
            if not rescued:
                # Récupère la case et l'active
                tile = self.player.game.board.tiles.get(self.position)
                tile.activate(self.position - self.last_position, self.player)

            # Indique que l'opération a fonctionné
            return True

        # Indique que l'opération a échoué
        return False

    def move_of(self, tiles: int) -> bool:
        """
        Fait avancer l'oie d'un certain nombre de cases.
        """
        return self.go_to(self.position + tiles)
