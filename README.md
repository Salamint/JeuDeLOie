# JeuDeLOie
Un jeu de l'oie fait en Python 3 avec la bibliothèque Pygame 2.1.2 !

## Sommaire

1. [Installation](#installation)
   1. [Python](#python)
   2. [Dépendances](#dépendances)
2. [Exécution](#exécution)
   1. [En ligne de commande](#en-ligne-de-commande)
      1. [Windows](#windows)
      2. [Systèmes Unix](#systmes-unix-linux--macos)
3. [Intégration](#intgration)
4. [Personnalisation](#personnalisation)
   1. [Cases simples](#cases-simples)
      1. [Structure du fichier](#structure-du-fichier-tiles)
      2. [Modifications](#modifications-tiles)
   2. [Cases spéciales](#cases-spciales)
      1. [Exemples](#exemples)
         1. [Actions temporaires](#actions-temporaires)
         2. [Actions continues](#actions-continues)
   3. [Plateau](#plateau)
      1. [Structure du fichier](#structure-du-fichier-board)
      2. [Modifications](#modifications-board)

## Installation

### Python

Ce programme tourne sur Python 3.10 et toute version de Python supérieure.
Si vous n'avez pas Python d'installé sur votre machine, rendez-vous sur la page des téléchargements du site officiel
de Python [ici](https://www.python.org/downloads/).
Suivez ensuite les consignes du programme d'installation et Python sera installé.

### Dépendances
Les librairies qui ne font pas partie de la bibliothèque standard, et dont dépend ce projet sont citées dans le fichier
```requirements.txt```, avec une version spécifiée.
Vous pouvez installer directement toutes les dépendances avec l'outil ```pip``` en entrant cette commande :
````shell
pip install -r requirements.txt
````
Si cette commande ne marche pas, c'est que ```pip``` ne se trouve pas sur votre variable d'environnement ```PATH```.
Essayez alors :
````shell
py -m pip install -r requirements.txt
````
Si vous avez plusieurs versions de python installées sur votre machine, précisez laquelle en entrant plutôt :
````shell
py -m pip3.10 install -r requirements.txt
````

## Exécution
Après installation, double-cliquez simplement sur le fichier ```main.py```, et le jeu devrait alors se lancer.
Si ce n'est pas le cas, essayez la méthode suivante.

### En ligne de commande
Il vous faudra d'abord ouvrir un terminal peu importe votre système d'exploitation.
Ensuite suivez les instructions pour chaque plateforme :

#### Windows
Sans spécifier la version :
`````shell
py main.py
`````

En spécifiant la version :
````shell
py -3.10 main.py
````

#### Systèmes Unix (Linux & MacOS)
`````shell
python3 main.py
`````

## Intégration
L'intégration dans d'autres programmes se fait aisément. En effet, grâce à la fonction ```main()```, vous pouvez très
simplement importer ce jeu dans d'autres projets. Assurez-vous seulement que le dossier du jeu se trouve dans votre
répertoire du projet, puis placez au début de votre programme :
`````python
from JeuDeLOie import main  # Importe le fichier principal 'main' du dossier du jeu.
`````
Ensuite vous pourrez l'utiliser dans tous les programmes aillant importé le jeu :
````python
main.main()                 # Lance le jeu, comme lors d'un double-clique.
````
Vous pouvez aussi créer une nouvelle instance de la classe ```Application``` pour la modifier :
````python
jeu = main.Application()    # Crée une instance d'application.
jeu.start()                 # Lance le jeu.
````


## Personnalisation

Il est possible de personnaliser le contenu du jeu pour ainsi créer votre propre plateau de jeu,
et même votre propre cases personnalisées, spéciales ou non en utilisant vos propres images,
et ce, de façon très simple !

### Cases simples

Le fichier ``tiles.json`` dans le dossier ``data`` contient toutes les definitions de cases,
et il vous suffit d'ajouter vos propres nom de cases dans le dictionnaire comme ceci :

#### Structure du fichier {#tiles}

````json5
{
  "bridge": "bridge",
  "default": null,
  "dices": "dices",
  "end": "end",
  "goose": "goose",
  "hotel": "hotel",
  "jail": "jail",
  "maze": "maze",
  "skull": "skull",
  "start": null,
  "well": "well",
  // La définition des cases personnalisées débute ici
  "custom": null
}
````

#### Modifications {#tiles}

La chaîne de caractères située après le symbole ``:`` correspond à l'action activée lorsque le joueur
va arriver sur la case, par défaut nous la mettrons sur ``null``, pour ne rien activer.

Lors du démarrage du jeu, toutes les cases seront chargées, avec une image qui porte le nom de la clé
correspondant à la case dans le dictionnaire des cases, il est donc **important** de placer
une image portant le nom de la case, de dimensions **64x64** pixels, dans le dossier ``assets/tiles``
pour ne pas créer **d'erreurs** lors du lancement du jeu.


### Cases spéciales

Les cases spéciales créent une action qui sera attribuée au joueur qui l'a activé,
permettant de créer des actions qui perdurent sur plusieurs tours.

Évidemment, ces cases sont plus difficiles à définir et nécessitent de toucher au code source du jeu.
Si vous ne souhaitez pas créer vos cases spéciales, que vous avez peur de modifier le code source,
vous pouvez passer à la rubrique suivante sans tarder.

Il vous est conseillé en premier lieu, de lire la documentation du fichier ``actions.py``
avant de modifier quoi que ce soit qui puisse mettre en péril le programme,
et vous devez posséder un minimum de connaissances en programmation Python,
ainsi qu'en Programmation Orientée Objet (OOP) en général, avant de vous essayer.

#### Exemples

Et plutôt que de vous donner de longues explications, voici quelques exemples d'actions personnalisées
que vous pourriez créer, mais il est cependant important de **lire la documentation**.

##### Actions temporaires

Pour une action qui n'est activée que lors de sa création, puis est supprimée :

````python
"""
Il est aussi important de préciser que ce code doit être écrit dans le fichier 'actions.py',
en dessous de la définition de la classe Action, ou qu'il doit être importé à un moment dans
le programme sans causer d'erreurs.
"""


# Hérite de la classe 'Action'
class TemporaryCustomAction(Action):
    """
    Action personnalisée ne s'exécutant qu'une seule fois lors de son activation.
    """

    def default(self):
        """
        Cette action est appelée par défaut et à la fin de son exécution,
        l'action est supprimée.
        """
        
        # Votre code ici
````

##### Actions continues

Pour une action qui est appelée en continu chaque tour.

````python
"""
Il est aussi important de préciser que ce code doit être écrit dans le fichier 'actions.py',
en dessous de la définition de la classe Action, ou qu'il doit être importé à un moment dans
le programme sans causer d'erreurs.
"""


# Hérite de la classe 'Action'
class ContinueCustomAction(Action):
    """
    Action personnalisée ne s'exécutant qu'une seule fois lors de son activation.
    """

    def activate(self):
        """
        Cette action est appelée à la création de l'action et permet de conserver l'action.
        """
        
        # Votre code ici

    def update(self):
        """
        Cette action est appelée à chaque tour après la méthode 'activate'.
        """
        
        # Votre code ici
````


### Plateau

Le plateau peut être modifié sans avoir recouru aux cases personnalisées,
mais permet de mettre en œuvre beaucoup de choses.

Lors du lancement du jeu, le plateau est généré à partir du fichier ``data/board.json``,
que vous pouvez modifier.

#### Structure du fichier {#board}

Regardons d'un peu plus près le contenu :

````json5
{
   // Dimensions du plateau :
   
   // Largeur
  "width": 8,
   // Hauteur
  "height": 8,
   
   // Cases du jeu, dans l'ordre de déplacement
  "tiles": [
    "start", "default", "default", "default", "default", "goose", "bridge", "default",
    "default", "goose", "default", "default", "bridge", "default", "goose", "default",
    "default",  "default", "goose", "hotel", "default", "default", "default", "goose",
    "default", "default", "dices", "goose", "default", "default", "default", "well",
    "goose", "default", "default", "default", "goose", "default", "default", "default",
    "default", "goose", "maze", "default", "default", "default", "goose", "default",
    "default", "default", "goose", "default", "jail", "dices", "goose", "default",
    "default", "default", "skull", "goose", "default", "default", "default", "end"
  ]
}
````

Que signifie *"dans l'ordre de déplacement"* ? Eh bien, cela signifie que le nom des cases tel
que vous le voyez n'est pas sous forme de spirale, à la fin de la première ligne,
un virage est créé visuellement pour faire un effet de spirale, mais les cases suivantes
seront celles de la deuxième ligne, et non celles de bord droit.

#### Modifications {#board}

Maintenant que vous savez cela, vous pouvez très facilement changer l'ordre des cases,
utiliser vos cases personnalisées en plaçant leur nom, mais le nombre total de nom de cases
dans le dictionnaire ``tiles`` doit être égal à ``width * height``, ou vous pourriez faire
face à des bugs, ou des phénomènes inattendus.

Soit dit en passant, si un nom de case ne figure pas dans le fichier ``data.tiles.json``,
une erreur sera levée.

Vous pouvez aussi faire varier les valeurs de ``width`` et ``height``,
mais si elles ne sont plus comprises entre 1 et 8, une erreur sera produite.
