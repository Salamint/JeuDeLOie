"""
Un fichier contenant les composants du jeu.
"""

# Import de 'common.py'
from os import stat
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
        self.file = None

        self.board = board.Board.default(8, 8)
        self.gameplay = multiplayer.SAME_MACHINE
        self.geese = pygame.sprite.Group()

        self.pause = False
        self.pause_menu = pygame.sprite.Group()
        self.pause_menu.add(self.resume, self.save, self.quit)
        
        self.players: list[player.Player] = []
        self.turn = 0
        self.start_time = time.time()

        self.add_player()
        self.stats = pygame.Surface((screen_size[0], 32))
    
    def __getstate__(self) -> dict:
        """"""
        state = {
            'file': self.file,
            'turn': self.turn,
            'board': self.board,
            'players': self.players,
            'elapsed': self.start_time,
            'multiplayer': self.gameplay
        }
        return state
    
    def __setstate__(self, state: dict):
        """"""
        self.file = state.get('file', None)
        self.turn = state.get('turn', 0)
        self.board = state.get('board')
        self.players = state.get('players', [])
        self.start_time = state.get('elapsed', 0) - time.time()
        self.gameplay = state.get('multiplayer', multiplayer.SAME_MACHINE)
    
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

        if self.pause:
            self.pause_menu.draw(self.app.screen)

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
    
    @Button("Quitter", (720, 300))
    def quit(self):
        """
        Quitte le jeu en remplaçant la tâche en cours par l'écran titre.
        """
        # todo : Créer l'écran titre et remplacer 'None' par l'écran titre
        self.app.task = None
    
    @Button("Reprendre", (720, 350))
    def resume(self):
        """"""
        self.pause = False
    
    @Button("Sauvegarder", (720, 400))
    def save(self):
        """
        Sauvegarde le jeu, dans le dernier fichir ou à été enregistré la partie,
        ou lors de la première sauvegarde, crée un fichier de sauvegarde.
        """

        # Si le fichier n'exitsait pas.
        if self.file is None:

            # Si le dossier des sauvegardes n'existe pas encore (première suavegarde).
            if not os.path.exists(SAVE_PATH):
                # Crée le dossier des sauvegardes.
                os.mkdir(SAVE_PATH)
            
            # Compte le nombre de fichier dans le dossier des sauvegardes.
            save_number = len(os.listdir(SAVE_PATH))
            # Stocke le nom du fichier de sauvegarde.
            self.file = f"{SAVE_PATH}/save#{save_number}.bin"
        
        # Sauvegarde le jeu.
        with open(self.file, "wb") as file:
            pickle.dump(self, file)

    def update(self, event: pygame.event.Event):
        """
        Met à jour le jeu, le plateau du jeu et les oies.
        """
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.pause = not self.pause
        
        if not self.pause:
            self.board.update(event)
            self.geese.update(event)
            self.play()
        else:
            self.pause_menu.update(event)
