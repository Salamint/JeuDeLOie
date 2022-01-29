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
    """
    Classe représentant les deux dés qui pourront être lancés
    par le joueur en appuyant sur la touche "espace". Les dés
    sont lancés de façon aléatoire et ont six faces.
    """

    def __init__(self):

        super().__init__()

        self.image = pygame.image.load("assets/dice/1.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.nbr_move = 0

    def update(self, event: pygame.event.Event):
        """
        Change la face du dé en fonction du lancer de dé
        (chiffre aléatoire entre 1 et 6) et compte le nombre
        de cases que l'oie doit parcourir
        """

        self.nbr_move = 0

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                match roll_dice():
                    case 1:
                        self.image = pygame.image.load("assets/dice/1.png").convert_alpha()
                        self.nbr_move += 1
                    case 2:
                        self.image = pygame.image.load("assets/dice/2.png").convert_alpha()
                        self.nbr_move += 2
                    case 3:
                        self.image = pygame.image.load("assets/dice/3.png").convert_alpha()
                        self.nbr_move += 3
                    case 4:
                        self.image = pygame.image.load("assets/dice/4.png").convert_alpha()
                        self.nbr_move += 4
                    case 5:
                        self.image = pygame.image.load("assets/dice/5.png").convert_alpha()
                        self.nbr_move += 5
                    case 6:
                        self.image = pygame.image.load("assets/dice/6.png").convert_alpha()
                        self.nbr_move += 6


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

        self.add_player()
        self.stats = pygame.Surface((screen_size[0], 32))

        self.new_dice_one = Dice()
        self.new_dice_two = Dice()
        self.dice_one = pygame.sprite.Group()
        self.dice_two = pygame.sprite.Group()

        self.add_dices()
        self.dice_zone_one = pygame.Surface((140, 320))
        self.dice_zone_two = pygame.Surface((140, 320))

    def add_player(self):
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

    def add_dices(self):
        """
        Stocke les dés nouvellement créés dans deux groupes différents
        pour qu'ils soient indépendants l'un vis-à-vis de l'autre
        """
        self.new_dice_one.add(self.dice_one)
        self.new_dice_two.add(self.dice_two)

    def display(self):
        """
        Affiche les modifications sur l'écran.
        """
        self.board.display()
        self.geese.draw(self.board.surface)
        self.dice_one.draw(self.dice_zone_one)
        self.dice_two.draw(self.dice_zone_two)

        current_time = time.localtime(time.time() - self.start_time)
        self.stats.blit(
            font.render(
                time.strftime("Vous jouez depuis : %H:%M:%S:", current_time),
                True, (255, 255, 255), (0, 0, 0)
            ), (0, 0)
        )

        self.app.screen.blit(self.stats, (0, 608))
        self.app.screen.blit(self.board.surface, (0, 96))
        self.app.screen.blit(self.dice_zone_one, (545, 200))
        self.app.screen.blit(self.dice_zone_two, (545, 320))

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
        nbr_move = self.new_dice_one.nbr_move + self.new_dice_two.nbr_move

        self.board.update(event)
        self.geese.update(event, nbr_move)
        self.dice_one.update(event)
        self.dice_two.update(event)

        self.play()
