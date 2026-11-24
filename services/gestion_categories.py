from database.connexion import Connexion


class GestionCategories:

    def __init__(self):
        self.db = Connexion()

    def ajouter_categorie(self, nom):
        if not nom or not nom.strip():
            raise ValueError("Le nom de la catégorie est obligatoire.")
        try:
            self.db.curseur.execute("""
                INSERT INTO categories (nom)
                VALUES (?)
            """, (nom.strip(),))
            self.db.connexion.commit()
            return self.db.curseur.lastrowid
        except Exception:
            self.db.connexion.rollback()
            raise

    def afficher_categories(self):
        self.db.curseur.execute("""
            SELECT id_categorie, nom
            FROM categories
            ORDER BY nom
        """)
        return self.db.curseur.fetchall()

    def afficher_categories_avec_stats(self):
        self.db.curseur.execute("""
            SELECT c.id_categorie, c.nom, COUNT(l.id_livre) as total_livres
            FROM categories c
            LEFT JOIN livres l ON c.id_categorie = l.id_categorie
            GROUP BY c.id_categorie
            ORDER BY c.nom
        """)
        return self.db.curseur.fetchall()

    def rechercher_categorie(self, texte):
        terme = f"%{texte.strip()}%"
        self.db.curseur.execute("""
            SELECT id_categorie, nom
            FROM categories
            WHERE nom LIKE ?
            ORDER BY nom
        """, (terme,))
        return self.db.curseur.fetchall()

    def obtenir_categorie(self, id_categorie):
        self.db.curseur.execute("""
            SELECT id_categorie, nom
            FROM categories
            WHERE id_categorie = ?
        """, (id_categorie,))
        return self.db.curseur.fetchone()

    def modifier_categorie(self, id_categorie, nom):
        if not nom or not nom.strip():
            raise ValueError("Le nom de la catégorie est obligatoire.")
        try:
            self.db.curseur.execute("""
                UPDATE categories
                SET nom = ?
                WHERE id_categorie = ?
            """, (nom.strip(), id_categorie))
            if self.db.curseur.rowcount != 1:
                raise ValueError("Catégorie introuvable.")
            self.db.connexion.commit()
        except Exception:
            self.db.connexion.rollback()
            raise

    def supprimer_categorie(self, id_categorie):
        try:
            self.db.curseur.execute("""
                SELECT COUNT(*) FROM livres WHERE id_categorie = ?
            """, (id_categorie,))
            nb_livres = self.db.curseur.fetchone()[0]
            if nb_livres > 0:
                raise ValueError(f"Impossible de supprimer cette catégorie : {nb_livres} livre(s) y sont rattaché(s).")

            self.db.curseur.execute("""
                DELETE FROM categories
                WHERE id_categorie = ?
            """, (id_categorie,))
            if self.db.curseur.rowcount != 1:
                raise ValueError("Catégorie introuvable.")
            self.db.connexion.commit()
        except Exception:
            self.db.connexion.rollback()
            raise

    def fermer(self):
        self.db.fermer()
