from datetime import date 

from database .connexion import Connexion 


class GestionEmprunts :

    def __init__ (self ):
        self .db =Connexion ()

    def verifier_date (self ,valeur ):

        try :
            return date .fromisoformat (valeur )

        except (ValueError ,TypeError ):
            raise ValueError (
            "Date invalide. Utilisez le format AAAA-MM-JJ."
            )

    def emprunter_livre (
    self ,
    id_livre ,
    id_lecteur ,
    date_emprunt ,
    date_retour_prevue 
    ):

        try :

            debut =self .verifier_date (date_emprunt )
            fin =self .verifier_date (date_retour_prevue )

            if fin <debut :
                raise ValueError (
                "La date de retour doit être après "
                "la date d'emprunt."
                )

            self .db .curseur .execute ("BEGIN IMMEDIATE")

            self .db .curseur .execute ("""
                SELECT quantite_disponible
                FROM livres
                WHERE id_livre = ?
            """,(id_livre ,))

            livre =self .db .curseur .fetchone ()

            if livre is None :
                raise ValueError ("Livre introuvable.")

            if livre [0 ]<=0 :
                raise ValueError (
                "Aucun exemplaire disponible."
                )

            self .db .curseur .execute ("""
                SELECT id_lecteur
                FROM lecteurs
                WHERE id_lecteur = ?
            """,(id_lecteur ,))

            lecteur =self .db .curseur .fetchone ()

            if lecteur is None :
                raise ValueError ("Lecteur introuvable.")

            self .db .curseur .execute ("""
                INSERT INTO emprunts (
                    id_livre,
                    id_lecteur,
                    date_emprunt,
                    date_retour_prevue,
                    statut
                )
                VALUES (?, ?, ?, ?, 'En cours')
            """,(
            id_livre ,
            id_lecteur ,
            date_emprunt ,
            date_retour_prevue 
            ))

            self .db .curseur .execute ("""
                UPDATE livres
                SET quantite_disponible = quantite_disponible - 1
                WHERE id_livre = ?
                AND quantite_disponible > 0
            """,(id_livre ,))

            if self .db .curseur .rowcount !=1 :
                raise ValueError (
                "Impossible de mettre à jour le stock."
                )

            self .db .connexion .commit ()

        except Exception :

            self .db .connexion .rollback ()
            raise 

    def afficher_emprunts (self ):

        self .db .curseur .execute ("""
            SELECT *
            FROM emprunts
            ORDER BY id_emprunt DESC
        """)

        return self .db .curseur .fetchall ()

    def enregistrer_retour (self ,id_emprunt ,date_retour ):

        try :

            retour =self .verifier_date (date_retour )

            if retour >date .today ():
                raise ValueError (
                "La date de retour ne peut pas être dans le futur."
                )

            self .db .curseur .execute ("BEGIN IMMEDIATE")

            self .db .curseur .execute ("""
                SELECT
                    id_livre,
                    statut,
                    date_emprunt
                FROM emprunts
                WHERE id_emprunt = ?
            """,(id_emprunt ,))

            emprunt =self .db .curseur .fetchone ()

            if emprunt is None :
                raise ValueError ("Emprunt introuvable.")

            id_livre =emprunt [0 ]
            statut =emprunt [1 ]
            date_emprunt =self .verifier_date (emprunt [2 ])

            if statut !="En cours":
                raise ValueError (
                "Ce livre a déjà été retourné."
                )

            if retour <date_emprunt :
                raise ValueError (
                "La date de retour ne peut pas être "
                "antérieure à la date d'emprunt."
                )

            self .db .curseur .execute ("""
                INSERT INTO retours (
                    id_emprunt,
                    date_retour_effective
                )
                VALUES (?, ?)
            """,(
            id_emprunt ,
            date_retour 
            ))

            self .db .curseur .execute ("""
                UPDATE emprunts
                SET statut = 'Terminé'
                WHERE id_emprunt = ?
                AND statut = 'En cours'
            """,(id_emprunt ,))

            if self .db .curseur .rowcount !=1 :
                raise ValueError (
                "Impossible de terminer cet emprunt."
                )

            self .db .curseur .execute ("""
                UPDATE livres
                SET quantite_disponible = quantite_disponible + 1
                WHERE id_livre = ?
                AND quantite_disponible < quantite_totale
            """,(id_livre ,))

            if self .db .curseur .rowcount !=1 :
                raise ValueError (
                "Impossible de mettre à jour la quantité disponible."
                )

            self .db .connexion .commit ()

        except Exception :

            self .db .connexion .rollback ()
            raise 

    def afficher_retards (self ,date_actuelle ):

        self .db .curseur .execute ("""
            SELECT *
            FROM emprunts
            WHERE statut = 'En cours'
            AND date_retour_prevue < ?
            ORDER BY date_retour_prevue
        """,(date_actuelle ,))

        return self .db .curseur .fetchall ()

    def fermer (self ):

        self .db .fermer ()
