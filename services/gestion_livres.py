from database.connexion import Connexion


class GestionLivres:

    def __init__(self):
        self.db = Connexion()

    def ajouter_livre(self, livre):
        try:
            if not livre.titre or not livre.titre.strip():
                raise ValueError("Le titre du livre est obligatoire.")

            if livre.quantite_totale < 1:
                raise ValueError("La quantité totale doit être au moins égale à 1.")

            self.db.curseur.execute("""
                INSERT INTO livres (
                    titre,
                    isbn,
                    annee_publication,
                    editeur,
                    id_auteur,
                    id_categorie,
                    id_rayon,
                    quantite_totale,
                    quantite_disponible
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                livre.titre.strip(),
                livre.isbn.strip() if livre.isbn else None,
                livre.annee_publication,
                livre.editeur.strip() if livre.editeur else None,
                livre.id_auteur,
                livre.id_categorie,
                livre.id_rayon,
                livre.quantite_totale,
                livre.quantite_totale
            ))
            self.db.connexion.commit()
            return self.db.curseur.lastrowid
        except Exception:
            self.db.connexion.rollback()
            raise

    def afficher_livres(self):
        self.db.curseur.execute("""
            SELECT *
            FROM livres
            ORDER BY titre
        """)
        return self.db.curseur.fetchall()

    def afficher_livres_details(self):
        self.db.curseur.execute("""
            SELECT
                livres.id_livre,
                livres.titre,
                COALESCE(auteurs.nom || ' ' || COALESCE(auteurs.prenom, ''), 'Inconnu') AS auteur,
                COALESCE(categories.nom, 'Non classé') AS categorie,
                COALESCE(rayons.nom, 'Non assigné') AS rayon,
                livres.isbn,
                livres.annee_publication,
                livres.editeur,
                livres.quantite_totale,
                livres.quantite_disponible
            FROM livres
            LEFT JOIN auteurs ON livres.id_auteur = auteurs.id_auteur
            LEFT JOIN categories ON livres.id_categorie = categories.id_categorie
            LEFT JOIN rayons ON livres.id_rayon = rayons.id_rayon
            ORDER BY livres.titre
        """)
        return self.db.curseur.fetchall()

    def rechercher_livre(self, terme):
        recherche = f"%{terme.strip()}%"
        self.db.curseur.execute("""
            SELECT
                livres.id_livre,
                livres.titre,
                COALESCE(auteurs.nom || ' ' || COALESCE(auteurs.prenom, ''), 'Inconnu') AS auteur,
                COALESCE(categories.nom, 'Non classé') AS categorie,
                COALESCE(rayons.nom, 'Non assigné') AS rayon,
                livres.isbn,
                livres.annee_publication,
                livres.editeur,
                livres.quantite_totale,
                livres.quantite_disponible
            FROM livres
            LEFT JOIN auteurs ON livres.id_auteur = auteurs.id_auteur
            LEFT JOIN categories ON livres.id_categorie = categories.id_categorie
            LEFT JOIN rayons ON livres.id_rayon = rayons.id_rayon
            WHERE livres.titre LIKE ?
               OR livres.isbn LIKE ?
               OR auteurs.nom LIKE ?
               OR auteurs.prenom LIKE ?
               OR categories.nom LIKE ?
            ORDER BY livres.titre
        """, (recherche, recherche, recherche, recherche, recherche))
        return self.db.curseur.fetchall()

    def obtenir_livre(self, id_livre):
        self.db.curseur.execute("""
            SELECT
                livres.id_livre,
                livres.titre,
                livres.isbn,
                livres.annee_publication,
                livres.editeur,
                livres.id_auteur,
                livres.id_categorie,
                livres.id_rayon,
                livres.quantite_totale,
                livres.quantite_disponible,
                COALESCE(auteurs.nom || ' ' || COALESCE(auteurs.prenom, ''), 'Inconnu') AS auteur,
                COALESCE(categories.nom, 'Non classé') AS categorie,
                COALESCE(rayons.nom, 'Non assigné') AS rayon
            FROM livres
            LEFT JOIN auteurs ON livres.id_auteur = auteurs.id_auteur
            LEFT JOIN categories ON livres.id_categorie = categories.id_categorie
            LEFT JOIN rayons ON livres.id_rayon = rayons.id_rayon
            WHERE livres.id_livre = ?
        """, (id_livre,))
        return self.db.curseur.fetchone()

    def modifier_livre(self, livre, id_livre):
        try:
            if not livre.titre or not livre.titre.strip():
                raise ValueError("Le titre du livre est obligatoire.")

            if livre.quantite_totale < 1:
                raise ValueError("La quantité totale doit être au moins égale à 1.")

            self.db.curseur.execute("""
                SELECT COUNT(*)
                FROM emprunts
                WHERE id_livre = ?
                AND statut = 'En cours'
            """, (id_livre,))
            emprunts_en_cours = self.db.curseur.fetchone()[0]

            if livre.quantite_totale < emprunts_en_cours:
                raise ValueError(
                    f"La quantité totale ne peut pas être inférieure au nombre de livres actuellement empruntés ({emprunts_en_cours})."
                )

            quantite_disponible = livre.quantite_totale - emprunts_en_cours

            self.db.curseur.execute("""
                UPDATE livres
                SET
                    titre = ?,
                    isbn = ?,
                    annee_publication = ?,
                    editeur = ?,
                    id_auteur = ?,
                    id_categorie = ?,
                    id_rayon = ?,
                    quantite_totale = ?,
                    quantite_disponible = ?
                WHERE id_livre = ?
            """, (
                livre.titre.strip(),
                livre.isbn.strip() if livre.isbn else None,
                livre.annee_publication,
                livre.editeur.strip() if livre.editeur else None,
                livre.id_auteur,
                livre.id_categorie,
                livre.id_rayon,
                livre.quantite_totale,
                quantite_disponible,
                id_livre
            ))

            if self.db.curseur.rowcount != 1:
                raise ValueError("Livre introuvable.")

            self.db.connexion.commit()
        except Exception:
            self.db.connexion.rollback()
            raise

    def supprimer_livre(self, id_livre):
        try:
            self.db.curseur.execute("""
                SELECT COUNT(*) FROM emprunts
                WHERE id_livre = ? AND statut = 'En cours'
            """, (id_livre,))
            nb_actifs = self.db.curseur.fetchone()[0]
            if nb_actifs > 0:
                raise ValueError(f"Impossible de supprimer ce livre : {nb_actifs} emprunt(s) sont encore en cours.")

            self.db.curseur.execute("""
                DELETE FROM livres
                WHERE id_livre = ?
            """, (id_livre,))

            if self.db.curseur.rowcount != 1:
                raise ValueError("Livre introuvable.")

            self.db.connexion.commit()
        except Exception:
            self.db.connexion.rollback()
            raise

    def fermer(self):
        self.db.fermer()
