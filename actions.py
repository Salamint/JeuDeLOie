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
        self.player.effects.pop(self.tile.name, self)
    
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
        """"""
        for position, tile in self.player.game.board.tiles.items():
            if position > self.tile.index and tile.name == self.tile.name:
                self.player.goose.go_to(tile.index)


class Dices(Action):
    """
    Permet au joueur de relancer les dés.
    """

    def default(self):
        """"""
        for dice in self.player.game.dices:
            dice.roll()
        self.player.update()


class End(Action):
    """
    Met fin au jeu.
    """

    def default(self):
        """"""
        self.player.stopped = True


class Goose(Action):
    """
    Permet à une oie d'avancer une deuxième fois du nombre de cases qu'elle a déjà parcouru.
    """

    def default(self):
        """"""
        self.player.move_of(self.distance)


class Hotel(Action):
    """
    Fait passer son tour au joueur.
    """

    def activate(self):
        """"""
        self.player.stopped = True
    
    def update(self):
        self.player.stopped = False


class Jail(Action):
    """
    Le joueur doit attendre qu'un autre joueur le délivre.
    Le joueur qui délivre ne pend pas la place du joueur délivré.
    """

    queue = dict[int, 'Jail']()

    def activate(self):
        """"""
        action: Jail = Jail.queue.get(self.tile.index)
        if action is None:
            Jail.queue[self.tile.index] = self
            self.player.stopped = True
        else:
            action.player.stopped = False
            self.discard()


class Maze(Action):
    """
    Le joueur recule de 12 cases.
    """

    def default(self):
        """"""
        self.player.move_of(-12)


class Skull(Action):
    """
    Fait recommencer le joueur à 0.
    """

    def default(self):
        """"""
        self.player.goose.go_to(1)


class Well(Action):
    """
    Le joueur doit attendre qu'un autre joueur prenne sa place.
    """

    queue = dict[int, 'Well']()

    def activate(self):
        """"""
        action: Well = Well.queue.get(self.tile.index)
        if action is None:
            Well.queue[self.tile.index] = self
            self.player.stopped = True
        else:
            action.player.stopped = False
            action.discard()
            self.player.stopped = True


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
