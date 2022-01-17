"""
Ce fichier regroupe tous les imports de bibliothèques,
et les déclarations utilisées partout dans le programme.

Ce fichier est à inclure dans chaque nouveau fichier,
mais ne doit inclure aucun fichier, sauf les imports de bibliothèques.

À manipuler avec précaution.
"""

# Imports des bibliothèques
import abc
import json
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
screen_size = (640, 640)
# Création de l'écran
screen = pygame.display.set_mode(screen_size)

# Constantes
MAX_PLAYERS = 4

# Couleurs
geese_colors = [
    (255, 255, 255),
    (128, 255, 128),
    (255, 128, 128),
    (128, 128, 255)
]

font = pygame.font.SysFont("consolas", 20)


# Définition des fonctions

def roll_dice():
    return random.randint(1, 6)


# Définition des classes et interfaces


class ITask(abc.ABC):
    """
    Classe abstraite représentant une tâche.
    Toutes les méthodes de cette interface sont abstraites, et peut être comparée à une interface.
    Une classe implémentant cette interface, devra alors avoir une méthode display,
    qui se charge de l'affichage, ainsi que d'une méthode update, avec un argument `event`,
    qui se charge de l'actualisation de la tâche.
    """

    @abc.abstractmethod
    def display(self):
        """
        Méthode appelée lors de l'affichage de la tâche.
        L'affichage de la tâche correspond à laffichage de tous ses composants.
        Cette méhode est abstraite et levera une exception si elle n'est pas recouverte.
        """
        pass

    @abc.abstractmethod
    def update(self, event: pygame.event.Event):
        """
        Méthode appelée lors de l'actualisation de la tâche, avec en paramètre un évènement pygame
        (click de souris, touche pressée/levée ...).
        Cette méthode est abstraite et levera une exception si elle n'est pas recouverte.
        """
        pass
