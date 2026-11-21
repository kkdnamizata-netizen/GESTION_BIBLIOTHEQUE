import tkinter as tk 
from tkinter import ttk ,messagebox 
from datetime import date ,timedelta 

from database .connexion import Connexion 
from services .gestion_emprunts import GestionEmprunts 


class PageEmprunts :

    def __init__ (self ,parent ):

        self .parent =parent 
        self .gestion =GestionEmprunts ()
        self .db =Connexion ()

        self .livres ={}
        self .lecteurs ={}

        self .creer_interface ()
        self .charger_listes ()
        self .afficher_emprunts ()

    def creer_interface (self ):

        for element in self .parent .winfo_children ():
            element .destroy ()

        titre =tk .Label (
        self .parent ,
        text ="Gestion des emprunts",
        bg ="#F4F6F9",
        fg ="#243447",
        font =("Arial",23 ,"bold")
        )
        titre .pack (anchor ="w",padx =30 ,pady =15 )

        formulaire =tk .LabelFrame (
        self .parent ,
        text ="Enregistrer un emprunt",
        bg ="white",
        padx =15 ,
        pady =10 ,
        font =("Arial",11 ,"bold")
        )
        formulaire .pack (fill ="x",padx =30 ,pady =5 )

        tk .Label (
        formulaire ,
        text ="Livre :",
        bg ="white"
        ).grid (row =0 ,column =0 ,padx =8 ,pady =8 ,sticky ="w")

        self .liste_livres =ttk .Combobox (
        formulaire ,
        width =35 ,
        state ="readonly"
        )
        self .liste_livres .grid (row =0 ,column =1 ,padx =8 ,pady =8 )

        tk .Label (
        formulaire ,
        text ="Lecteur :",
        bg ="white"
        ).grid (row =1 ,column =0 ,padx =8 ,pady =8 ,sticky ="w")

        self .liste_lecteurs =ttk .Combobox (
        formulaire ,
        width =35 ,
        state ="readonly"
        )
        self .liste_lecteurs .grid (row =1 ,column =1 ,padx =8 ,pady =8 )

        tk .Label (
        formulaire ,
        text ="Date d'emprunt :",
        bg ="white"
        ).grid (row =0 ,column =2 ,padx =8 ,pady =8 ,sticky ="w")

        self .date_emprunt =tk .Entry (formulaire ,width =18 )
        self .date_emprunt .grid (row =0 ,column =3 ,padx =8 ,pady =8 )
        self .date_emprunt .insert (0 ,date .today ().isoformat ())

        tk .Label (
        formulaire ,
        text ="Retour prévu :",
        bg ="white"
        ).grid (row =1 ,column =2 ,padx =8 ,pady =8 ,sticky ="w")

        self .date_retour =tk .Entry (formulaire ,width =18 )
        self .date_retour .grid (row =1 ,column =3 ,padx =8 ,pady =8 )

        self .date_retour .insert (
        0 ,
        (date .today ()+timedelta (days =14 )).isoformat ()
        )

        tk .Button (
        formulaire ,
        text ="Enregistrer l'emprunt",
        bg ="#243447",
        fg ="white",
        command =self .enregistrer_emprunt 
        ).grid (row =2 ,column =0 ,columnspan =4 ,pady =12 )

        recherche =tk .Frame (
        self .parent ,
        bg ="#F4F6F9"
        )
        recherche .pack (fill ="x",padx =30 ,pady =10 )

        tk .Label (
        recherche ,
        text ="Rechercher un emprunt :",
        bg ="#F4F6F9"
        ).pack (side ="left")

        self .recherche =tk .Entry (recherche ,width =30 )
        self .recherche .pack (side ="left",padx =10 )

        tk .Button (
        recherche ,
        text ="Rechercher",
        command =self .rechercher_emprunt 
        ).pack (side ="left")

        tk .Button (
        recherche ,
        text ="Afficher tout",
        command =self .afficher_emprunts 
        ).pack (side ="left",padx =8 )

        colonnes =(
        "id",
        "livre",
        "lecteur",
        "date_emprunt",
        "date_retour",
        "statut"
        )

        self .tableau =ttk .Treeview (
        self .parent ,
        columns =colonnes ,
        show ="headings"
        )

        entetes ={
        "id":"N° Emprunt",
        "livre":"Livre",
        "lecteur":"Lecteur",
        "date_emprunt":"Date d'emprunt",
        "date_retour":"Retour prévu",
        "statut":"Statut"
        }

        for colonne ,nom in entetes .items ():

            self .tableau .heading (colonne ,text =nom )
            self .tableau .column (colonne ,width =120 )

        self .tableau .pack (
        fill ="both",
        expand =True ,
        padx =30 ,
        pady =10 
        )

    def charger_listes (self ):

        self .db .curseur .execute ("""
            SELECT id_livre, titre, quantite_disponible
            FROM livres
            WHERE quantite_disponible > 0
            ORDER BY titre
        """)

        valeurs_livres =[]
        self .livres .clear ()

        for identifiant ,titre ,quantite in self .db .curseur .fetchall ():

            affichage =(
            f"{identifiant } - {titre } "
            f"({quantite } disponible(s))"
            )

            valeurs_livres .append (affichage )
            self .livres [affichage ]=identifiant 

        self .liste_livres ["values"]=valeurs_livres 

        self .db .curseur .execute ("""
            SELECT id_lecteur, nom, prenom
            FROM lecteurs
            ORDER BY nom
        """)

        valeurs_lecteurs =[]
        self .lecteurs .clear ()

        for identifiant ,nom ,prenom in self .db .curseur .fetchall ():

            affichage =f"{identifiant } - {nom } {prenom }"

            valeurs_lecteurs .append (affichage )
            self .lecteurs [affichage ]=identifiant 

        self .liste_lecteurs ["values"]=valeurs_lecteurs 

    def enregistrer_emprunt (self ):

        try :

            livre_selectionne =self .liste_livres .get ()
            lecteur_selectionne =self .liste_lecteurs .get ()

            if not livre_selectionne or not lecteur_selectionne :
                raise ValueError (
                "Sélectionnez un livre et un lecteur."
                )

            date_debut =date .fromisoformat (
            self .date_emprunt .get ().strip ()
            )

            date_fin =date .fromisoformat (
            self .date_retour .get ().strip ()
            )

            if date_fin <date_debut :
                raise ValueError (
                "La date de retour doit être après "
                "la date d'emprunt."
                )

            id_livre =self .livres [livre_selectionne ]
            id_lecteur =self .lecteurs [lecteur_selectionne ]

            self .gestion .emprunter_livre (
            id_livre ,
            id_lecteur ,
            date_debut .isoformat (),
            date_fin .isoformat ()
            )

            messagebox .showinfo (
            "Succès",
            "Emprunt enregistré avec succès."
            )

            self .liste_livres .set ("")
            self .liste_lecteurs .set ("")

            self .charger_listes ()
            self .afficher_emprunts ()

        except Exception as erreur :

            messagebox .showerror ("Erreur",str (erreur ))

    def recuperer_emprunts (self ,terme =""):

        self .db .curseur .execute ("""
            SELECT
                emprunts.id_emprunt,
                livres.titre,
                lecteurs.nom || ' ' || lecteurs.prenom,
                emprunts.date_emprunt,
                emprunts.date_retour_prevue,
                emprunts.statut
            FROM emprunts
            INNER JOIN livres
                ON emprunts.id_livre = livres.id_livre
            INNER JOIN lecteurs
                ON emprunts.id_lecteur = lecteurs.id_lecteur
            WHERE livres.titre LIKE ?
               OR lecteurs.nom LIKE ?
               OR lecteurs.prenom LIKE ?
            ORDER BY emprunts.id_emprunt DESC
        """,(
        "%"+terme +"%",
        "%"+terme +"%",
        "%"+terme +"%"
        ))

        emprunts =self .db .curseur .fetchall ()

        resultats =[]
        aujourd_hui =date .today ().isoformat ()

        for emprunt in emprunts :

            statut =emprunt [5 ]

            if statut =="En cours"and emprunt [4 ]<aujourd_hui :
                statut ="En retard"

            resultats .append ((
            emprunt [0 ],
            emprunt [1 ],
            emprunt [2 ],
            emprunt [3 ],
            emprunt [4 ],
            statut 
            ))

        return resultats 

    def afficher_emprunts (self ):

        for ligne in self .tableau .get_children ():
            self .tableau .delete (ligne )

        for emprunt in self .recuperer_emprunts ():

            self .tableau .insert (
            "",
            tk .END ,
            values =emprunt 
            )

    def rechercher_emprunt (self ):

        terme =self .recherche .get ().strip ()

        for ligne in self .tableau .get_children ():
            self .tableau .delete (ligne )

        for emprunt in self .recuperer_emprunts (terme ):

            self .tableau .insert (
            "",
            tk .END ,
            values =emprunt 
            )

    def fermer (self ):

        self .gestion .fermer ()
        self .db .fermer ()
