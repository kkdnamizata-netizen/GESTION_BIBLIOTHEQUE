import tkinter as tk 
from tkinter import ttk ,messagebox 
from datetime import date 

from database .connexion import Connexion 
from services .gestion_emprunts import GestionEmprunts 


class PageRetours :

    def __init__ (self ,parent ):

        self .parent =parent 
        self .gestion =GestionEmprunts ()
        self .db =Connexion ()

        self .creer_interface ()
        self .afficher_emprunts ()

    def creer_interface (self ):

        for element in self .parent .winfo_children ():
            element .destroy ()

        titre =tk .Label (
        self .parent ,
        text ="Gestion des retours",
        bg ="#F4F6F9",
        fg ="#243447",
        font =("Arial",23 ,"bold")
        )
        titre .pack (anchor ="w",padx =30 ,pady =20 )

        description =tk .Label (
        self .parent ,
        text ="Consultez les emprunts en cours et enregistrez les retours.",
        bg ="#F4F6F9",
        fg ="#555555",
        font =("Arial",11 )
        )
        description .pack (anchor ="w",padx =30 ,pady =5 )

        recherche =tk .Frame (
        self .parent ,
        bg ="#F4F6F9"
        )
        recherche .pack (fill ="x",padx =30 ,pady =15 )

        tk .Label (
        recherche ,
        text ="Rechercher :",
        bg ="#F4F6F9"
        ).pack (side ="left")

        self .recherche =tk .Entry (
        recherche ,
        width =30 
        )
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
        "etat"
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
        "etat":"État"
        }

        for colonne ,nom in entetes .items ():

            self .tableau .heading (
            colonne ,
            text =nom 
            )

            self .tableau .column (
            colonne ,
            width =125 
            )

        self .tableau .pack (
        fill ="both",
        expand =True ,
        padx =30 ,
        pady =10 
        )

        tk .Button (
        self .parent ,
        text ="Enregistrer le retour du livre sélectionné",
        bg ="#287A55",
        fg ="white",
        font =("Arial",11 ,"bold"),
        command =self .enregistrer_retour 
        ).pack (
        anchor ="e",
        padx =30 ,
        pady =15 
        )

    def afficher_emprunts (self ):

        for ligne in self .tableau .get_children ():
            self .tableau .delete (ligne )

        self .db .curseur .execute ("""
            SELECT
                emprunts.id_emprunt,
                livres.titre,
                lecteurs.nom || ' ' || lecteurs.prenom,
                emprunts.date_emprunt,
                emprunts.date_retour_prevue
            FROM emprunts
            INNER JOIN livres
                ON emprunts.id_livre = livres.id_livre
            INNER JOIN lecteurs
                ON emprunts.id_lecteur = lecteurs.id_lecteur
            WHERE emprunts.statut = 'En cours'
            ORDER BY emprunts.date_retour_prevue
        """)

        emprunts =self .db .curseur .fetchall ()

        aujourd_hui =date .today ().isoformat ()

        for emprunt in emprunts :

            if emprunt [4 ]<aujourd_hui :
                etat ="En retard"
            else :
                etat ="En cours"

            self .tableau .insert (
            "",
            tk .END ,
            values =(
            emprunt [0 ],
            emprunt [1 ],
            emprunt [2 ],
            emprunt [3 ],
            emprunt [4 ],
            etat 
            )
            )

    def rechercher_emprunt (self ):

        terme =self .recherche .get ().strip ()

        for ligne in self .tableau .get_children ():
            self .tableau .delete (ligne )

        self .db .curseur .execute ("""
            SELECT
                emprunts.id_emprunt,
                livres.titre,
                lecteurs.nom || ' ' || lecteurs.prenom,
                emprunts.date_emprunt,
                emprunts.date_retour_prevue
            FROM emprunts
            INNER JOIN livres
                ON emprunts.id_livre = livres.id_livre
            INNER JOIN lecteurs
                ON emprunts.id_lecteur = lecteurs.id_lecteur
            WHERE emprunts.statut = 'En cours'
            AND (
                livres.titre LIKE ?
                OR lecteurs.nom LIKE ?
                OR lecteurs.prenom LIKE ?
            )
            ORDER BY emprunts.date_retour_prevue
        """,(
        '%'+terme +'%',
        '%'+terme +'%',
        '%'+terme +'%'
        ))

        aujourd_hui =date .today ().isoformat ()

        for emprunt in self .db .curseur .fetchall ():

            if emprunt [4 ]<aujourd_hui :
                etat ="En retard"
            else :
                etat ="En cours"

            self .tableau .insert (
            "",
            tk .END ,
            values =(
            emprunt [0 ],
            emprunt [1 ],
            emprunt [2 ],
            emprunt [3 ],
            emprunt [4 ],
            etat 
            )
            )

    def enregistrer_retour (self ):

        selection =self .tableau .selection ()

        if not selection :

            messagebox .showwarning (
            "Attention",
            "Sélectionnez un emprunt dans le tableau."
            )
            return 

        confirmation =messagebox .askyesno (
        "Confirmation",
        "Confirmez-vous le retour de ce livre ?"
        )

        if confirmation :

            valeurs =self .tableau .item (
            selection [0 ]
            )["values"]

            id_emprunt =valeurs [0 ]

            try :

                self .gestion .enregistrer_retour (
                id_emprunt ,
                date .today ().isoformat ()
                )

                messagebox .showinfo (
                "Succès",
                "Le retour du livre a été enregistré."
                )

                self .afficher_emprunts ()

            except Exception as erreur :

                messagebox .showerror (
                "Erreur",
                str (erreur )
                )

    def fermer (self ):

        self .gestion .fermer ()
        self .db .fermer ()
