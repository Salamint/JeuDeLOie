"""
Ce fichier contient toutes les définitions de classe et de fonctions
en rapport avec le plateau de jeu.
"""

# Import de 'common.py'
from common import *


# Définition des fonctions

def spiral(width: int, height: int, position: int, padding: int = 0) -> (int, int):
    """
    Un algorithme permettant de déterminer les coordonnées d'une case dans une spirale carrée,
    dans le sens des aiguilles d'une montre, à partir de sa position, dans un repère en deux dimensions.
    Cet algorithme utilise une fonction récursive (qui s'appelle elle-même), ce genre de fonction
    est à manipuler avec précaution, ne pas mettre des valeurs qui ne pourraient potentiellement
    pas être calculées.

    NOTE : Cet algorithme est de plus en plus lorsque la taille de la spirale augmente ainsi que la position,
    il est donc conseillé de n'utiliser qu'un nombre limité de fois cette fonction, et de stocker les résultats
    dans un tableau de valeur ou un dictionnaire.

    :param width : La largeur de la spirale.
    :param height : La hauteur de la spirale.
    :param position : Les cases restantes (ou nombre de cases).
    :param padding : L'écartement par rapport au bord de la spirale. S'incrémente de 1 à chaque appel récursif.

    :returns : Un tuple à deux valeurs entières, représentant les coordonnées d'un point.
    """

    # La largeur et la hauteur sont décrémentés.
    width -= 1
    height -= 1

    # Variable qui est égale à 0 lors du premier contour puis à 1 pour tous les autres.
    v = padding - 1 if padding > 0 else 0

    # Lorsque le nombre de cases (position) est supérieur à la nouvelle largeur.
    if position > width - padding:
        position -= width

        # Lorsque le nombre de cases restantes (position) est supérieur à la nouvelle hauteur.
        if position > height - padding - v:
            position -= height - padding - v

            # Lorsque le nombre de cases (position) est supérieur à la nouvelle largeur.
            if position > width - padding:
                position -= width - padding

                # Lorsque le nombre de cases (position) est supérieur à la nouvelle largeur moins un,
                # dû à la rangée supérieure, cette ligne est une case plus petite que les autres.
                if position > height - padding - 1:
                    position -= height - padding - 1

                    # Appel de la fonction de manière récursive.
                    return spiral(width, height, position, padding + 1)

                # Retourne les coordonnées (ligne horizontale du haut).
                return padding, height - position

            # Retourne les coordonnées (ligne horizontale du haut).
            return width - position, height

        # Retourne les coordonnées (ligne verticale du droite).
        return width, position + padding + v

    # Retourne les coordonnées (ligne horizontale du haut).
    return position + v, padding


# Définition des classes

class Board(Savable):
    """
    Une classe qui représente le plateau du jeu.
    """

    # todo: remplacer par la méthode `from_file`.
    @staticmethod
    def default(width: int, height: int):
        """
        CETTE METHODE EST TEMPORAIRE, A REMPLACER PAR LA METHODE `from_file`,
        QUI CHARGE UN FICHIER PLATEAU.
        """
        board = Board(
            pygame.Surface(Board.get_surface_size(width, height)),
            (width, height)
        )
        for x in range(width):
            for y in range(height):
                board.add_tile("data/tiles/default.json")
        return board

    @staticmethod
    def from_file(file_name: str):
        """
        Crée un objet Board depuis un fichier JSON.
        """

        with open(file_name, "r") as file:
            board = json.load(file)
            file.close()
        
        return board

    @staticmethod
    def generate(width: int, height: int) -> {int: (int, int)}:
        """"""
        mapping = {}

        for position in range(width * height):
            mapping.setdefault(position, spiral(width, height, position))

        return mapping

    @staticmethod
    def get_surface_size(width: int, height: int) -> (int, int):
        """
        Une méthode statique qui retourne la largeur et la hauteur d'un plateau en pixels, et de taille donnée,
        en utilisant les constantes de la classe Tile.
        """
        return width * Tile.WIDTH, height * Tile.HEIGHT
    
    def __init__(self, surface: pygame.Surface, size: tuple[int] or list[int]):
        """
        Construit un objet Board avec les tuiles du plateau en paramètre.
        `size`: Définit la taille du plateau de jeu, en donnant le nombre de tuiles
        en hauteur et en largeur, et une tuile a une taille par défaut de 128 px par 128 px.
        `tiles`: Les tuiles déjà chargées sont fournies en argument.
        """
        self.surface = surface
        self.width, self.height = size

        self.mapping = Board.generate(self.width, self.height)
        self.tiles = pygame.sprite.Group()

        self.display()
    
    def __getstate__(self) -> dict:
        """"""
        state = self.__dict__.copy()
        state.update(
            {
                'size': (self.width, self.height),
                'tiles': [getattr(tile, "file") for tile in self.tiles]
            }
        )
        return state
    
    def __setstate__(self, state: dict):
        """"""
        size = state["size"]
        self.__init__(pygame.Surface(Board.get_surface_size(*size)), size)
    
    def add_tile(self, file: str):
        """"""
        tile = Tile(self, file, self.get_at(len(self.tiles)))
        tile.image.blit(
            pygame.font.SysFont("consolas", 16).render(f"{len(self.tiles) + 1}", True, (0, 0, 0)),
            (8, 8)
        )
        self.tiles.add(tile)
    
    def display(self):
        """"""
        self.tiles.draw(self.surface)
    
    def get_at(self, position: int = None) -> tuple[int, int] or None:
        """
        Retourne les coordonnées de l'emplacement de la prochaine tuile,
        sert à créer une spirale.
        """
        return self.mapping.get(position)

    @property
    def size(self):
        return self.width * self.height
    
    def update(self, event: pygame.event.Event):
        self.tiles.update(event)


class GooseAction:
    """
    Un décorateur pour une action d'oie.
    """

    def __init__(self, function: callable):
        """"""
        self.function = function
    
    def __call__(self, goose) -> None:
        """"""
        self.function(goose)


# todo: documentation
class Tile(pygame.sprite.Sprite):
    """
    Une classe qui représente une tuile du plateau.

    Une tuile est représentée par sa taille et position (rectangle),
    ainsi qu'une image et une action exécutée lorsqu'un joueur atterri dessus.
    """

    # Constantes représentant la largeur et la hauteur d'une tuile (ne pas modifier).
    WIDTH = 64
    HEIGHT = 64

    def __init__(self, board: Board, file: str, position: tuple[int] or list[int]):
        """"""
        super().__init__()
        self.board = board

        self.file = file

        with open(self.file, "r") as file:
            data = json.load(file)
            self.action = data['action']
            self.image = pygame.image.load(data['image']).convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.x = position[0] * Tile.WIDTH
        self.rect.y = position[1] * Tile.HEIGHT
