import sqlite3 


class Connexion :

    def __init__ (self ):

        self .connexion =sqlite3 .connect (
        "database/bibliotheque.db",
        timeout =10 
        )

        self .curseur =self .connexion .cursor ()

        self .curseur .execute (
        "PRAGMA foreign_keys = ON"
        )

    def fermer (self ):

        self .connexion .close ()
