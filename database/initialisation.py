from database.connexion import Connexion


class Initialisation:

    def __init__(self):
        self.db = Connexion()

    def creer_tables(self):

        self.db.curseur.execute("""
            CREATE TABLE IF NOT EXISTS auteurs (
                id_auteur INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                prenom TEXT
            )
        """)

        self.db.curseur.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                id_categorie INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT UNIQUE NOT NULL
            )
        """)

        self.db.curseur.execute("""
            CREATE TABLE IF NOT EXISTS rayons (
                id_rayon INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT UNIQUE NOT NULL,
                description TEXT
            )
        """)

        self.db.curseur.execute("""
            CREATE TABLE IF NOT EXISTS livres (
                id_livre INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                isbn TEXT UNIQUE,
                annee_publication INTEGER,
                editeur TEXT,
                id_auteur INTEGER,
                id_categorie INTEGER,
                id_rayon INTEGER,
                quantite_totale INTEGER DEFAULT 1,
                quantite_disponible INTEGER DEFAULT 1,

                FOREIGN KEY (id_auteur)
                    REFERENCES auteurs(id_auteur),

                FOREIGN KEY (id_categorie)
                    REFERENCES categories(id_categorie),

                FOREIGN KEY (id_rayon)
                    REFERENCES rayons(id_rayon)
            )
        """)

        self.db.curseur.execute("""
            CREATE TABLE IF NOT EXISTS lecteurs (
                id_lecteur INTEGER PRIMARY KEY AUTOINCREMENT,
                nom TEXT NOT NULL,
                prenom TEXT NOT NULL,
                telephone TEXT,
                email TEXT UNIQUE,
                adresse TEXT,
                date_inscription TEXT NOT NULL
            )
        """)

        self.db.curseur.execute("""
            CREATE TABLE IF NOT EXISTS emprunts (
                id_emprunt INTEGER PRIMARY KEY AUTOINCREMENT,
                id_livre INTEGER NOT NULL,
                id_lecteur INTEGER NOT NULL,
                date_emprunt TEXT NOT NULL,
                date_retour_prevue TEXT NOT NULL,
                statut TEXT DEFAULT 'En cours',

                FOREIGN KEY (id_livre)
                    REFERENCES livres(id_livre),

                FOREIGN KEY (id_lecteur)
                    REFERENCES lecteurs(id_lecteur)
            )
        """)

        self.db.curseur.execute("""
            CREATE TABLE IF NOT EXISTS retours (
                id_retour INTEGER PRIMARY KEY AUTOINCREMENT,
                id_emprunt INTEGER NOT NULL UNIQUE,
                date_retour_effective TEXT NOT NULL,

                FOREIGN KEY (id_emprunt)
                    REFERENCES emprunts(id_emprunt)
            )
        """)

        self.db.connexion.commit()

    def fermer(self):
        self.db.fermer()
