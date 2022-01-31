"""
Ce fichier permet de connecter plusieurs ordinateurs
ensembles pour permettre de jouer à plusieurs au même jeu.
"""

# Import de 'common.py'
from common import *


# Définition des constantes

SAME_MACHINE = 0
LOCAL_AREA_NETWORK = 1


# Définition des classes

class Socket(socket.socket):
    """
    Une classe permettant la gestion d'un socket, hérite de la classe 'socket.socket'.

    Un `socket` est un canal de communication utilisé entre les programmes localement
    ou sur internet pour transmettre des informations dans les deux sens du canal.
    Un socket a besoin de deux informations :
     - La famille d'adresse, qui gère le format
    d'adresse (AF_INET pour IPv4, AF_INET6 pour IPv6 t AF_UNIX pour le système
    de nom de domaine Unix).
     - Le protocole pour l'échange (SOCK_DGRAM pour
    le protocole UDP, SOCK_STREAM pour le protocole TCP).

    La différence entre les protocoles TCP (Transmission Control Protocol)
    et UDP (User Datagram Protocol) est que le protocole UDP demande moins d'informations,
    mais ne demande aucune confirmation de réception, et peut donc envoyer les paquets
    dans le désordre, et les paquets perdus ne seront pas réenvoyés, contrairement
    au protocole TCP.
    """

    # Constantes permettant de différencier les sockets clients, serveurs et inutilisés
    UNUSED = 0
    SERVER = 1
    CLIENT = 2

    # Récupère l'IPv4 de la machine locale (valeur par défaut)
    ADDRESS = socket.gethostbyname(socket.gethostname())
    # Le port sur lequel vont se créer les connexions (valeur par défaut)
    PORT = 50600

    def __init__(self, address: str = None, port: int = None):
        """
        Les variables `host` et `port` ont des valeurs par défaut,
        il est conseillé de laisser la variable port par défaut, toutefois,
        si et seulement si le socket est un socket client, le paramètre `host`
        doit être changé. 

        La constante socket.AF_INET définit le format d'adressage IPv4
        (par exemple xxx.xx.x.xx), et la constante socket.SOCK_STREAM définit
        le protocole TCP (voir documentation).
        """

        # Appelle le constructeur de la classe parent (socket.socket)
        super().__init__(socket.AF_INET, socket.SOCK_STREAM)
        
        # Valeur par défaut du nom de l'hôte
        if address is None:
            address = Socket.ADDRESS
        self.address = address

        # Valeur par défaut du port
        if port is None:
            port = Socket.PORT
        self.port = port

        # Définit le socket comme inutilisé (non-serveur et non-client)
        self.connection = Socket.UNUSED
    
    def get_host(self):
        """
        Retourne un tuple (<adresse_de_l_hôte>, <port>) pour créer un serveur.
        """
        return self.address, self.port
    
    def is_used(self) -> bool:
        """"""
        return self.connection != Socket.UNUSED
    
    def set_client(self, address: str, port: int = None):
        """
        Marque ce socket comme utilisé en tant que serveur et envoie une demande de connexion
        à un serveur.
        'address' : L'adresse du serveur (IPv4).
        'port' : Le port du serveur (valeur par défaut : Socket.PORT).
        """

        # Lorsque le socket est déjà en cours d'utilisation, lève une erreur
        if self.connection != Socket.UNUSED:
            raise socket.error("Ce socket est déjà utilisé !")
        
        # Valeur par défaut du port
        if port is None:
            port = Socket.PORT

        # Se connecte au serveur
        self.connection = Socket.CLIENT
        self.connect((address, port))
    
    def set_server(self, clients: int):
        """
        Marque ce socket comme utilisé en tant que serveur et attend la demande de connexion
        de clients.
        'clients' : Un entier, correspond au nombre maximum de client qui peut se connecter.
        """
        
        # Lorsque le socket est déjà en cours d'utilisation, lève une erreur
        if self.connection != Socket.UNUSED:
            raise socket.error("Ce socket est déjà utilisé !")

        # Crée un serveur
        self.connection = Socket.SERVER
        self.bind(self.get_host())

        # Attend la demande de connexion de clients
        self.listen(clients)
