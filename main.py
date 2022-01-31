"""
Jeu de l'oie en Python 3 avec la bibliothèque Pygame 2.1.2.
Ceci est un projet de NSI pour classe de Seconde Générale.
"""

# Import de 'common.py'
import pygame

import game
from common import *


# variables globales de signature (version, auteurs, license, droits...)

# Nom du jeu
__title__ = "Jeu de l'oie"
# Auteurs du jeu
__authors__ = ["CelianJok", "Nagrom850", "soh-L", "Warna38"]
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


# todo: documentation
class TitleScreen(Task):
    """
    Classe représentant l'écran de démarrage du jeu.
    """

    def __init__(self, app: Application):
        """"""
        # Appel du constructeur de la superclasse.
        super().__init__(app)

        # Images et surfaces de base.
        text = sans_font.render("Le Jeu De L'Oie", True, (255, 255, 255))
        goose = pygame.image.load("assets/goose.png").convert_alpha()

        # Titre.
        self.title = pygame.Surface((self.app.screen.get_width() - 64, 64))
        self.title.blit(goose, (0, 0))
        self.title.blit(text, (64, -16))
        self.title.blit(goose, (512, 0))
        self.title_position = (32, 64)

        # Menu principal.
        self.menu = pygame.sprite.Group()
        self.menu.add(
            PushButton("Nouvelle Partie", (256, 64), (192, 384), self.play),
            PushButton("Charger", (256, 64), (192, 480), self.save_select)
        )

        # Menu des sauvegardes.
        self.select = False
        self.saves = pygame.sprite.Group()
        self.save_selector = pygame.Surface((256, 384))
        self.save_selector_rect = pygame.Rect(192, 192, 256, 384)
        self.back_button = PushButton("Retour", (128, 64), (32, 512), self.main)

    def display(self):
        """"""
        screen.blit(self.title, self.title_position)
        if self.select:
            rect = self.save_selector_rect.copy()
            rect.x -= 4
            rect.y -= 4
            rect.width += 8
            rect.height += 8
            pygame.draw.rect(self.app.screen, '#FFFFFF', rect)
            self.save_selector.fill('#000000')
            self.saves.draw(self.save_selector)
            self.app.screen.blit(self.save_selector, self.save_selector_rect)
            self.app.screen.blit(self.back_button.image, self.back_button.rect)
        else:
            self.menu.draw(self.app.screen)

    def load(self, name: str):
        with open(name, "rb") as file:
            self.app.task = pickle.load(file, encoding="UTF-8")

    def main(self):
        self.select = False

    def play(self):
        """"""
        self.app.task = game.Game(self.app)

    def save_select(self):
        """"""
        self.saves.empty()

        height = 8
        for file in os.listdir(access_directory(SAVE_PATH)):
            path = f"{SAVE_PATH}/{file}"
            if os.path.isfile(path):
                self.saves.add(
                    PushButton(file, (256, 64), (0, height), lambda: self.load(path)))
            height += 96

        self.select = True

    def update(self, event: pygame.event.Event):
        """"""
        if self.select:
            if event.type == pygame.MOUSEWHEEL:
                if event.y < 0:
                    for sprite in self.saves:
                        sprite.rect.y -= 96
                if event.y > 0:
                    for sprite in self.saves:
                        sprite.rect.y += 96
            self.saves.update(event, (192, 192))
            self.back_button.update(event)
        else:
            self.menu.update(event)


# Vérifie si ce fichier que ce fichier est exécuté et non importé.
if __name__ == '__main__':
    # Lance le programme.
    main()
    # Quitte le programme.
    sys.exit()
