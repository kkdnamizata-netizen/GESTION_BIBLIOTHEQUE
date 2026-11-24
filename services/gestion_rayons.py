from database.connexion import Connexion


class GestionRayons:

    def __init__(self):
        self.db = Connexion()

    def ajouter_rayon(self, nom, description=""):
        if not nom or not nom.strip():
            raise ValueError("Le nom du rayon est obligatoire.")
        try:
            self.db.curseur.execute("""
                INSERT INTO rayons (nom, description)
                VALUES (?, ?)
            """, (nom.strip(), description.strip() if description else ""))
            self.db.connexion.commit()
            return self.db.curseur.lastrowid
        except Exception:
            self.db.connexion.rollback()
            raise

    def afficher_rayons(self):
        self.db.curseur.execute("""
            SELECT id_rayon, nom, description
            FROM rayons
            ORDER BY nom
        """)
        return self.db.curseur.fetchall()

    def afficher_rayons_avec_stats(self):
        self.db.curseur.execute("""
            SELECT r.id_rayon, r.nom, r.description, COUNT(l.id_livre) as total_livres
            FROM rayons r
            LEFT JOIN livres l ON r.id_rayon = l.id_rayon
            GROUP BY r.id_rayon
            ORDER BY r.nom
        """)
        return self.db.curseur.fetchall()

    def rechercher_rayon(self, texte):
        terme = f"%{texte.strip()}%"
        self.db.curseur.execute("""
            SELECT id_rayon, nom, description
            FROM rayons
            WHERE nom LIKE ? OR description LIKE ?
            ORDER BY nom
        """, (terme, terme))
        return self.db.curseur.fetchall()

    def obtenir_rayon(self, id_rayon):
        self.db.curseur.execute("""
            SELECT id_rayon, nom, description
            FROM rayons
            WHERE id_rayon = ?
        """, (id_rayon,))
        return self.db.curseur.fetchone()

    def modifier_rayon(self, id_rayon, nom, description=""):
        if not nom or not nom.strip():
            raise ValueError("Le nom du rayon est obligatoire.")
        try:
            self.db.curseur.execute("""
                UPDATE rayons
                SET nom = ?, description = ?
                WHERE id_rayon = ?
            """, (nom.strip(), description.strip() if description else "", id_rayon))
            if self.db.curseur.rowcount != 1:
                raise ValueError("Rayon introuvable.")
            self.db.connexion.commit()
        except Exception:
            self.db.connexion.rollback()
            raise

    def supprimer_rayon(self, id_rayon):
        try:
            self.db.curseur.execute("""
                SELECT COUNT(*) FROM livres WHERE id_rayon = ?
            """, (id_rayon,))
            nb_livres = self.db.curseur.fetchone()[0]
            if nb_livres > 0:
                raise ValueError(f"Impossible de supprimer ce rayon : {nb_livres} livre(s) y sont placés.")

            self.db.curseur.execute("""
                DELETE FROM rayons
                WHERE id_rayon = ?
            """, (id_rayon,))
            if self.db.curseur.rowcount != 1:
                raise ValueError("Rayon introuvable.")
            self.db.connexion.commit()
        except Exception:
            self.db.connexion.rollback()
            raise

    def fermer(self):
        self.db.fermer()
