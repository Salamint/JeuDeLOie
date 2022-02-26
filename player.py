"""
Ce fichier contient la définition de la classe 'Player',
représentant un joueur.
"""

# Import de 'common.py'
from common import *

# Imports d'autres fichiers
import actions
import board
import game
import goose


# Définition des classes

class HeadUpDisplay:
    """
    Une classe représentant un affichage tête haute,
    permettant de récupérer et d'afficher des informations pour le joueur.
    Les affichages tête haute sont différents pour chaque joueur.
    """

    def __init__(self, player: 'Player'):
        """
        Construit une nouvelle instance de la classe 'HeadUpDisplay' représentant
        un affichage tête haute, permettant d'afficher des informations sur le joueur et la partie.
        """

        # Le joueur
        self.player = player
        # Raccourci à l'application
        self.app = self.player.game.app

        # Surface d'affichage des statistiques
        self.time = pygame.Surface((screen_size[0], 32))

    def display(self):
        """
        Affiche les informations à l'écran.
        """

        # Récupère le temps écoulé depuis le début de la partie et en fait une structure de temps
        current_time = time.gmtime(time.perf_counter() - self.player.game.timer)
        # Formate le temps de la manière %H:%M:%S
        statistic_text = default_font.render(
            time.strftime("Vous jouez depuis : %H:%M:%S", current_time),
            True, (255, 255, 255), (0, 0, 0)
        )
        # Affiche l'heure sur la surface des statistiques
        self.time.blit(statistic_text, center_surface(statistic_text, self.time))
        # Affiche sur l'écran le temps écoulé
        self.app.screen.blit(self.time, (0, 600))

        # Si le joueur n'est pas seul
        if self.player.game.enough_players():
            # Affiche à l'écran le tour du joueur
            self.app.screen.blit(
                default_font.render(f"Au tour du Joueur {self.player.id}", True, '#FFFFFF', '#000000'),
                (16, 16)
            )
        # Sinon
        else:
            # Affiche à l'écran le tour du joueur
            self.app.screen.blit(
                default_font.render(f"En attente d'autres joueurs...", True, '#FFFFFF', '#000000'),
                (16, 16)
            )

        # Affiche à l'écran la couleur du joueur
        self.app.screen.blit(default_font.render("Couleur :", True, '#FFFFFF', '#000000'), (356, 16))
        pygame.draw.rect(self.app.screen, self.player.goose.color, pygame.Rect(452, 8, 32, 32))

        # Affiche à l'écran la liste des effets en cours
        self.app.screen.blit(default_font.render("Effets en cours :", True, '#FFFFFF', '#000000'), (560, 16))
        # Affiche à l'écran la liste des effets en cours
        for index, effect in enumerate(self.player.effects):
            self.app.screen.blit(
                pygame.transform.scale(self.player.effects[effect].tile.image, (32, 32)),
                (740 + 40 * index, 8)
            )


class Player(Savable):
    """
    Une classe représentant un joueur. Un joueur est en général plus qu'une simple oie,
    et contiendra des informations plus diverses, comme des statistiques ou l'adresse IPv4.
    """

    def __init__(self, game_: 'game.Game', identifier: int, color: list[int] or tuple[int]):
        """
        Construit une nouvelle instance de la classe 'Player' représentant un joueur.
        Un joueur est associé à un jeu, possède un identifiant correspondant à son indice dans le dictionnaire
        des joueurs du jeu, ainsi qu'une oie et des effets.
        """

        # Le jeu
        self.game = game_

        # L'identifiant
        self.id = identifier

        # Les effets du joueur
        self.effects: dict[str, 'actions.Action'] = {}

        # L'état du joueur (False lui permet de se mouvoir, et True non)
        self.stopped = False

        # L'oie du joueur
        self.goose = goose.Goose(self, color)

        # L'affichage tête haute
        self.hud = HeadUpDisplay(self)

    def __getstate__(self) -> dict: ...

    def __setstate__(self, state: dict): ...

    def add_effect(self, name: str, action: 'actions.Action') -> 'actions.Action':
        """
        Ajoute l'action donnée dans le dictionnaire des effets ainsi que dans son HUD,
        puis retourne l'action.
        """

        # Ajout dans le dictionnaire
        self.effects[name] = action

        # Retourne l'action
        return action

    def dice_move(self):
        """
        Fait avancer le joueur en fonction des dés.
        """

        # Marque la distance à parcourir
        distance = 0

        # Parcours tous les dés du jeu
        for dice in self.game.dices:

            # Si le dé a été lancé durant le tour
            if dice.rolled:

                # Ajoute la valeur du dé la distance et réinitialise l'état du dé
                distance += dice.get_value()

        # Fait avancer le joueur
        self.move_of(distance)

    def discard_effect(self, name: str):
        """
        Supprime l'effet du dictionnaire des effets du joueur, ainsi que de son HUD.
        """

        # Retire l'action du dictionnaire des effets
        self.effects.pop(name, self)

    def move_of(self, distance: int):
        """
        Semblable à self.goose.move_of() mais fait reculer l'oie lorsqu'elle va trop loin.
        """

        # Si le joueur n'est pas stoppé et que la distance à parcourir n'est pas nulle
        if not self.stopped and distance != 0:
            
            # Avancer
            if not self.goose.move_of(distance):
                
                # S'il est impossible d'avancer, reculer
                self.goose.move_of(-distance)

            # Passe au tour suivant
            self.game.next_turn()

    def quit(self):
        """
        Fait quitter le joueur du jeu. Sauvegarde sa progression.
        """

        # Ajoute le joueur au cache des joueurs en le supprimant des joueurs actifs
        self.game.player_cache.append(self.game.players.pop(self.id))

    def update(self, event: pygame.event.Event):
        """
        Met à jour l'oie (placement).
        """

        # S'il y a assez de joueurs
        if self.game.enough_players():

            # Met à jour les dés
            for dice in self.game.dices:
                dice.update(event)

            # Fait avancer le joueur
            self.dice_move()

        # Met à jour la position de l'oie
        tile = self.game.board.tiles.get(self.goose.position)
        self.goose.rect.x = board.Tile.WIDTH * tile.x
        self.goose.rect.y = board.Tile.HEIGHT * tile.y
