from datetime import date
from database.connexion import Connexion


class GestionLecteurs:

    def __init__(self):
        self.db = Connexion()

    def ajouter_lecteur(self, lecteur):
        try:
            if not lecteur.nom or not lecteur.nom.strip():
                raise ValueError("Le nom du lecteur est obligatoire.")

            if not lecteur.prenom or not lecteur.prenom.strip():
                raise ValueError("Le prénom du lecteur est obligatoire.")

            date_insc = lecteur.date_inscription if lecteur.date_inscription else date.today().isoformat()

            self.db.curseur.execute("""
                INSERT INTO lecteurs (
                    nom,
                    prenom,
                    telephone,
                    email,
                    adresse,
                    date_inscription
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                lecteur.nom.strip(),
                lecteur.prenom.strip(),
                lecteur.telephone.strip() if lecteur.telephone else None,
                lecteur.email.strip() if lecteur.email else None,
                lecteur.adresse.strip() if lecteur.adresse else None,
                date_insc
            ))
            self.db.connexion.commit()
            return self.db.curseur.lastrowid
        except Exception:
            self.db.connexion.rollback()
            raise

    def afficher_lecteurs(self):
        self.db.curseur.execute("""
            SELECT id_lecteur, nom, prenom, telephone, email, adresse, date_inscription
            FROM lecteurs
            ORDER BY nom, prenom
        """)
        return self.db.curseur.fetchall()

    def rechercher_lecteur(self, terme):
        recherche = f"%{terme.strip()}%"
        self.db.curseur.execute("""
            SELECT id_lecteur, nom, prenom, telephone, email, adresse, date_inscription
            FROM lecteurs
            WHERE nom LIKE ?
               OR prenom LIKE ?
               OR telephone LIKE ?
               OR email LIKE ?
            ORDER BY nom, prenom
        """, (recherche, recherche, recherche, recherche))
        return self.db.curseur.fetchall()

    def obtenir_lecteur(self, id_lecteur):
        self.db.curseur.execute("""
            SELECT id_lecteur, nom, prenom, telephone, email, adresse, date_inscription
            FROM lecteurs
            WHERE id_lecteur = ?
        """, (id_lecteur,))
        return self.db.curseur.fetchone()

    def modifier_lecteur(self, lecteur, id_lecteur):
        try:
            if not lecteur.nom or not lecteur.nom.strip():
                raise ValueError("Le nom du lecteur est obligatoire.")

            if not lecteur.prenom or not lecteur.prenom.strip():
                raise ValueError("Le prénom du lecteur est obligatoire.")

            self.db.curseur.execute("""
                UPDATE lecteurs
                SET
                    nom = ?,
                    prenom = ?,
                    telephone = ?,
                    email = ?,
                    adresse = ?
                WHERE id_lecteur = ?
            """, (
                lecteur.nom.strip(),
                lecteur.prenom.strip(),
                lecteur.telephone.strip() if lecteur.telephone else None,
                lecteur.email.strip() if lecteur.email else None,
                lecteur.adresse.strip() if lecteur.adresse else None,
                id_lecteur
            ))

            if self.db.curseur.rowcount != 1:
                raise ValueError("Lecteur introuvable.")

            self.db.connexion.commit()
        except Exception:
            self.db.connexion.rollback()
            raise

    def supprimer_lecteur(self, id_lecteur):
        try:
            self.db.curseur.execute("""
                SELECT COUNT(*) FROM emprunts
                WHERE id_lecteur = ? AND statut = 'En cours'
            """, (id_lecteur,))
            nb_actifs = self.db.curseur.fetchone()[0]
            if nb_actifs > 0:
                raise ValueError(f"Impossible de supprimer ce lecteur : il a encore {nb_actifs} emprunt(s) en cours.")

            self.db.curseur.execute("""
                DELETE FROM lecteurs
                WHERE id_lecteur = ?
            """, (id_lecteur,))

            if self.db.curseur.rowcount != 1:
                raise ValueError("Lecteur introuvable.")

            self.db.connexion.commit()
        except Exception:
            self.db.connexion.rollback()
            raise

    def fermer(self):
        self.db.fermer()
