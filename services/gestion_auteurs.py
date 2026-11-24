from database.connexion import Connexion


class GestionAuteurs:

    def __init__(self):
        self.db = Connexion()

    def ajouter_auteur(self, nom, prenom=""):
        if not nom or not nom.strip():
            raise ValueError("Le nom de l'auteur est obligatoire.")
        try:
            self.db.curseur.execute("""
                INSERT INTO auteurs (nom, prenom)
                VALUES (?, ?)
            """, (nom.strip(), prenom.strip() if prenom else ""))
            self.db.connexion.commit()
            return self.db.curseur.lastrowid
        except Exception:
            self.db.connexion.rollback()
            raise

    def afficher_auteurs(self):
        self.db.curseur.execute("""
            SELECT id_auteur, nom, prenom
            FROM auteurs
            ORDER BY nom, prenom
        """)
        return self.db.curseur.fetchall()

    def afficher_auteurs_avec_stats(self):
        self.db.curseur.execute("""
            SELECT a.id_auteur, a.nom, a.prenom, COUNT(l.id_livre) as total_livres
            FROM auteurs a
            LEFT JOIN livres l ON a.id_auteur = l.id_auteur
            GROUP BY a.id_auteur
            ORDER BY a.nom, a.prenom
        """)
        return self.db.curseur.fetchall()

    def rechercher_auteur(self, texte):
        terme = f"%{texte.strip()}%"
        self.db.curseur.execute("""
            SELECT id_auteur, nom, prenom
            FROM auteurs
            WHERE nom LIKE ? OR prenom LIKE ?
            ORDER BY nom, prenom
        """, (terme, terme))
        return self.db.curseur.fetchall()

    def obtenir_auteur(self, id_auteur):
        self.db.curseur.execute("""
            SELECT id_auteur, nom, prenom
            FROM auteurs
            WHERE id_auteur = ?
        """, (id_auteur,))
        return self.db.curseur.fetchone()

    def modifier_auteur(self, id_auteur, nom, prenom=""):
        if not nom or not nom.strip():
            raise ValueError("Le nom de l'auteur est obligatoire.")
        try:
            self.db.curseur.execute("""
                UPDATE auteurs
                SET nom = ?, prenom = ?
                WHERE id_auteur = ?
            """, (nom.strip(), prenom.strip() if prenom else "", id_auteur))
            if self.db.curseur.rowcount != 1:
                raise ValueError("Auteur introuvable.")
            self.db.connexion.commit()
        except Exception:
            self.db.connexion.rollback()
            raise

    def supprimer_auteur(self, id_auteur):
        try:
            self.db.curseur.execute("""
                SELECT COUNT(*) FROM livres WHERE id_auteur = ?
            """, (id_auteur,))
            nb_livres = self.db.curseur.fetchone()[0]
            if nb_livres > 0:
                raise ValueError(f"Impossible de supprimer cet auteur : {nb_livres} livre(s) lui sont encore associé(s).")

            self.db.curseur.execute("""
                DELETE FROM auteurs
                WHERE id_auteur = ?
            """, (id_auteur,))
            if self.db.curseur.rowcount != 1:
                raise ValueError("Auteur introuvable.")
            self.db.connexion.commit()
        except Exception:
            self.db.connexion.rollback()
            raise

    def fermer(self):
        self.db.fermer()
