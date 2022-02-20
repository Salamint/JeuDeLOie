"""
Jeu de l'oie en Python 3 avec la bibliothèque Pygame 2.1.2.
Ceci est un projet de NSI pour classe de Seconde Générale du lycée Ferdinand-Buisson (Voiron).
"""

# Import de 'common.py'
from common import *
import game


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
    sans pour autant utiliser la fonction 'exit' du module 'sys'.
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

        Met l'attribut `running` sur False pour stopper la boucle du jeu. Cette méthode peut être
        appelée à n'importe quel endroit du code.
        """
        self.running = False

    def start(self):
        """
        Lance la boucle du jeu.
        Le jeu tourne à 60 fps (frame per second), et chaque tour de boucle correspond à une frame.
        Donc pendant execution du jeu, il y aura 60 tours de boucle en moyenne chaque seconde.
        
        L'attribut 'running' n'est pas une variable locale donc le programme peut être arrêté
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
        """
        Construit une nouvelle instance de la classe TitleScreen.
        L'écran titre est constitué d'un titre, de boutons permettant de créer une nouvelle partie,
        et d'un menu de sélection de sauvegardes.
        """

        # Appel du constructeur de la superclasse
        super().__init__(app)

        # Images et surfaces de base.
        text = sans_font.render("Le Jeu De L'Oie", True, (255, 255, 255))
        goose = pygame.image.load("assets/goose.png").convert_alpha()

        # Crée l'image du titre et le centre sur l'écran
        title_size = (576, 64)
        self.title = pygame.Surface(title_size)
        self.title.blit(goose, (0, 0))
        self.title.blit(text, (64, -16))
        self.title.blit(goose, (title_size[0] - 64, 0))
        self.title_position = (
            center_width(title_size[0], self.app.screen.get_width()),
            title_size[1]
        )

        # Menu principal et boutons
        button_size = (256, 64)
        screen_width_center = center_width(button_size[0], self.app.screen.get_width())

        self.menu = pygame.sprite.Group()
        self.menu.add(
            PushButton("Nouvelle Partie", button_size, (screen_width_center, 384), self.play),
            PushButton("Charger", button_size, (screen_width_center, 480), self.save_select)
        )

        # Menu des sauvegardes
        self.select = False
        self.saves = pygame.sprite.Group()
        save_selector_size = (256, 384)
        self.save_selector_position = (center_width(save_selector_size[0], self.app.screen.get_width()), 192)
        self.save_selector = pygame.Surface(save_selector_size)
        self.save_selector_rect = pygame.Rect(*self.save_selector_position, *save_selector_size)

        def back():
            """
            Fonction locale temporaire, permettant de passer de l'écran de sélection des sauvegardes à l'écran
            d'accueil. N'est utilisée qu'une seule fois dans un seul attribut, d'où l'intérêt de faire de cette fonction
            une fonction locale. Equivalent d'une fonction lambda.
            """
            self.select = False

        self.back_button = PushButton("Retour", (128, 64), (128, 512), back)

        # Calculs du rectangle des bordures
        self.border_rect = self.save_selector_rect.copy()
        self.border_rect.x -= 4
        self.border_rect.y -= 4
        self.border_rect.width += 8
        self.border_rect.height += 8

    def display(self):
        """
        Affiche l'écran titre sur l'écran.

        Affiche dans tous les cas le titre du jeu, puis, si l'utilisateur se trouve dans le menu des sauvegardes,
        affiche toutes les sauvegardes disponibles, avec un bouton de retour.
        Sinon, affiche un bouton pour lancer une nouvelle partie et un bouton pour charger une partie existante.
        """

        # Affiche le titre
        screen.blit(self.title, self.title_position)

        # Si le menu de sélection des sauvegardes est ouvert
        if self.select:

            # Dessine un fond blanc pour les sauvegardes (bordure)
            pygame.draw.rect(self.app.screen, '#FFFFFF', self.border_rect)
            # Rempli le menu de sélection des sauvegardes de noir
            self.save_selector.fill('#000000')
            # Dessine les boutons de sauvegardes
            self.saves.draw(self.save_selector)

            # Affiche le menu sur l'écran
            self.app.screen.blit(self.save_selector, self.save_selector_rect)
            # Affiche le bouton de retour
            self.app.screen.blit(self.back_button.image, self.back_button.rect)

        # Si le menu de sélection des sauvegardes n'est pas ouvert (menu principal)
        else:
            # Afficher le menu principal
            self.menu.draw(self.app.screen)

    def load(self, name: str):
        """
        Charge un fichier de sauvegarde et en fait la tâche de l'application en cours.
        """

        # Charge le fichier de sauvegarde sélectionné
        with open(name, "rb") as file:
            # Charge le fichier et remplace l'application actuelle par l'objet chargé
            self.app.task = pickle.load(file, encoding="UTF-8")

    def play(self):
        """
        Crée une tâche jeu remplaçant la tâche de l'écran titre.
        """
        self.app.task = game.Game(self.app)

    def save_select(self):
        """
        Ouvre le menu de sélection de sauvegardes et crée dans le groupe de boutons de sauvegardes,
        un bouton par fichier contenu dans le répertoire des sauvegardes.
        """

        # Vide le groupe de boutons de sauvegardes
        self.saves.empty()

        # Hauteur par défaut
        height = 16

        # Pour chaque fichier ou dossier contenu dans 'data/saves'
        for file in os.listdir(access_directory(SAVES_PATH)):
            path = f"{SAVES_PATH}/{file}"

            # Si l'élément est un fichier
            if os.path.isfile(path):
                # Création et ajout d'un bouton chargeant le fichier
                self.saves.add(
                    PushButton(file, (256, 64), (0, height), lambda: self.load(path))
                )

            # Incrémente la hauteur
            height += 96

        # Indique que le menu de sélection des sauvegardes est ouvert
        self.select = True

    def update(self, event: pygame.event.Event):
        """
        Met à jour l'écran titre.
        Lorsque l'écran titre est sur le menu principal, seul les boutons principaux sont mis à jour.
        Lorsque l'écran titre est sur le menu de sélection des sauvegardes, chaque bouton de sauvegarde est
        mis à jour, et il est possible de scroller dans ce menu pour faire défiler les sauvegardes.
        """

        # Si le menu de sélection des sauvegardes est ouvert
        if self.select:

            # Si la molette de la souris est actionnée
            if event.type == pygame.MOUSEWHEEL:

                # Lorsque la molette est actionnée vers le bas
                if event.y < 0:
                    # Pour chaque bouton de sauvegarde
                    for sprite in self.saves:
                        # Défiler vers le bas
                        sprite.rect.y -= 96

                # Lorsque la molette est actionnée vers le haut
                if event.y > 0:
                    # Pour chaque bouton de sauvegarde
                    for sprite in self.saves:
                        # Défiler vers le haut
                        sprite.rect.y += 96

            # Met à jour les boutons des sauvegardes
            self.saves.update(event, self.save_selector_position)
            # Met à jour le bouton de retour
            self.back_button.update(event)

        # Si le menu de sélection des sauvegardes n'est pas ouvert (menu principal)
        else:

            # Met à jour les boutons principaux
            self.menu.update(event)


# Vérifie si ce fichier que ce fichier est exécuté et non importé.
if __name__ == '__main__':
    # Lance le programme.
    main()
    # Quitte le programme.
    sys.exit()
