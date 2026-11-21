from database .connexion import Connexion 


class GestionLecteurs :

    def __init__ (self ):
        self .db =Connexion ()

    def ajouter_lecteur (self ,lecteur ):

        try :

            if not lecteur .nom or not lecteur .nom .strip ():
                raise ValueError ("Le nom du lecteur est obligatoire.")

            if not lecteur .prenom or not lecteur .prenom .strip ():
                raise ValueError ("Le prénom du lecteur est obligatoire.")

            self .db .curseur .execute ("""
                INSERT INTO lecteurs (
                    nom,
                    prenom,
                    telephone,
                    email,
                    adresse,
                    date_inscription
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """,(
            lecteur .nom .strip (),
            lecteur .prenom .strip (),
            lecteur .telephone ,
            lecteur .email ,
            lecteur .adresse ,
            lecteur .date_inscription 
            ))

            self .db .connexion .commit ()

        except Exception :
            self .db .connexion .rollback ()
            raise 

    def afficher_lecteurs (self ):

        self .db .curseur .execute ("""
            SELECT *
            FROM lecteurs
            ORDER BY nom, prenom
        """)

        return self .db .curseur .fetchall ()

    def rechercher_lecteur (self ,nom ):

        self .db .curseur .execute ("""
            SELECT *
            FROM lecteurs
            WHERE nom LIKE ?
               OR prenom LIKE ?
            ORDER BY nom, prenom
        """,(
        "%"+nom +"%",
        "%"+nom +"%"
        ))

        return self .db .curseur .fetchall ()

    def modifier_lecteur (self ,lecteur ,id_lecteur ):

        try :

            if not lecteur .nom or not lecteur .nom .strip ():
                raise ValueError ("Le nom du lecteur est obligatoire.")

            if not lecteur .prenom or not lecteur .prenom .strip ():
                raise ValueError ("Le prénom du lecteur est obligatoire.")

            self .db .curseur .execute ("""
                UPDATE lecteurs
                SET
                    nom = ?,
                    prenom = ?,
                    telephone = ?,
                    email = ?,
                    adresse = ?
                WHERE id_lecteur = ?
            """,(
            lecteur .nom .strip (),
            lecteur .prenom .strip (),
            lecteur .telephone ,
            lecteur .email ,
            lecteur .adresse ,
            id_lecteur 
            ))

            if self .db .curseur .rowcount !=1 :
                raise ValueError ("Lecteur introuvable.")

            self .db .connexion .commit ()

        except Exception :
            self .db .connexion .rollback ()
            raise 

    def supprimer_lecteur (self ,id_lecteur ):

        try :

            self .db .curseur .execute ("""
                DELETE FROM lecteurs
                WHERE id_lecteur = ?
            """,(id_lecteur ,))

            if self .db .curseur .rowcount !=1 :
                raise ValueError ("Lecteur introuvable.")

            self .db .connexion .commit ()

        except Exception :
            self .db .connexion .rollback ()
            raise 

    def fermer (self ):

        self .db .fermer ()
