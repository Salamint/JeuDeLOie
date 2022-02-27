"""
Ce fichier regroupe tous les imports de bibliothèques
et les déclarations utilisées partout dans le programme.

Ce fichier est à inclure dans chaque nouveau fichier,
mais ne doit inclure aucun fichier, sauf les imports de bibliothèques.

À manipuler avec précaution.
"""

# Imports des bibliothèques
import abc
import json
import os
import pickle
import pygame
import random
import socket
import sys
import time


# Initialisation des modules
pygame.init()
pygame.mixer.pre_init()
pygame.display.init()
pygame.font.init()


# Création d'un premier écran, permettant l'utilisation
# du package pygame.display par la suite.

# Taille de l'écran
screen_size = (1050, 640)
# Création de l'écran
screen = pygame.display.set_mode(screen_size)

# Constantes
MAX_PLAYERS = 4
SAVES_PATH = "data/saves"

# Couleurs
geese_colors = [
    (255, 255, 255),
    (128, 255, 128),
    (255, 128, 128),
    (128, 128, 255)
]

push_buttons_colors = {
    'bottom': '#2e5cb8',
    'normal': '#4775d1',
    'hover': '#0099ff',
    'press': '#4db8ff'
}

# Polices d'écriture
debug_font = pygame.font.SysFont("consolas", 20)
default_font = pygame.font.Font(None, 30)
tile_font = pygame.font.SysFont("consolas", 12)
sans_font = pygame.font.SysFont("Comic Sans MS", 60)
win_font = pygame.font.Font(None, 60)


# Définition des fonctions

def access_directory(directory: str) -> str:
    """
    Cherche à accéder à un dossier :
    Si le dossier n'existe pas, il est créé.
    """

    # Si le dossier n'existe pas encore.
    if not os.path.exists(directory):
        # Le créer.
        os.mkdir(directory)

    # Retourne le nom du dossier.
    return directory


def center_height(height: int, container: int):
    """
    Centre une hauteur à partir d'une première hauteur, et d'une hauteur servant de conteneur.
    """
    return container // 2 - height // 2


def center_rect(rect: pygame.Rect, container: pygame.Rect) -> (int, int):
    """
    Une fonction permettant de centrer une surface à l'intérieur d'une autre surface.
    Renvoie uniquement des coordonnées, ne modifie aucune des deux surfaces.
    """
    return (
        center_width(rect.width, container.width),
        center_height(rect.height, container.height)
    )


def center_surface(surface: pygame.Surface, container: pygame.Surface) -> (int, int):
    """
    Une fonction permettant de centrer une surface à l'intérieur d'une autre surface.
    Renvoie uniquement des coordonnées, ne modifie aucune des deux surfaces.
    """
    content_width, content_height = surface.get_size()
    container_width, container_height = container.get_size()
    return (
        center_width(content_width, container_width),
        center_height(content_height, container_height)
    )


def center_width(width: int, container: int):
    """
    Centre une largeur à partir d'une première largeur, et d'une largeur servant de conteneur.
    """
    return container // 2 - width // 2


# Définition des classes et interfaces

class Application(abc.ABC):
    """
    Classe abstraite représentant une application.
    Toutes les méthodes de cette classe ne sont abstraites (comme la méthode __init__).

    Une classe implémentant cette interface devra alors avoir une méthode display, qui se charge de l'affichage,
    une méthode quit qui se charge de quitter l'application et une méthode start que se charge su démarrage
    de l'application.
    """

    def __init__(self, __screen: pygame.Surface, task: type):
        """
        Construit une nouvelle instance d'une application avec des attributs par défaut.
        Une application doit avoir un écran, une tâche et une tâche par défaut.
        """
        self.screen = __screen
        self.default_task: type = task
        self.task: Task = self.default_task(self)

    @abc.abstractmethod
    def display(self):
        """
        Méthode abstraite à implémenter servant à l'affichage de l'application sur un écran.
        """
        pass

    @abc.abstractmethod
    def quit(self):
        """
        Méthode abstraite à implémenter qui ferme l'application en cours.
        """
        pass

    @abc.abstractmethod
    def start(self):
        """
        Méthode abstraite à implémenter qui démarre l'application en cours.
        """
        pass


class Button(pygame.sprite.Sprite):
    """
    Une classe représentant un bouton cliquable.
    Un bouton a un texte, une surface et un rectangle servant de boîte de collision.
    """

    def __init__(self, label: str, size: (int, int), position: (int, int), action: callable):
        """
        Initialise un nouveau bouton.
        Une fonction, méthode ou autre objet appelable est passée en paramètres et est appelé lors du click sur
        le bouton sans aucun paramètre.
        """
        super().__init__()

        # Données spécifiques au bouton (texte, action, souris au-dessus...).
        self.action: callable = action
        self.label = label
        self.hovering = False

        # Image du bouton (composant graphique).
        self.image = pygame.Surface(size)
        self.image.fill('#000000')
        self.render('#FFFFFF')

        # Rectangle du bouton (boîte de collision et d'affichage).
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position

    def render(self, color: str):
        """
        Affiche le texte du bouton sur son image, au centre et avec une couleur indiquée (code hexadecimal).
        Cette action est gourmande en temps, il est donc conseillé de l'utiliser peut souvent.
        """
        # Créer une surface avec le texte de la couleur indiquée.
        text = debug_font.render(self.label, True, color, '#000000')
        # Affiche le texte sur l'image du bouton au centre.
        self.image.blit(
            text, center_surface(text, self.image)
        )
    
    def update(self, event: pygame.event.Event, contained: (int, int) = None):
        """
        Met à jour le bouton, active son action lorsque la souris clique dessus
        et change sa couleur si la souris est placée au-dessus du bouton.
        """

        rect = self.rect.copy()
        if contained is not None:
            rect.x += contained[0]
            rect.Y += contained[1]

        # Lorsque la pointe de la souris rentre en contact avec la boîte de collision.
        if rect.collidepoint(*pygame.mouse.get_pos()):

            # Si ce n'était pas le cas au par-avant.
            if self.hovering is False:
                # Change la couleur du texte du bouton.
                self.render('#FFFF00')
                # Indique qu'à présent la souris est au-dessus du bouton.
                self.hovering = True

            # Si le click gauche est actionné.
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                # Actionne la fonction.
                self.action()

        # Si la souris n'est pas placée au-dessus du bouton, et que ce n'était pas le cas avant.
        elif self.hovering is True:
            # Change la couleur du texte du bouton.
            self.render('#FFFFFF')
            # Indique qu'à présent la souris n'est au-dessus du bouton.
            self.hovering = False


class ErrorMessage(pygame.sprite.Sprite):
    """
    Une classe représentant un message d'erreur qui peut être affiché sur l'écran
    """

    def __init__(self, app: 'Application', error: Exception):
        """
        Construit une nouvelle instance de la classe 'ErrorMessage' représentant un message d'erreur
        pouvant être affiché à l'écran.
        """

        # Appel du constructeur de la superclasse
        super().__init__()

        # Stocke l'erreur
        self.error = error

        # Stocke les dimensions
        width, height = 384, 128

        # Image
        self.image = pygame.Surface((width, height))
        self.image.fill('#FFFFFF')
        self.image.fill('#000000', pygame.Rect(8, 8, width - 16, height - 16))

        # Rectangle
        self.rect = pygame.Rect(
            *center_rect(self.image.get_rect(), app.screen.get_rect()),
            width, height
        )

        # Application du message
        self.image.blit(debug_font.render("Une erreur est survenue, plus", True, '#FFFFFF'), (16, 24))
        self.image.blit(debug_font.render("d'informations dans la console.", True, '#FFFFFF'), (16, 56))
        self.image.blit(debug_font.render("Appuyez sur une touche ...", True, '#FFFFFF'), (16, 88))

        # Affichage du message dans la console
        print(self.error)


class LoadingException(Exception):
    """
    Une classe représentant une erreur de chargement, utilisé par le jeu et le plateau lors du chargement de fichiers.
    """

    def __init__(self, file: str, *messages: str):
        """
        Construit une nouvelle instance de la classe 'LoadingError' représentant une erreur de chargement.
        """

        # Appel du constructeur de la superclasse 'Exception'
        super().__init__()

        # Stocke le message à afficher
        message = " ".join(messages)
        self.message = f"[{file}]: {message}"

    def __str__(self) -> str:
        """
        Renvoie une chaîne de caractères représentant le message de l'erreur.
        """

        # Retourne le message d'erreur
        return self.message


class PlayerException(Exception):
    """
    Une classe représentant une erreur de joueur, utilisé par le jeu lors du tour de jeu des joueurs
    ou lorsqu'ils rejoignent une partie.
    Cette classe ne possède aucun corps.
    """


class PushButton(Button):
    """
    Classe représentant un bouton poussoir, qui fait une animation lorsqu'il est pressé, et ne s'active
    que lorsqu'il est relâché.
    Il est possible en plus de choisir sa couleur, le rayon de l'arrondissement des angles ainsi que l'élévation.
    """

    def __init__(
            self, label: str, size: (int, int), position: (int, int), action: callable,
            elevation: int = 8, border_radius: int = 16
    ):
        """
        Construit une nouvelle instance de la classe 'PushButton' représentant un bouton poussoir
        et héritant de la classe 'Button'.

        Le bouton poussoir fonctionne de la même manière qu'un bouton normal, à l'exception qu'il est animé
        et est activé lorsqu'il est relâché.
        """

        # Appel du constructeur de la superclasse 'Button'
        super().__init__(label, size, position, action)

        # Attributs primaires
        self.pressed = False
        self.elevation = elevation
        self.border_radius = border_radius

        # Taille
        self.size = list(size)
        # Image
        self.image = pygame.Surface((self.size[0], self.size[1] + self.elevation))
        # Rectangle
        self.rect = self.image.get_rect()
        self.rect.x = position[0]
        self.rect.y = position[1] - self.elevation

        # Boîte de collision
        self.layer = self.image.get_rect()
        self.layer.height -= self.elevation
        # Texte
        self.text = default_font.render(self.label, True, '#FFFFFF')

        # Affiche le bouton.
        self.display(push_buttons_colors['normal'])

    def display(self, color: str):
        """
        Affiche le texte du bouton sur son image, au centre et avec une couleur indiquée (code hexadecimal).
        Cette action est gourmande en temps, il est donc conseillé de l'utiliser peut souvent.
        """
        # Filling with black.
        self.image.fill('#000000')
        # Drawing button's bottom part.
        pygame.draw.rect(
            self.image, push_buttons_colors['bottom'],
            pygame.Rect(0, self.elevation, *self.size),
            border_radius=self.border_radius
        )
        # Drawing button's top part and text.
        pygame.draw.rect(self.image, color, self.layer, border_radius=self.border_radius)
        x, y = center_rect(self.text.get_rect(), self.layer)
        y += self.layer.y
        self.image.blit(self.text, (x, y))

    def update(self, event: pygame.event.Event, contained: (int, int) = None):
        """
        Met à jour le bouton, active son action lorsque la souris clique dessus
        et change sa couleur si la souris est placée au-dessus du bouton.
        """

        rect = self.rect.copy()
        if contained is not None:
            rect.x += contained[0]
            rect.y += contained[1]

        # Lorsque la pointe de la souris rentre en contact avec la boîte de collision.
        if rect.collidepoint(*pygame.mouse.get_pos()):

            # Si ce n'était pas le cas au par-avant.
            if self.hovering is False:
                # Change la couleur du bouton.
                self.display(push_buttons_colors['hover'])
                # Indique qu'à présent la souris est au-dessus du bouton.
                self.hovering = True

            # Si le click gauche est actionné.
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:

                # Si le bouton n'était pas en train d'être pressé.
                if self.pressed is False:
                    # Abaisse le bouton.
                    self.layer.y = self.elevation
                    # Change la couleur du bouton.
                    self.display(push_buttons_colors['press'])
                    # Indique que le bouton est à présent pressé.
                    self.pressed = True

                # Si le bouton était en train d'être pressé.
                else:
                    # Relève le bouton.
                    self.layer.y = 0
                    # Change la couleur du bouton.
                    self.display(push_buttons_colors['normal'])
                    # Indique que le bouton est relâché.
                    self.pressed = False

            elif self.pressed is True:
                # Indique que le bouton est relâché.
                self.pressed = False
                # Relève le bouton.
                self.layer.y = 0
                # Change la couleur du bouton.
                self.display(push_buttons_colors['normal'])
                # Actionne la fonction.
                self.action()

        # Si la souris n'est pas placée au-dessus du bouton, et que ce n'était pas le cas avant.
        elif self.hovering is True:
            # Change la couleur du bouton.
            self.display(push_buttons_colors['normal'])
            # Indique qu'à présent la souris n'est au-dessus du bouton.
            self.hovering = False


class Savable(abc.ABC):
    """
    Classe abstraite représentant une tâche.
    Toutes les méthodes de cette classe ne sont abstraites (comme la méthode __init__).

    Une classe implémentant cette interface, devra alors avoir une méthode __getstate__,
    qui se charge de récupérer les informations de l'objet dans un dictionnaire, ainsi que d'une méthode __setstate__,
    qui se charge de créer un objet à partir d'informations stockées dans un dictionnaire.
    """

    @abc.abstractmethod
    def __getstate__(self) -> dict:
        """
        Méthode abstraite à implémenter qui sert à la sauvegarde de l'objet.
        Doit retourner un dictionnaire des attributs, et ne demande aucun argument.
        """
        pass

    @abc.abstractmethod
    def __setstate__(self, state: dict):
        """
        Méthode abstraite à implémenter qui sert au chargement de l'objet.
        Ne dois rien retourner et demande un dictionnaire des attributs en argument.
        """
        pass


class Task(abc.ABC):
    """
    Classe abstraite représentant une tâche.
    Toutes les méthodes de cette classe ne sont abstraites (comme la méthode __init__).

    Une classe implémentant cette interface, devra alors avoir une méthode display,
    qui se charge de l'affichage, ainsi que d'une méthode update, avec un argument 'event',
    qui se charge de l'actualisation de la tâche.
    """

    def __init__(self, app: 'Application'):
        """
        Construit une nouvelle instance d'une tâche avec des attributs par défaut.
        Une tâche doit être associée avec une application.
        """
        self.app = app

    @abc.abstractmethod
    def display(self):
        """
        Méthode appelée lors de l'affichage de la tâche.
        L'affichage de la tâche correspond à l'affichage de tous ses composants.
        Cette méthode est abstraite et lèvera une exception si elle n'est pas recouverte.
        """
        pass

    @abc.abstractmethod
    def update(self, event: pygame.event.Event):
        """
        Méthode appelée lors de l'actualisation de la tâche, avec en paramètre un évènement pygame
        (click de souris, touche pressée/levée ...).
        Cette méthode est abstraite et lèvera une exception si elle n'est pas recouverte.
        """
        pass
