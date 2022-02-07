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

    def __init__(self, game, position: (int, int)):
        """
        Construit une nouvelle instance de dé
        """

        # Appel le constructeur de la superclasse
        super().__init__()

        # La partie en cours
        self.game = game

        # Liste contenant tous les sprites de dés allant de 1 à 6
        self.dices = [
            pygame.image.load(f"assets/dice/{number + 1}.png").convert_alpha()
            for number in range(6)
        ]

        # Image par défaut à 0 (1 point)
        self.image = self.dices[0]
        # Rectangle (position et taille)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position

    def update(self, event: pygame.event.Event):
        """
        Change la face du dé en fonction du lancer de dé
        (chiffre aléatoire entre 1 et 6) et compte le nombre
        de cases que l'oie doit parcourir
        """

        # Si une touche est pressée, et qu'il s'agit de la barre espace
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:

            # Stocke le résultat du lancé de dé
            result = roll_dice()
            # Change l'image du dé au nombre correspondant
            self.image = self.dices[result - 1]
            # Fait avancer le joueur du nombre de cases indiquées
            self.game.get_player().forward(result)


class Game(Task, Savable):
    """
    Une classe représentant le jeu, elle se différencie par son utilisation et ses attributs :
    La classe Application gère le jeu et les composants graphiques de base (fenêtre),
    ainsi que d'autres choses diverses qui n'ont pas de rapport avec la classe Game.

    Elle implémente la classe abstraite/interface ITask, et implémente donc les méthodes
    display et update.
    """

    def __init__(self, app: Application):
        """
        Construit une nouvelle instance de Game.
        Un jeu à des joueurs, un plateau, es dés, des règles et des statistiques.
        Il peut être mis en pause avec la méthode pause et être rétabli avec la méthode resume.
        """

        # Appel du constructeur de la superclasse
        super().__init__(app)
        # fichier dans lequel la partie est enregistrée
        self.file = None

        # Création du plateau de jeu
        self.board = board.Board.from_file("data/board.json")
        # Mode de jeu (multijoueur)
        self.multiplayer = multiplayer.SAME_MACHINE
        # Groupe de sprites d'oies
        self.geese = pygame.sprite.Group()

        # L'état du jeu (en pause ou pas), attribut privé, accessible depuis les méthodes pause et resume
        self.__pause = False
        # Menu de pause
        self.pause_menu = pygame.sprite.Group()
        buttons_size = (256, 64)
        buttons_x = center_width(buttons_size[0], self.app.screen.get_width())
        self.pause_menu.add(
            Button("Reprendre", buttons_size, (buttons_x, 192), self.resume),
            Button("Sauvegarder", buttons_size, (buttons_x, 256), self.save),
            Button("Quitter", buttons_size, (buttons_x, 320), self.quit)
        )

        # Liste des joueurs
        self.players: list[player.Player] = []
        # Tour de jeu
        self.turn = 0
        # Si un joueur est en train de jouer
        self.is_playing = False

        # Un chronomètre de la partie
        self.timer = time.perf_counter()
        # Surface d'affichage des statistiques
        self.stats = pygame.Surface((screen_size[0], 32))

        self.add_player()

        # Définit leur emplacement en x qui est identique
        dices_x = center_width(64, 274) + 576
        # Ajoute les dés
        self.dices = (
            Dice(self, (dices_x, 128)),
            Dice(self, (dices_x, 448))
        )

    # todo: améliorer les sauvegardes et documenter les méthodes spécifiées
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

    def display(self):
        """
        Affiche les modifications sur l'écran.
        """

        # Affiche le plateau de jeu
        self.board.display()
        # Affiche les oies
        self.geese.draw(self.board.surface)

        # Récupère le temps écoulé depuis le début de la partie et en fait une structure de temps
        current_time = time.gmtime(time.perf_counter() - self.timer)
        # Formate le temps de la manière %H:%M:%S
        statistic_text = debug_font.render(
            time.strftime("Vous jouez depuis : %H:%M:%S", current_time),
            True, (255, 255, 255), (0, 0, 0)
        )
        # Affiche l'heure sur la surface des statistiques
        self.stats.blit(statistic_text, center_surface(statistic_text, self.stats))

        # Affiche sur l'écran les statistiques
        self.app.screen.blit(self.stats, (0, 608))
        # Affiche sur l'écran la surface du plateau
        self.app.screen.blit(self.board.surface, (64, 64))
        # Affiche les dés
        for dice in self.dices:
            self.app.screen.blit(dice.image, dice.rect)

        # Si le jeu est en pause
        if self.__pause:
            # Afficher le menu de pause
            self.pause_menu.draw(self.app.screen)

    def get_player(self) -> player.Player:
        """
        Retourne le joueur en train de jouer (à qui c'est le tour).
        """
        return self.players[self.turn]

    def next_turn(self):
        """
        Passe au tour de l'oie suivante, si la dernière oie à déjà jouée,
        c'est donc au tour de la première oie.
        """

        # S'il reste des joueurs qui n'ont pas encore joué
        if self.turn < len(self.players) - 1:
            # Passer au joueur suivant
            self.turn += 1
        # Sinon
        else:
            # Reprendre depuis le début
            self.turn = 0

    # todo: revoir cette méthode
    def play(self):
        self.is_playing = True

    def pause(self):
        """
        Met le jeu en pause, empêche les éléments tels que le plateau ou les dés d'être mis à jour,
        mais continuera de les afficher.
        """
        self.__pause = True

    def quit(self):
        """
        Quitte le jeu en remplaçant la tâche en cours par l'écran titre.
        """
        self.app.task = self.app.default_task(self.app)

    def resume(self):
        """
        Rétablit le jeu là où il s'était arrêté et arrête la pause.
        """
        self.__pause = False

    def save(self):
        """
        Sauvegarde le jeu, dans le dernier fichier ou a été enregistré la partie,
        ou lors de la première sauvegarde, crée un fichier de sauvegarde.
        """

        # Si le fichier n'existait pas
        if self.file is None:
            # Compte le nombre de fichiers dans le dossier des sauvegardes
            save_number = len(os.listdir(access_directory(SAVE_PATH)))
            # Stocke le nom du fichier de sauvegarde
            self.file = f"{SAVE_PATH}/save#{save_number}.pickle"

        # Sauvegarde le jeu
        with open(self.file, "wb") as file:
            pickle.dump(self, file)

    def update(self, event: pygame.event.Event):
        """
        Met à jour le jeu.
        Lorsque le jeu est en pause, les boutons du menu de pause sont mis à jour,
        mais les autres éléments sont bloqués et ne sont pas mis à jour.
        Lorsque le jeu n'est pas en pause, le menu de pause n'est pas mis à jour,
        et le plateau du jeu, les oies et les dés le sont.
        """

        # Si le jeu est en pause
        if self.__pause:

            # Si la touche espace est pressée
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Rétablir le jeu
                self.resume()

            # Met à jour les boutons de l'écran de pause
            self.pause_menu.update(event)

        # Si l'écran n'est pas en pause
        else:

            # Si la touche espace est pressée
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Mettre le jeu en pause
                self.pause()

            # Met à jour les dés
            for dice in self.dices:
                dice.update(event)

            # Met à jour le plateau de jeu
            self.board.update(event)
            # Met à jour les joueurs
            self.geese.update(event)
            # Met à jour le tour de jeu
            self.play()
