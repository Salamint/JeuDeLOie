"""
Jeu de l'oie en Python 3 avec la bibliothèque Pygame 2.1.0.
Ceci est un projet de NSI pour classe de Seconde Générale.
"""

# Import de 'common.py'
from common import *

# Nom du jeu
__title__ = "jeu de l'oie"
# Auteurs du jeu
__authors__ = []
# License du jeu
__license__ = "GPL 3.0"
# Version du jeu
__version__ = "0.0.0"


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


class Application:
    """
    Une classe représentant une application.
    Cette classe est le point de départ du programme,
    appeler sa méthode `start` la lance.
    """

    def __init__(self):
        """"""
        self.running = True

    def quit(self):
        """"""
        self.running = False

    def start(self):
        """"""

        while self.running:

            pygame.display.flip()

            for event in pygame.event.get():

                if event.type == pygame.QUIT:

                    self.quit()


# Vérifie si ce fichier n'est pas importé
if __name__ == '__main__':
    # Lance le programme
    main()
    # Quitte le programme
    sys.exit()
