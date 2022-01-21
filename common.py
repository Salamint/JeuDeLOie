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
screen_size = (640, 640)
# Création de l'écran
screen = pygame.display.set_mode(screen_size)

# Constantes
MAX_PLAYERS = 4
SAVE_PATH = "data/saves"

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
    """
    Simule un lancé de dé en retournant un nombre aléator entre 1 et 6.
    """
    return random.randint(1, 6)


# Définition des classes et interfaces

class Button(pygame.sprite.Sprite):
    """
    Une classe représentant un bouton clickable.
    """

    def __init__(self, label: str, position: (int, int)):
        super().__init__()
        self.action: callable = None
        self.label = label

        self.image = pygame.Surface((150, 50))
        self.image.fill('#000000')
        pygame.draw.rect(self.image, '#000000', pygame.Rect(0, 0, 150, 50))
        self.image.blit(font.render(self.label, True, '#FFFFFF', '#000000'), (50, 25))
        
        self.rect = self.image.get_rect()
        self.x, self.y = position
    
    def __call__(self, action: callable = None):
        if action is None:
            return self.action
        self.action = action
        return self.action
    
    def update(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
            self.__call__()


class ITask(abc.ABC):
    """
    Classe abstraite représentant une tâche.
    Toutes les méthodes de cette interface sont abstraites et peut être comparée à une interface.
    Une classe implémentant cette interface, devra alors avoir une méthode display,
    qui se charge de l'affichage, ainsi que d'une méthode update, avec un argument `event`,
    qui se charge de l'actualisation de la tâche.
    """

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
