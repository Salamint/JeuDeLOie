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

def center_surface(surface: pygame.Surface, container: pygame.Surface):
    text_width, text_height = surface.get_size()
    container_width, container_height = container.get_size()
    return (
        container_width // 2 - text_width // 2,
        container_height // 2 - text_height // 2
    )


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

    def __init__(self, label: str, position: (int, int), action: callable):
        super().__init__()
        self.action: callable = action
        self.label = label
        self.hovering = False

        self.image = pygame.Surface((256, 64))
        self.image.fill('#000000')
        self.render('#FFFFFF')

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position

    def render(self, color: str):
        text = font.render(self.label, True, color, '#000000')
        self.image.blit(
            text, center_surface(text, self.image)
        )
    
    def update(self, event: pygame.event.Event):
        if self.rect.collidepoint(*pygame.mouse.get_pos()):
            if self.hovering is False:
                self.render('#FFFF00')
                self.hovering = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                self.action()
        elif self.hovering is True:
            self.render('#FFFFFF')
            self.hovering = False


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
