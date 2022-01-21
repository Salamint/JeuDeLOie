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
L'intégration dans d'autres programmes se fait aisément.
