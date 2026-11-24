import os
import sqlite3


class Connexion:

    def __init__(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        db_path = os.path.join(base_dir, "database", "bibliotheque.db")

        self.connexion = sqlite3.connect(
            db_path,
            timeout=10
        )

        self.curseur = self.connexion.cursor()

        self.curseur.execute(
            "PRAGMA foreign_keys = ON"
        )

    def fermer(self):
        self.connexion.close()
