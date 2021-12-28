"""
Ce fichier contient toutes les définitions de classe et de fonctions
en rapport avec le plateu de jeu.
"""

# Import de 'common.py'
from common import *
import goose


# Définition des classes

class Board:
    """
    Une classe qui représente le plateau du jeu.
    """

    @staticmethod
    def from_file(file_name: str):
        """
        Crée un objet Board depuis un fichier JSON.
        """
        board = None

        with open(file_name, "r") as file:
            board = json.load(file)
            file.close()
        
        return board
    
    @staticmethod
    def defaut(width, height):
        board = Board(
            pygame.Surface(Tile.get_size(width, height), pygame.SRCALPHA),
            (width, height)
        )
        for x in range(width):
            for y in range(height):
                board.add_tile("assets/tiles/tile.png", lambda: print("action!"))
        board.add_goose((0, 200, 0))
        return board
    
    def __init__(self, surface: pygame.Surface, size: tuple[int] or list[int]):
        """
        Construit un objet Board avec les tuiles du plateau en paramètre.
        `size`: Définit la taille du plateau de jeu, en donnant le nombre de tuile
        en hauteur et en largeur, et une tuile a une taillepar défaut de 128px par 128px.
        `tiles`: Les tuiles déjà chargés sont fournies en argument.
        """
        self.surface = surface
        self.width, self.height = size
        self.size = self.width * self.height

        self.tiles = pygame.sprite.Group()
        self.geese = pygame.sprite.Group()
    
    def __getstate__(self) -> dict:
        """"""
        state = {}
        return state
    
    def __setstate__(self, state: dict):
        """"""
    
    def add_goose(self, color: list[int] or tuple[int]):
        """"""
        self.geese.add(goose.Goose(self, color))
    
    def add_tile(self, image: str, action: callable):
        """"""
        tile = Tile(self, image, self.get_tile(), action)
        tile.image.blit(
            pygame.font.SysFont("consolas", 25).render(f"{len(self.tiles) + 1}", True, (255, 255, 255)),
            (24, 24)
        )
        self.tiles.add(tile)
    
    def display(self) -> pygame.Surface:
        """"""
        self.tiles.draw(self.surface)
        self.geese.draw(self.surface)
        return self.surface
    
    def get_tile(self, position: int = None) -> list[int] or tuple[int]:
        """
        Retourne les coordonnées de l'emplacement de la prochaine tuile,
        sert à créer une spirale.
        """

        def spiral(width: int, height: int, left_tiles: int = None, padding: int = 0):
            
            if left_tiles == None:
                left_tiles = len(self.tiles) + 1

            if left_tiles > width:
                left_tiles -= width

                if left_tiles > height - 1:
                    left_tiles -= height - 1

                    if left_tiles > width - 1:
                        left_tiles -= width - 1

                        if left_tiles > height - 2:
                            return spiral(width - 2, height - 2, left_tiles - 2, padding + 1)
                        
                        return padding, height - left_tiles - 1 + padding
                    return width - 1 - left_tiles + padding, height - 1 + padding
                return width - 1 + padding, left_tiles + padding
            return left_tiles - 1 + padding, padding

        return spiral(self.width, self.height, position)
    
    def update(self, event: pygame.event.Event):
        self.tiles.update()
        self.geese.update(event)


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
        super().__init__()

        self.action = action
        self.board = board

        self.image = pygame.image.load(image).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = position[0] * Tile.WIDTH
        self.rect.y = position[1] * Tile.HEIGHT
