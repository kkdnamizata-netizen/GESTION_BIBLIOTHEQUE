from datetime import date
from database.connexion import Connexion


class GestionEmprunts:

    def __init__(self):
        self.db = Connexion()

    def verifier_date(self, valeur):
        try:
            return date.fromisoformat(str(valeur).strip())
        except (ValueError, TypeError):
            raise ValueError("Date invalide. Utilisez le format AAAA-MM-JJ (ex: 2026-12-01).")

    def emprunter_livre(self, id_livre, id_lecteur, date_emprunt, date_retour_prevue):
        try:
            debut = self.verifier_date(date_emprunt)
            fin = self.verifier_date(date_retour_prevue)

            if fin < debut:
                raise ValueError("La date de retour prévue doit être égale ou postérieure à la date d'emprunt.")

            self.db.curseur.execute("""
                SELECT quantite_disponible, titre
                FROM livres
                WHERE id_livre = ?
            """, (id_livre,))
            livre = self.db.curseur.fetchone()

            if livre is None:
                raise ValueError("Livre introuvable.")

            if livre[0] <= 0:
                raise ValueError(f"Aucun exemplaire disponible pour '{livre[1]}'.")

            self.db.curseur.execute("""
                SELECT id_lecteur, nom, prenom
                FROM lecteurs
                WHERE id_lecteur = ?
            """, (id_lecteur,))
            lecteur = self.db.curseur.fetchone()

            if lecteur is None:
                raise ValueError("Lecteur introuvable.")

            self.db.curseur.execute("""
                INSERT INTO emprunts (
                    id_livre,
                    id_lecteur,
                    date_emprunt,
                    date_retour_prevue,
                    statut
                )
                VALUES (?, ?, ?, ?, 'En cours')
            """, (
                id_livre,
                id_lecteur,
                debut.isoformat(),
                fin.isoformat()
            ))

            self.db.curseur.execute("""
                UPDATE livres
                SET quantite_disponible = quantite_disponible - 1
                WHERE id_livre = ?
                AND quantite_disponible > 0
            """, (id_livre,))

            if self.db.curseur.rowcount != 1:
                raise ValueError("Impossible de décrémenter le stock disponible.")

            self.db.connexion.commit()
            return self.db.curseur.lastrowid
        except Exception:
            self.db.connexion.rollback()
            raise

    def afficher_emprunts(self):
        self.db.curseur.execute("""
            SELECT
                e.id_emprunt,
                l.titre,
                lec.nom || ' ' || lec.prenom AS lecteur,
                e.date_emprunt,
                e.date_retour_prevue,
                e.statut,
                e.id_livre,
                e.id_lecteur
            FROM emprunts e
            JOIN livres l ON e.id_livre = l.id_livre
            JOIN lecteurs lec ON e.id_lecteur = lec.id_lecteur
            ORDER BY e.id_emprunt DESC
        """)
        return self.db.curseur.fetchall()

    def afficher_emprunts_en_cours(self):
        self.db.curseur.execute("""
            SELECT
                e.id_emprunt,
                l.titre,
                lec.nom || ' ' || lec.prenom AS lecteur,
                e.date_emprunt,
                e.date_retour_prevue,
                e.statut,
                e.id_livre,
                e.id_lecteur
            FROM emprunts e
            JOIN livres l ON e.id_livre = l.id_livre
            JOIN lecteurs lec ON e.id_lecteur = lec.id_lecteur
            WHERE e.statut = 'En cours'
            ORDER BY e.date_retour_prevue ASC
        """)
        return self.db.curseur.fetchall()

    def afficher_retards(self, date_reference=None):
        if date_reference is None:
            date_ref_str = date.today().isoformat()
        else:
            date_ref_str = self.verifier_date(date_reference).isoformat()

        self.db.curseur.execute("""
            SELECT
                e.id_emprunt,
                l.titre,
                lec.nom || ' ' || lec.prenom AS lecteur,
                e.date_emprunt,
                e.date_retour_prevue,
                e.statut,
                e.id_livre,
                e.id_lecteur
            FROM emprunts e
            JOIN livres l ON e.id_livre = l.id_livre
            JOIN lecteurs lec ON e.id_lecteur = lec.id_lecteur
            WHERE e.statut = 'En cours'
            AND e.date_retour_prevue < ?
            ORDER BY e.date_retour_prevue ASC
        """, (date_ref_str,))
        return self.db.curseur.fetchall()

    def enregistrer_retour(self, id_emprunt, date_retour=None):
        try:
            if date_retour is None:
                retour = date.today()
            else:
                retour = self.verifier_date(date_retour)

            self.db.curseur.execute("""
                SELECT id_livre, statut, date_emprunt
                FROM emprunts
                WHERE id_emprunt = ?
            """, (id_emprunt,))
            emprunt = self.db.curseur.fetchone()

            if emprunt is None:
                raise ValueError("Emprunt introuvable.")

            id_livre, statut, date_emprunt_str = emprunt
            date_emprunt = self.verifier_date(date_emprunt_str)

            if statut != "En cours":
                raise ValueError("Ce livre a déjà été retourné.")

            if retour < date_emprunt:
                raise ValueError("La date de retour ne peut pas être antérieure à la date d'emprunt.")

            self.db.curseur.execute("""
                INSERT INTO retours (
                    id_emprunt,
                    date_retour_effective
                )
                VALUES (?, ?)
            """, (id_emprunt, retour.isoformat()))

            self.db.curseur.execute("""
                UPDATE emprunts
                SET statut = 'Terminé'
                WHERE id_emprunt = ?
                AND statut = 'En cours'
            """, (id_emprunt,))

            if self.db.curseur.rowcount != 1:
                raise ValueError("Impossible de mettre à jour le statut de l'emprunt.")

            self.db.curseur.execute("""
                UPDATE livres
                SET quantite_disponible = quantite_disponible + 1
                WHERE id_livre = ?
                AND quantite_disponible < quantite_totale
            """, (id_livre,))

            self.db.connexion.commit()
        except Exception:
            self.db.connexion.rollback()
            raise

    def afficher_retours(self):
        self.db.curseur.execute("""
            SELECT
                r.id_retour,
                e.id_emprunt,
                l.titre,
                lec.nom || ' ' || lec.prenom AS lecteur,
                e.date_emprunt,
                e.date_retour_prevue,
                r.date_retour_effective
            FROM retours r
            JOIN emprunts e ON r.id_emprunt = e.id_emprunt
            JOIN livres l ON e.id_livre = l.id_livre
            JOIN lecteurs lec ON e.id_lecteur = lec.id_lecteur
            ORDER BY r.id_retour DESC
        """)
        return self.db.curseur.fetchall()

    def fermer(self):
        self.db.fermer()
