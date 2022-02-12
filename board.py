"""
Ce fichier contient toutes les définitions de classe et de fonctions
en rapport avec le plateau de jeu.
"""

# Import de 'common.py'
from common import *

# Import d'autres fichiers
import player


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

    @staticmethod
    def from_file(file_name: str):
        """
        Charge un plateau de jeu depuis un fichier JSON.
        """

        # Ouvre un fichier
        with open(file_name, "r") as file:
            # Charge les informations du fichier
            data = json.load(file)
            # Ferme le fichier
            file.close()

        # Stocke la largeur et hauteur du plateau
        width, height = data.get('width', 8), data.get('height', 8)

        # Crée une cartographie du plateau (emplacement des cases selon leur position)
        tiles: {int: 'Tile'} = {}

        for position, tile in enumerate(data.get("tiles", [])):
            tiles[position] = Tile(tile, spiral(width, height, position), index=position if position != 0 else None)

        # Crée et retourne un nouveau plateau de dimensions indiquées dans le fichier
        return Board(width, height, tiles)
    
    def __init__(self, width: int, height: int, tiles: {int: 'Tile'}):
        """
        Construit un objet Board avec les cases du plateau en paramètre.
        'size' : Définit la taille du plateau de jeu, en donnant le nombre de tuiles
        en hauteur et en largeur, et une tuile a une taille par défaut de 128 px par 128 px.
        'tiles' : Les tuiles déjà chargées sont fournies en argument.
        """

        # Dimensions du plateau
        self.width = width
        self.height = height

        # Surface et tuiles du plateau
        self.surface = pygame.Surface((self.width * Tile.WIDTH, self.height * Tile.HEIGHT))
        self.tiles = tiles

        # Affiche le plateau
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

    def display(self):
        """
        Affiche l'ensemble des cases du plateau sur la surface qui leur est destinée.
        """
        for tile in self.tiles.values():
            self.surface.blit(tile.image, tile.rect)

    @property
    def size(self):
        """
        Retourne la superficie du plateau de jeu (en nombre de cases).
        Peut servir à calculer le nombre de cases totales que le plateau compte.
        """
        return self.width * self.height
    
    def update(self, event: pygame.event.Event):
        """
        Met à jour l'ensemble des cases du plateau de jeu, à l'aide d'un événement.
        """
        for tile in self.tiles.values():
            tile.update(event)


class Tile(pygame.sprite.Sprite):
    """
    Une classe qui représente une case du plateau.

    Une tuile est représentée par sa taille et position (rectangle),
    ainsi qu'une image et une action exécutée lorsqu'un joueur atterri dessus.
    """

    # Constantes représentant les dimensions d'une case (à ne pas modifier).
    WIDTH = 64
    HEIGHT = 64

    def __init__(self, name: str, position: (int, int), index: int = None):
        """
        Construit un object Tile.
        Une case requiert un nom, une position (coordonnées) et optionnellement
        un indice à afficher en haut à gauche de la case.
        """

        # Appel le constructeur de la superclasse
        super().__init__()

        # Le nom de la case
        self.name = name
        # Ses coordonnées
        self.x, self.y = position

        # Ouvre le fichier des tuiles en mode lecture
        with open("data/tiles.json", "r") as file:

            # Charge dans un dictionnaire les informations du fichier
            data = json.load(file)

            # Récupère l'action associée à la case (None lorsque introuvable)
            self.action = data.get(self.name)
            # Charge l'image correspondant à la case
            self.image = pygame.image.load(f"assets/tiles/{self.name}.jpg").convert()

        # Si un indice est passé en paramètres, c'est qu'il est à afficher
        if index is not None:
            # L'afficher sur l'image de la case
            self.image.blit(
                tile_font.render(str(index), True, '#000000', '#c3c3c3'),
                (4, 4)
            )

        # Le rectangle de la case
        self.rect = self.image.get_rect()
        self.rect.x = self.x * Tile.WIDTH
        self.rect.y = self.y * Tile.HEIGHT

    def activate(self, tiles: int, p: player.Player):
        """
        Méthode appelée lorsqu'un joueur arrive sur cette case.
        Ajoute une action à la liste des effets du joueur.
        """

        # Si l'action de la case n'est pas nulle (inexistante)
        if self.action is not None:
            # Ajouter une nouvelle action à la liste d'effets du joueur
            p.effects.append(self.action(tiles, p))
