"""
Jeu de l'oie en Python 3 avec la bibliothèque Pygame 2.1.2.
Ceci est un projet de NSI pour classe de Seconde Générale.
"""

# Import de 'common.py'
import game
from common import *


# variables globales de signature (version, auteurs, license, droits...)

# Nom du jeu
__title__ = "Jeu de l'oie"
# Auteurs du jeu
__authors__ = ["CelianJok", "soh-L", "Warna38", "Nagrom850"]
# License du jeu
__license__ = "MIT License"
# Version du jeu
__version__ = "0.0.0"


# Définition des fonctions

def main():
    """
    La fonction 'main' est le point d'entrée du programme.
    C'est ici que va être lancé le jeu.

    Cette directive permet de se servir du bloc `if __name__ == '__main__'`
    pour ne pas lancer le jeu lorsque ce fichier est importé,
    mais permet d'utiliser la fonction `main` dans d'autres programmes,
    sans pour autant utiliser 'sys.exit'.
    """

    # Crée une nouvelle instance de `Application`
    application = Application()
    # Démarre l'application
    application.start()


# Définition des classes

class Application(Application):
    """
    Une classe représentant une application.
    Cette classe est le point de départ du programme,
    appeler sa méthode `start` la lance.
    """

    def __init__(self):
        """
        Initialise une nouvelle application.
        Récupère l'écran global dans common, change le titre par le titre du programme
        et change l'icône de la fenêtre.
        """

        # Appelle le constructeur de la super classe
        super().__init__(screen, TitleScreen)
        # Stoppe le jeu
        self.running = False

        # Change le titre de l'application
        pygame.display.set_caption(__title__)
        # Change l'icône de l'application
        pygame.display.set_icon(pygame.image.load("assets/goose.png").convert_alpha())

        self.clock = pygame.time.Clock()

    def display(self):
        """
        Met à jour l'affichage (affiche sur l'écran tous les groupes de sprites et sprites).
        """
        self.screen.fill((0, 0, 0))
        self.task.display()

    def quit(self):
        """
        Quitte le jeu.

        Met la variable `self.running` sur False pour stopper la boucle du jeu. Cette méthode peut être
        appelée à n'importe quel endroit du code.
        """
        self.running = False

    def start(self):
        """
        Lance la boucle du jeu.
        Le jeu tourne à 60 fps (frame per second), et chaque tour de boucle correspond à une frame.
        Donc pendant execution du jeu, il y aura 60 tours de boucle en moyenne chaque seconde.
        
        La variable 'self.running' n'est pas une variable locale donc le programme peut être arrêté
        à n'importe quel moment, mais il est recommandé d'utiliser la méthode 'self.quit'.

        À chaque tour de boucle, tous les éléments graphiques (sprites, groupes de sprites)
        sont affichés à l'écran, puis l'écran est rafraîchi pour faire apparaitre les changements,
        et enfin on met à jour tous les composants pour chaque évènement récupéré.

        L'appel à la méthode `self.clock.tick(60)` permet de régler le jeu sur 60 fps,
        sans cet appel, le jeu dépasserait les 60 fps, donc la boucle s'exécuterait plus de 60
        fois par secondes. Cela peut causer des ralentissements, épuiser les ressources de la machine,
        ainsi que créer des décalages entre différentes machines.
        """

        # Démarre le jeu
        self.running = True

        # Tant que le jeu est lancé (un tour de boucle par frame).
        while self.running:

            # Met à jour l'affichage.
            self.display()
            # Met à jour tous les écrans de pygame.
            pygame.display.flip()
            
            # Capture tous les évènements (click, appui sur une touche...) de la frame actuelle.
            for event in pygame.event.get():

                # Met à jour la tâche en cours.
                self.task.update(event)
                
                # Si l'évènement est celui de fermer la fenêtre.
                if event.type == pygame.QUIT:
                    # Fermer le jeu.
                    self.quit()
            
            # Régule le jeu à 60 fps.
            self.clock.tick(144)


class TitleScreen(Task):
    """
    Classe représentant l'écran de démarrage du jeu.
    """

    def __init__(self, app: Application):

        self.pos = (100, 400)
        self.text_surface = sans_font.render("Le Jeu De L'Oie", True, (255, 255, 255))
        self.goose = pygame.image.load("assets/goose.png").convert_alpha()

        # Core attributes
        super().__init__(app)
        self.pressed = False
        self.elevation = 5
        self.dynamic_elevation = self.elevation
        self.original_y_pos = self.pos[1]

        # top rectangle
        self.top_rect = pygame.Rect(self.pos, (200, 40))
        self.top_color = '#475F77'

        # bottom rectangle
        self.bottom_rect = pygame.Rect(self.pos, (200, 40))
        self.bottom_color = '#354B5E'
        # text
        self.text_surf = default_font.render("Start The Game", True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect()

    def display(self):
        """"""
        self.top_rect.y = self.original_y_pos - self.dynamic_elevation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elevation

        pygame.draw.rect(screen, self.bottom_color, self.bottom_rect, border_radius=12)
        pygame.draw.rect(screen, self.top_color, self.top_rect, border_radius=12)
        screen.blit(self.text_surf, self.text_rect)

        screen.blit(self.text_surface, (170, 100))
        screen.blit(self.goose, (640, 110))
        screen.blit(self.goose, (90, 110))

    def update(self, event: pygame.event.Event):
        """"""
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#D74B4B'
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == pygame.BUTTON_LEFT:
                self.dynamic_elevation = 0
                self.pressed = True
                self.app.task = game.Game(self.app)
            else:
                self.dynamic_elevation = self.elevation
                if self.pressed is True:
                    self.display()
                    self.pressed = False
        else:
            self.dynamic_elevation = self.elevation
            self.top_color = '#475F77'


# Vérifie si ce fichier que ce fichier est exécuté et non importé.
if __name__ == '__main__':
    # Lance le programme.
    main()
    # Quitte le programme.
    sys.exit()
