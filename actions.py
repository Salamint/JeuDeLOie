"""
Un fichier qui contient toutes les fonctions que peuvent utiliser les oies lorsqu'elles atterrissent
sur des cases spéciales.
"""

# Import d'autres fichiers
import board
import player


# Définition des classes

class Action:
    """
    Représente une action qu'un joueur peut activer en atterrissant sur une case spéciale.
    """

    def __init__(self, distance: int, tile: 'board.Tile', p: 'player.Player'):
        """
        Construit une nouvelle instance de la classe 'Action'.
        Une action possède un nom, et permet de se souvenir de tout un tas d'informations
        nécessaires lors de l'arrivée sur la case spéciale, tel que la distance parcourue,
        la case sur laquelle se trouve le joueur et le joueur.
        """

        # La distance parcourue avant d'arriver sur la case
        self.distance = distance

        # La case actuelle où se trouve le joueur
        self.tile = tile

        # Le joueur
        self.player = p

    def activate(self) -> None:
        """
        Cette méthode est appelée lorsque le joueur vient d'arriver sur la case.
        Ceci est une méthode par défaut et ne lèvera pas d'erreur si elle n'est pas réécrite,
        même si elle est conçue pour.

        Par défaut, elle appelle la méthode par défaut, puis s'auto détruit,
        car la plupart des cases spéciales ne sont activées que lorsque le joueur arrivent dessus,
        il n'est donc, dans la plupart des cas, pas nécessaire de conserver l'action.
        """

        # Appel de la méthode par défaut
        self.default()

        # Suppression de l'action
        self.discard()

    def default(self) -> None:
        """
        Cette méthode est appelée lorsque le joueur vient d'arriver sur la case,
        et si la méthode 'activate' n'est pas réécrite.
        Elle détruira l'action après l'appel de cette méthode, si vous voulez conserver l'action,
        car elle est effective sur plusieurs tours, réécrivez la méthode 'activate'.
        """
        pass

    def discard(self) -> None:
        """
        Cette méthode supprime l'action de la liste des effets du joueur.
        """

        # Retire l'action des effets du joueur
        self.player.discard_effect(self.tile.name)
    
    def update(self) -> None:
        """
        Méthode appelée à chaque tour de jeu lorsque l'action n'est pas détruite.
        """
        pass


class Bridge(Action):
    """
    Permet de téléporter le joueur au pont suivant.
    """

    def default(self):
        """
        Action par défaut, téléporte le joueur sur la prochaine case pont.
        """

        # Itère parmi les cases et leur position
        for position, tile in self.player.game.board.tiles.items():

            # Si la position de la case est supérieure à celle du joueur
            # et que la case est un pont
            if position > self.tile.index and tile.name == self.tile.name:

                # Téléporte le joueur dessus
                self.player.goose.go_to(tile.index)


class Dices(Action):
    """
    Permet au joueur de relancer les dés.
    """

    def default(self):
        """
        Action par défaut, relance les dés et fait avancer le joueur.
        """

        # Itère parmi les dés du jeu
        for dice in self.player.game.dices:
            # Lance les dés
            dice.roll()

        # Actualise le joueur, le faisant avancer
        self.player.update()


class End(Action):
    """
    Met fin au jeu.
    """

    def default(self):
        """
        Action par défaut, stoppe le joueur
        """

        # Stoppe le joueur
        self.player.stopped = True


class Goose(Action):
    """
    Permet à une oie d'avancer une deuxième fois du nombre de cases qu'elle a déjà parcouru.
    """

    def default(self):
        """
        Action par défaut, fait avancer une deuxième fois l'oie de la distance qu'elle a parcourue.
        """

        # Fait avancer l'oie
        self.player.move_of(self.distance)


class Hotel(Action):
    """
    Fait passer son tour au joueur.
    """

    def activate(self):
        """
        Action sur plusieurs tours, stoppe le joueur.
        """

        # Stoppe le joueur
        self.player.stopped = True
    
    def update(self):
        """
        Met à jour l'action, libère le joueur, lui permettant de repartir.
        """

        # Libère le joueur
        self.player.stopped = False


class Jail(Action):
    """
    Le joueur doit attendre qu'un autre joueur le délivre.
    Le joueur qui délivre ne pend pas la place du joueur délivré.
    """

    queue = dict[int, 'Jail']()

    def activate(self):
        """
        Action sur plusieurs tours, lorsque le joueur arrive sur la case,
        l'action vérifie si une action a déjà été créé pour cette case,
        signifiant qu'un joueur en est déjà prisonnier.
        Garde le joueur prisonnier sinon.
        """

        # Essaye de récupérer l'action à la position de la case
        action: Jail = Jail.queue.get(self.tile.index)

        # Si l'action est inexistante
        if action is None:

            # Ajoute l'action dans la queue des actions
            Jail.queue[self.tile.index] = self
            # Stoppe le joueur
            self.player.stopped = True

        # Si elle existe
        else:

            # Libère le joueur
            action.player.stopped = False
            # Supprime l'action
            self.discard()


class Maze(Action):
    """
    Le joueur recule de 12 cases.
    """

    def default(self):
        """
        Action par défaut, fait reculer le joueur de 12 cases.
        """

        # Fait reculer le joueur
        self.player.move_of(-12)


class Skull(Action):
    """
    Fait recommencer le joueur à 0.
    """

    def default(self):
        """
        Action par défaut, fait recommencer le joueur du début.
        """

        # Téléporte le joueur à la première case
        self.player.goose.go_to(1)


class Well(Action):
    """
    Le joueur doit attendre qu'un autre joueur prenne sa place.
    """

    queue = dict[int, 'Well']()

    def activate(self):
        """
        Action sur plusieurs tours, lorsque le joueur arrive sur la case,
        l'action vérifie si une action a déjà été créé pour cette case,
        signifiant qu'un joueur en est déjà prisonnier,
        le libère et emprisonne le joueur arrivant.
        Garde le joueur prisonnier sinon.
        """

        # Essaye de récupérer l'action à la position de la case
        action: Well = Well.queue.get(self.tile.index)

        # Si l'action est inexistante
        if action is None:

            # Ajoute l'action dans la queue des actions
            Well.queue[self.tile.index] = self
            # Stoppe le joueur
            self.player.stopped = True

        # Si elle existe
        else:

            # Libère le joueur prisonnier
            action.player.stopped = False
            # Supprime l'ancienne action
            action.discard()
            # Emprisonne le joueur arrivant
            self.player.stopped = True


# Dictionnaire des actions par défaut
DEFAULTS: dict[str, type] = {
    'bridge': Bridge,
    'dices': Dices,
    'end': End,
    'goose': Goose,
    'hotel': Hotel,
    'jail': Jail,
    'maze': Maze,
    'skull': Skull,
    'well': Well
}
