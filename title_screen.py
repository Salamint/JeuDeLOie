# Import de 'common.py'
import math
import time

from common import *
import pygame, sys
import pygame.freetype
from pygame.sprite import Sprite
from pygame.rect import Rect

# Import des autres fichiers
import game

pygame.init()
gui_font = pygame.font.Font(None, 30)
class Title:

    def __init__(self, text, width, height, pos, elevation):

        self.running = True

        self.screen = screen
        self.game = game.Game(self)
        # Core attributes
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]

        # top rectangle
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#475F77'

        # bottom rectangle
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = '#354B5E'
        # text
        self.text_surf = gui_font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect()

        self.clock = pygame.time.Clock()

    def draw(self):
        # elevation logic
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=12)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    print('start')
                    self.play()
                    self.display()
                    self.pressed = False
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = '#475F77'

    def display(self):
        self.game.display()

    def update(self, event: pygame.event.Event):
        # déclancher la partie
        print('coucou')
        self.game.update(event)

    def play(self):
        while self.running:

            # Met à jour l'affichage.
            self.game.display()
            # Met à jour tous les écrans de pygame.
            pygame.display.flip()

            # Capture tous les évènements (click, appui sur une touche...) de la frame actuelle.
            for event in pygame.event.get():

                # Met à jour la tâche en cours.
                self.game.update(event)

                # Si l'évènement est celui de fermer la fenêtre.
                if event.type == pygame.QUIT:
                    # Fermer le jeu.
                    pygame.quit()


screen = pygame.display.set_mode((800,600))
pygame.display.set_caption('Gui Menu')
clock = pygame.time.Clock()
gui_font = pygame.font.Font(None, 30)

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 60)
text_surface = my_font.render("Le Jeu De L'Oie", 5, (255, 255, 255))

goose = pygame.image.load("assets/goose.png").convert_alpha()

button1 = Title('Start The Game', 200, 40, (100, 400), 5)

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill('#000000')
    button1.draw()
    screen.blit(text_surface, (170, 100))
    screen.blit(goose, (640, 110))
    screen.blit(goose, (90, 110))

    pygame.display.update()
    clock.tick(60)

