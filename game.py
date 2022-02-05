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

        self.dices = [
            pygame.image.load(f"assets/dice/{number + 1}.png").convert_alpha()
            for number in range(6)
        ]
        self.image = pygame.image.load("assets/dice/1.png").convert_alpha()
        self.rect = self.image.get_rect()

        self.nbr_move = 0

    def update(self, event: pygame.event.Event):
        """
        Change la face du dé en fonction du lancer de dé
        (chiffre aléatoire entre 1 et 6) et compte le nombre
        de cases que l'oie doit parcourir
        """

        # Nombre de mouvements réalisés
        self.nbr_move = 0

        # Si une touche est pressée, et qu'il s'agit de la barre espace
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:

            # Stocke le résultat du lancé de dé
            result = roll_dice()
            # Change l'image du dé au nombre correspondant
            self.image = self.dices[result - 1]
            # Stocke le nombre de mouvements à réaliser
            self.nbr_move += result


class Game(Task, Savable):
    """
    Une classe représentant le jeu, elle se différencie par son utilisation et ses attributs :
    La classe Application gère le jeu et les composants graphiques de base (fenêtre),
    ainsi que d'autres choses diverses qui n'ont pas de rapport avec la classe Game.

    Elle implémente la classe abstraite/interface ITask, et implémente donc les méthodes
    display et update.
    """

    def __init__(self, app: Application):
        super().__init__(app)
        self.file = None

        self.is_playing = False

        self.board = board.Board.default(8, 8)
        self.gameplay = multiplayer.SAME_MACHINE
        self.geese = pygame.sprite.Group()

        self.pause = False
        self.pause_menu = pygame.sprite.Group()
        self.pause_menu.add(
            Button("Reprendre", (256, 64), (192, 192), self.resume),
            Button("Sauvegarder", (256, 64), (192, 256), self.save),
            Button("Quitter", (256, 64), (192, 320), self.quit)
        )

        self.players: list[player.Player] = []
        self.turn = 0
        self.timer = time.perf_counter()

        self.add_player()
        self.stats = pygame.Surface((screen_size[0], 32))

        self.new_dice_one = Dice()
        self.new_dice_two = Dice()
        self.dice_one = pygame.sprite.Group()
        self.dice_two = pygame.sprite.Group()

        self.add_dices()
        self.dice_zone_one = pygame.Surface((140, 320))
        self.dice_zone_two = pygame.Surface((140, 320))

    def __getnewargs__(self) -> tuple:
        return self.app,

    def __getstate__(self) -> dict:
        """"""
        state = self.__dict__.copy()
        state['timer'] -= time.perf_counter()
        return state

    def __setstate__(self, state: dict):
        """"""
        state['timer'] += time.perf_counter()
        self.__dict__ = state.copy()

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

        current_time = time.gmtime(time.perf_counter() - self.timer)
        statistic_text = debug_font.render(
            time.strftime("Vous jouez depuis : %H:%M:%S", current_time),
            True, (255, 255, 255), (0, 0, 0)
        )
        self.stats.blit(statistic_text, center_surface(statistic_text, self.stats))

        self.app.screen.blit(self.stats, (0, 608))

        self.app.screen.blit(self.dice_zone_one, (585, 200))
        self.app.screen.blit(self.dice_zone_two, (585, 320))
        self.app.screen.blit(self.board.surface, (64, 64))

        if self.pause:
            self.pause_menu.draw(self.app.screen)

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
        self.is_playing = True
        self.players[self.turn].play()

    def quit(self):
        """
        Quitte le jeu en remplaçant la tâche en cours par l'écran titre.
        """
        self.app.task = self.app.default_task(self.app)

    def resume(self):
        """"""
        self.pause = False

    def save(self):
        """
        Sauvegarde le jeu, dans le dernier fichier ou a été enregistré la partie,
        ou lors de la première sauvegarde, crée un fichier de sauvegarde.
        """

        # Si le fichier n'existait pas.
        if self.file is None:
            # Compte le nombre de fichiers dans le dossier des sauvegardes.
            save_number = len(os.listdir(access_directory(SAVE_PATH)))
            # Stocke le nom du fichier de sauvegarde.
            self.file = f"{SAVE_PATH}/save#{save_number}.pickle"

        # Sauvegarde le jeu.
        with open(self.file, "wb") as file:
            pickle.dump(self, file)

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
