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

# todo: documentation
class Board(Savable):
    """
    Une classe qui représente le plateau du jeu.
    """

    @staticmethod
    def from_file(file_name: str):
        """
        Crée un objet Board depuis un fichier JSON.
        """

        with open(file_name, "r") as file:
            info = json.load(file)
            file.close()

        board = Board(info.get('width', 8), info.get('height', 8))

        for tile in info.get('tiles', []):
            board.add_tile(tile)
        
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
    
    def __init__(self, width: int, height: int):
        """
        Construit un objet Board avec les tuiles du plateau en paramètre.
        `size`: Définit la taille du plateau de jeu, en donnant le nombre de tuiles
        en hauteur et en largeur, et une tuile a une taille par défaut de 128 px par 128 px.
        `tiles`: Les tuiles déjà chargées sont fournies en argument.
        """
        self.width, self.height = width, height
        self.surface = pygame.Surface((self.width * Tile.WIDTH, self.height * Tile.HEIGHT))

        self.mapping = Board.generate(self.width, self.height)
        self.tiles = pygame.sprite.Group()

        self.display()
    
    def __getstate__(self) -> dict:
        """"""
        state = self.__dict__.copy()
        state.update(
            {
                'width': self.width,
                'height': self.height,
                'tiles': [getattr(tile, "file") for tile in self.tiles]
            }
        )
        return state
    
    def __setstate__(self, state: dict):
        """"""
        self.__init__(state['width'], state['height'])
    
    def add_tile(self, name: str):
        """"""
        position = len(self.tiles)
        tile = Tile(self, name, self.get_at(position))
        if position > 0:
            tile.image.blit(
                pygame.font.SysFont("consolas", 12).render(f"{position}", True, '#000000', '#c3c3c3'),
                (4, 4)
            )
        self.tiles.add(tile)
    
    def display(self):
        """"""
        self.tiles.draw(self.surface)
    
    def get_at(self, position: int = None) -> (int, int) or None:
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

    def __init__(self, board: Board, name: str, position: (int, int)):
        """"""
        super().__init__()
        self.board = board

        self.name = name

        with open("data/tiles.json", "r") as file:
            data = json.load(file)
            self.action = data.get(self.name)
            self.image = pygame.image.load(f"assets/tiles/{self.name}.jpg").convert()

        self.rect = self.image.get_rect()
        self.rect.x = position[0] * Tile.WIDTH
        self.rect.y = position[1] * Tile.HEIGHT
