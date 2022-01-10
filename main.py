"""
Jeu de l'oie en Python 3 avec la bibliothèque Pygame 2.1.0.
Ceci est un projet de NSI pour classe de Seconde Générale.
"""

# Import de 'common.py'
from common import *

# Import des autres fichiers
import game


# variables globales de signature (version, auteurs, license, droits...)

# Nom du jeu
__title__ = "Jeu de l'oie"
# Auteurs du jeu
__authors__ = []
# License du jeu
__license__ = "MIT License"
# Version du jeu
__version__ = "0.0.0"


# Définition des fonctions

def main():
    """
    La fonction 'main' est le point d'entrée du programme.
    C'est ici que va être lancé le jeu, et lorsqu'une erreur survient,
    elle est écrite dans le fichier `debug.log` (peut être ouvert avec le bloc-note).

    Cette directive permet de se servir du bloc `if __name__ == '__main__'`
    pour ne pas lancer le jeu lorsque ce fichier est importé,
    mais permet d'utiliser la fonction `main` dans d'autres programmes,
    sans pour autant utiliser `sys.exit`.
    """

    # Crée une nouvelle instance de `Application`
    application = Application()
    # Démarre l'application
    application.start()


# Définition des classes

class Application:
    """
    Une classe représentant une application.
    Cette classe est le point de départ du programme,
    appeler sa méthode `start` la lance.
    """

    def __init__(self):
        """"""
        self.screen = screen
        self.running = True

        # Change le titre de l'application
        pygame.display.set_caption(__title__)
        # Change l'icone de l'application
        pygame.display.set_icon(pygame.image.load("assets/goose.png").convert_alpha())

        self.clock = pygame.time.Clock()
        self.game = game.Game(self)

    def display(self):
        """
        Met à jour l'affichage (affiche sur l'écran tous les groupes de sprites et sprites).
        """
        self.game.display()

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
        
        La variable `self.running` n'est pas une variable locale donc le programme peut être arrêté
        à n'importe quel moment, mais il est recommandé d'utiliser la méthode `self.quit`.

        A chaque tour de boucle, tous les éléments graphiques (sprites, groupes de sprites)
        sont affichés à l'écran, puis l'écran est rafraîchi pour faire apparaitre les changements,
        et enfin on met à jour tous les composants pour chaque évènement récupéré.

        L'appel à la méthode `self.clock.tick(60)` permet de régler le jeu sur 60 fps,
        sans cet appel, le jeu dépasserait les 60 fps, donc la boucle s'exécuterait plus de 60
        fois par secondes. Cela peut causer des ralentissements, épuiser les ressources de la machine,
        ainsi que créer des décalages entre différentes machines.
        """

        # Tant que le jeu est lancé (un tour de boucle par frame)
        while self.running:

            # Met à jour l'affichage
            self.display()
            # Met à jour tous les écrans de pygame
            pygame.display.flip()
            
            # Capture tous les évènements (click, appui sur une touche...) de la frame actuelle
            for event in pygame.event.get():

                # Met à jour le jeu
                self.update(event)
                
                # Si l'évènement est celui de cliquer sur la croix
                if event.type == pygame.QUIT:
                    # Fermer le jeu
                    self.quit()
            
            # Régule le jeu à 60 fps
            self.clock.tick(144)
    
    def update(self, event: pygame.event.Event):
        self.game.update(event)


# Vérifie si ce fichier n'est pas importé
if __name__ == '__main__':
    # Lance le programme
    main()
    # Quitte le programme
    sys.exit()
