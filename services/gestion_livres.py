from database .connexion import Connexion 


class GestionLivres :

    def __init__ (self ):
        self .db =Connexion ()

    def ajouter_livre (self ,livre ):

        try :

            if not livre .titre or not livre .titre .strip ():
                raise ValueError ("Le titre du livre est obligatoire.")

            if livre .quantite_totale <1 :
                raise ValueError (
                "La quantité totale doit être au moins égale à 1."
                )

            self .db .curseur .execute ("""
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
            """,(
            livre .titre .strip (),
            livre .isbn ,
            livre .annee_publication ,
            livre .editeur ,
            livre .id_auteur ,
            livre .id_categorie ,
            livre .id_rayon ,
            livre .quantite_totale ,
            livre .quantite_totale 
            ))

            self .db .connexion .commit ()

        except Exception :
            self .db .connexion .rollback ()
            raise 

    def afficher_livres (self ):

        self .db .curseur .execute ("""
            SELECT *
            FROM livres
            ORDER BY titre
        """)

        return self .db .curseur .fetchall ()

    def rechercher_livre (self ,titre ):

        self .db .curseur .execute ("""
            SELECT *
            FROM livres
            WHERE titre LIKE ?
            ORDER BY titre
        """,("%"+titre +"%",))

        return self .db .curseur .fetchall ()

    def modifier_livre (self ,livre ,id_livre ):

        try :

            if not livre .titre or not livre .titre .strip ():
                raise ValueError ("Le titre du livre est obligatoire.")

            if livre .quantite_totale <1 :
                raise ValueError (
                "La quantité totale doit être au moins égale à 1."
                )

            self .db .curseur .execute ("BEGIN IMMEDIATE")

            self .db .curseur .execute ("""
                SELECT COUNT(*)
                FROM emprunts
                WHERE id_livre = ?
                AND statut = 'En cours'
            """,(id_livre ,))

            emprunts_en_cours =self .db .curseur .fetchone ()[0 ]

            if livre .quantite_totale <emprunts_en_cours :
                raise ValueError (
                "La quantité totale ne peut pas être inférieure "
                "au nombre de livres actuellement empruntés."
                )

            quantite_disponible =(
            livre .quantite_totale -emprunts_en_cours 
            )

            self .db .curseur .execute ("""
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
            """,(
            livre .titre .strip (),
            livre .isbn ,
            livre .annee_publication ,
            livre .editeur ,
            livre .id_auteur ,
            livre .id_categorie ,
            livre .id_rayon ,
            livre .quantite_totale ,
            quantite_disponible ,
            id_livre 
            ))

            if self .db .curseur .rowcount !=1 :
                raise ValueError ("Livre introuvable.")

            self .db .connexion .commit ()

        except Exception :
            self .db .connexion .rollback ()
            raise 

    def supprimer_livre (self ,id_livre ):

        try :

            self .db .curseur .execute ("""
                DELETE FROM livres
                WHERE id_livre = ?
            """,(id_livre ,))

            if self .db .curseur .rowcount !=1 :
                raise ValueError ("Livre introuvable.")

            self .db .connexion .commit ()

        except Exception :
            self .db .connexion .rollback ()
            raise 

    def fermer (self ):

        self .db .fermer ()
