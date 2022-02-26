"""
Un fichier contenant les composants du jeu,
tel que la classe 'Game' représentant le jeu et la classe 'Dice' représentant un dé,
pour gérer l'aléatoire
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

    @staticmethod
    def random() -> int:
        """
        Simule un lancé de dé en retournant un nombre aléatoire entre 1 et 6.
        """
        return random.randint(1, 6)

    def __init__(self, game: 'Game', position: (int, int)):
        """
        Construit une nouvelle instance de la classe 'Dice' représentant un dé
        et permettant de simuler des lancés de dés.
        """

        # Appel le constructeur de la superclasse
        super().__init__()

        # La partie en cours
        self.game = game

        # Valeur du dé
        self.value = 1
        # Si le dé a changé entre temps
        self.rolled = False

        # Liste contenant tous les sprites de dés allant de 1 à 6
        self.dices = [
            pygame.image.load(f"assets/dice/{number + 1}.png").convert()
            for number in range(6)
        ]

        # Image par défaut à 0 (1 point)
        self.image = self.dices[self.value - 1]
        # Rectangle (position et taille)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position
    
    def get_value(self):
        """
        Retourne la valeur du dé et réinitialise l'état du dé.
        """

        # Réinitialise l'état du dé
        self.rolled = False
        # Retourne la valeur du dé
        return self.value
    
    def roll(self):
        """
        Lance le dé, change son apparence et sa valeur.
        """

        # Stocke le résultat du lancé de dé
        self.value = Dice.random()
        # Change l'image du dé au nombre correspondant
        self.image = self.dices[self.value - 1]
        # Indique que le dé a été lancé
        self.rolled = True

    def update(self, event: pygame.event.Event):
        """
        Change la face du dé en fonction du lancer de dé
        (chiffre aléatoire entre 1 et 6) et compte le nombre
        de cases que l'oie doit parcourir
        """

        # Si une touche est pressée, et qu'il s'agit de la barre espace
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:

            # Lance le dé
            self.roll()


class Game(Task, Savable):
    """
    Une classe représentant le jeu, elle se différencie par son utilisation et ses attributs :
    La classe Application gère le jeu et les composants graphiques de base (fenêtre),
    ainsi que d'autres choses diverses qui n'ont pas de rapport avec la classe Game.

    Elle implémente la classe abstraite/interface ITask, et implémente donc les méthodes
    display et update.
    """

    MINIMUM = 2

    def __init__(self, app: 'Application'):
        """
        Construit une nouvelle instance de Game.
        Un jeu à des joueurs, un plateau, es dés, des règles et des statistiques.
        Il peut être mis en pause avec la méthode pause et être rétabli avec la méthode resume.
        """

        # Appel du constructeur de la superclasse
        super().__init__(app)
        # Fichier dans lequel la partie est enregistrée
        self.file = None
        # Erreurs possiblement levées lors de l'exécution du jeu, permettant d'afficher un message
        self.error_message: 'ErrorMessage' or None = None

        # Tente de générer un plateau à partir des fichiers du jeu
        try:
            # Charge le fichier
            self.board = board.Board.from_file("data/board.json")
        # Si une exception de chargement est levée (probablement de mauvaises valeurs fournies)
        except LoadingException as e:
            # Quitte la partie pour ne pas risquer d'erreurs
            self.error_message = ErrorMessage(self.app, e)

        # Mode de jeu (multijoueur)
        self.multiplayer = multiplayer.SAME_MACHINE
        # Le gagnant de la partie
        self.winner = None

        # L'état du jeu (en pause ou pas), attribut privé, accessible depuis les méthodes pause et resume
        self.paused = False
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
        self.players = list[player.Player]()
        self.player_cache = list[player.Player]()
        # Tour de jeu
        self.turn = 0
        # Si un joueur est en train de jouer
        self.is_playing = False

        # Un chronomètre de la partie
        self.timer = time.perf_counter()

        self.add_player()

        # Définit leur emplacement en x qui est identique
        dices_x = center_width(64, 274) + 576
        # Ajoute les dés
        self.dices = (
            Dice(self, (dices_x, 128)),
            Dice(self, (dices_x, 448))
        )

    def __getstate__(self) -> dict: ...

    def __setstate__(self, state: dict): ...

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

    def display(self):
        """
        Affiche les modifications sur l'écran.
        """

        # Si une erreur n'a été levée
        if self.error_message is not None:

            # Affichage du message d'erreur
            self.app.screen.blit(self.error_message.image, self.error_message.rect)

        # Si aucune erreur a été levée
        else:

            # Affiche le plateau de jeu
            self.board.display()
            # Affiche les oies
            for player_ in self.players:
                self.board.surface.blit(player_.goose.image, player_.goose.rect)
            # Affiche sur l'écran la surface du plateau
            self.app.screen.blit(self.board.surface, (64, 64))
            # Affiche les dés
            for dice in self.dices:
                self.app.screen.blit(dice.image, dice.rect)
            # Affiche l'affichage tête haute du joueur en train de jouer
            self.get_player().hud.display()

        # Si il y a un gagnant
        if self.winner is not None:

            # Afficher la victoire à l'écran
            text = win_font.render(f"Victoire du joueur {self.winner.id + 1}", True, '#FFFFFF', '#000000')
            self.app.screen.blit(text, center_surface(text, self.app.screen))

        # Si le jeu est en pause
        if self.paused:
            # Afficher le menu de pause
            self.pause_menu.draw(self.app.screen)

    def enough_players(self) -> bool:
        """
        Indique si le nombre de joueurs nécessaire pour une partie est atteint.
        """
        return len(self.players) >= Game.MINIMUM

    def get_player(self) -> 'player.Player':
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

    def pause(self):
        """
        Met le jeu en pause, empêche les éléments tels que le plateau ou les dés d'être mis à jour,
        mais continuera de les afficher.
        """
        self.paused = True

    def quit(self):
        """
        Quitte le jeu en remplaçant la tâche en cours par l'écran titre.
        """
        self.app.task = self.app.default_task(self.app)

    def resume(self):
        """
        Rétablit le jeu là où il s'était arrêté et arrête la pause.
        """
        self.paused = False

    def save(self):
        """
        Sauvegarde le jeu, dans le dernier fichier ou a été enregistré la partie,
        ou lors de la première sauvegarde, crée un fichier de sauvegarde.
        """

        # Si le fichier n'existait pas
        if self.file is None:
            # Compte le nombre de fichiers dans le dossier des sauvegardes
            save_number = len(os.listdir(access_directory(SAVES_PATH)))
            # Stocke le nom du fichier de sauvegarde
            self.file = f"{SAVES_PATH}/save#{save_number}.pickle"

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

        # Si une erreur a été levée lors de l'exécution du jeu
        if self.error_message is not None:

            # Si une touche est pressée
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                # Arrêter le jeu
                self.quit()

        # Si le jeu est en pause
        elif self.paused:

            # Si la touche espace est pressée
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                # Rétablir le jeu
                self.resume()

            # Met à jour les boutons de l'écran de pause
            self.pause_menu.update(event)

        # Si l'écran n'est pas en pause
        else:

            # Si une touche est pressée
            if event.type == pygame.KEYDOWN:

                # Si c'est la touche espace
                if event.key == pygame.K_ESCAPE:
                    # Mettre le jeu en pause
                    self.pause()

                # Si c'est la touche L
                if event.key == pygame.K_l:

                    # S'il y a plus d'un joueur en jeu
                    if self.enough_players():
                        # Faire quitter le joueur
                        self.get_player().quit()
                    # Sinon
                    else:
                        # Quitter la partie
                        self.quit()

                # Si c'est la touche J
                if event.key == pygame.K_j:

                    # Si des joueurs sont sauvegardés dans le cache
                    if len(self.player_cache) > 0:
                        # Ramener le dernier joueur aillant quitté
                        self.players.append(self.player_cache.pop(-1))
                    # Sinon
                    else:
                        # Créer un joueur
                        self.add_player()

            # Met à jour le plateau de jeu
            self.board.update(event)

            # Met à jour le joueur en train de jouer
            self.get_player().update(event)
