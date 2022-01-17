"""
Un fichier contenant les composants du jeu.
"""

# Import de 'common.py'
from common import *

# Import d'autres fichiers
import board
import multiplayer
import player


# Définition des classes




class Dice(pygame.sprite.Sprite):

    def __init__(self):

        super().__init__()

    def roll(self):
        ...

    def update(self, event: pygame.event.Event):

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ...


class Game(ITask):

    """
    Une classe représentant le jeu, elle se différencie par son utilisation et ses attributs :
    La classe Application gère le jeu et les composants graphiques de base (fenêtre),
    ainsi que d'autres choses diverses qui n'ont pas de rapport avec la classe Game.

    Elle implémente la classe abstraite/interface ITask, et implémente donc les méthodes
    display et update.
    """

    def __init__(self, app):
        self.app = app

        self.board = board.Board.default(8, 8)
        self.gameplay = multiplayer.SAME_MACHINE
        self.geese = pygame.sprite.Group()
        self.players: list[player.Player] = []
        self.turn = 0
        self.start_time = time.time()

        self.add_player((255, 255, 255))
        self.stats = pygame.Surface((screen_size[0], 32))
    
    def add_player(self, color: list[int] or tuple[int]):
        """
        Stocke un joueur dans la liste des joueurs et des oies.
        Comme le joueur dans la liste des joueurs est identique
        au joueur passé en paramètre, si l'on modifie l'oie du joueur,
        elle sera aussi modifiée dans e groupe de sprite des oies.
        """
        identifier = len(self.players)
        if identifier < MAX_PLAYERS:
            p = player.Player(self, identifier, geese_colors[identifier])
            self.players.append(p)
            self.geese.add(p.goose)
    
    def display(self):
        """
        Affiche les modifications sur l'écran.
        """
        self.board.display()
        self.geese.draw(self.board.surface)

        current_time = time.localtime(time.time() - self.start_time)
        self.stats.blit(
            font.render(
                time.strftime("Vous jouez depuis : %H:%M:%S:", current_time),
                True, (255, 255, 255), (0, 0, 0)
            ), (0, 0)
        )

        self.app.screen.blit(self.stats, (0, 608))
        self.app.screen.blit(self.board.surface, (0, 96))
    
    def next_turn(self):
        """
        Passe au tour de l'oie suivante, si la dernière oie à déjà jouée,
        c'est donc au tour de la première oie.
        """
        if self.turn < len(self.players) - 1:
            self.turn += 1
        else:
            self.turn = 0
    
    def play(self):
        self.players[self.turn].play()

    def update(self, event: pygame.event.Event):
        """
        Met à jour le jeu, le plateau du jeu et les oies.
        """
        self.board.update(event)
        self.geese.update(event)
        self.play()
