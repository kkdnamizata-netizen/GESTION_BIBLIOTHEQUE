import tkinter as tk 
from tkinter import ttk ,messagebox 
from datetime import date 

from models .lecteur import Lecteur 
from services .gestion_lecteurs import GestionLecteurs 
from database .connexion import Connexion 


class PageLecteurs :

    def __init__ (self ,parent ):

        self .parent =parent 
        self .gestion =GestionLecteurs ()
        self .db =Connexion ()
        self .id_selectionne =None 

        self .creer_interface ()
        self .afficher_lecteurs ()

    def creer_interface (self ):

        for element in self .parent .winfo_children ():
            element .destroy ()

        titre =tk .Label (
        self .parent ,
        text ="Gestion des lecteurs",
        bg ="#F4F6F9",
        fg ="#243447",
        font =("Arial",23 ,"bold")
        )
        titre .pack (anchor ="w",padx =30 ,pady =15 )

        formulaire =tk .LabelFrame (
        self .parent ,
        text ="Informations du lecteur",
        bg ="white",
        padx =15 ,
        pady =10 ,
        font =("Arial",11 ,"bold")
        )
        formulaire .pack (fill ="x",padx =30 ,pady =5 )

        self .champs ={}

        informations =[
        ("Nom","nom"),
        ("Prénom","prenom"),
        ("Téléphone","telephone"),
        ("Email","email"),
        ("Adresse","adresse")
        ]

        for i ,(nom ,cle )in enumerate (informations ):

            ligne =i //2 
            colonne =(i %2 )*2 

            tk .Label (
            formulaire ,
            text =nom ,
            bg ="white"
            ).grid (
            row =ligne ,
            column =colonne ,
            padx =8 ,
            pady =5 ,
            sticky ="w"
            )

            champ =tk .Entry (formulaire ,width =25 )

            champ .grid (
            row =ligne ,
            column =colonne +1 ,
            padx =8 ,
            pady =5 
            )

            self .champs [cle ]=champ 

        boutons =tk .Frame (formulaire ,bg ="white")
        boutons .grid (row =3 ,column =0 ,columnspan =4 ,pady =10 )

        tk .Button (
        boutons ,
        text ="Ajouter",
        bg ="#243447",
        fg ="white",
        command =self .ajouter_lecteur 
        ).pack (side ="left",padx =5 )

        tk .Button (
        boutons ,
        text ="Modifier",
        bg ="#287A55",
        fg ="white",
        command =self .modifier_lecteur 
        ).pack (side ="left",padx =5 )

        tk .Button (
        boutons ,
        text ="Vider",
        command =self .vider_champs 
        ).pack (side ="left",padx =5 )

        recherche =tk .Frame (self .parent ,bg ="#F4F6F9")
        recherche .pack (fill ="x",padx =30 ,pady =8 )

        tk .Label (
        recherche ,
        text ="Rechercher un lecteur :",
        bg ="#F4F6F9"
        ).pack (side ="left")

        self .recherche =tk .Entry (recherche ,width =30 )
        self .recherche .pack (side ="left",padx =10 )

        tk .Button (
        recherche ,
        text ="Rechercher",
        command =self .rechercher_lecteur 
        ).pack (side ="left")

        tk .Button (
        recherche ,
        text ="Afficher tout",
        command =self .afficher_lecteurs 
        ).pack (side ="left",padx =8 )

        colonnes =(
        "id","nom","prenom","telephone",
        "email","adresse","date",
        "emprunts","retards"
        )

        self .tableau =ttk .Treeview (
        self .parent ,
        columns =colonnes ,
        show ="headings"
        )

        entetes ={
        "id":"ID",
        "nom":"Nom",
        "prenom":"Prénom",
        "telephone":"Téléphone",
        "email":"Email",
        "adresse":"Adresse",
        "date":"Inscription",
        "emprunts":"En cours",
        "retards":"En retard"
        }

        for colonne ,nom in entetes .items ():
            self .tableau .heading (colonne ,text =nom )
            self .tableau .column (colonne ,width =100 )

        self .tableau .pack (
        fill ="both",
        expand =True ,
        padx =30 ,
        pady =8 
        )

        self .tableau .bind (
        "<<TreeviewSelect>>",
        self .selectionner_lecteur 
        )

        tk .Button (
        self .parent ,
        text ="Supprimer le lecteur sélectionné",
        bg ="#B83232",
        fg ="white",
        command =self .supprimer_lecteur 
        ).pack (anchor ="e",padx =30 ,pady =8 )

    def recuperer_lecteurs (self ,terme =""):

        aujourd_hui =date .today ().isoformat ()

        self .db .curseur .execute ("""
            SELECT
                lecteurs.id_lecteur,
                lecteurs.nom,
                lecteurs.prenom,
                lecteurs.telephone,
                lecteurs.email,
                lecteurs.adresse,
                lecteurs.date_inscription,

                SUM(
                    CASE
                        WHEN emprunts.statut = 'En cours'
                        THEN 1 ELSE 0
                    END
                ),

                SUM(
                    CASE
                        WHEN emprunts.statut = 'En cours'
                        AND emprunts.date_retour_prevue < ?
                        THEN 1 ELSE 0
                    END
                )

            FROM lecteurs

            LEFT JOIN emprunts
                ON lecteurs.id_lecteur = emprunts.id_lecteur

            WHERE lecteurs.nom LIKE ?
               OR lecteurs.prenom LIKE ?

            GROUP BY lecteurs.id_lecteur

            ORDER BY lecteurs.nom
        """,(
        aujourd_hui ,
        "%"+terme +"%",
        "%"+terme +"%"
        ))

        return self .db .curseur .fetchall ()

    def afficher_lecteurs (self ):

        for ligne in self .tableau .get_children ():
            self .tableau .delete (ligne )

        for lecteur in self .recuperer_lecteurs ():

            valeurs =list (lecteur )

            valeurs [7 ]=valeurs [7 ]or 0 
            valeurs [8 ]=valeurs [8 ]or 0 

            self .tableau .insert (
            "",
            tk .END ,
            values =valeurs 
            )

    def ajouter_lecteur (self ):

        try :

            nom =self .champs ["nom"].get ().strip ()
            prenom =self .champs ["prenom"].get ().strip ()

            if not nom or not prenom :
                raise ValueError (
                "Le nom et le prénom sont obligatoires."
                )

            lecteur =Lecteur (
            nom ,
            prenom ,
            self .champs ["telephone"].get ().strip (),
            self .champs ["email"].get ().strip ()or None ,
            self .champs ["adresse"].get ().strip (),
            date .today ().isoformat ()
            )

            self .gestion .ajouter_lecteur (lecteur )

            messagebox .showinfo (
            "Succès",
            "Lecteur enregistré avec succès."
            )

            self .vider_champs ()
            self .afficher_lecteurs ()

        except Exception as erreur :

            messagebox .showerror ("Erreur",str (erreur ))

    def rechercher_lecteur (self ):

        terme =self .recherche .get ().strip ()

        for ligne in self .tableau .get_children ():
            self .tableau .delete (ligne )

        for lecteur in self .recuperer_lecteurs (terme ):

            valeurs =list (lecteur )

            valeurs [7 ]=valeurs [7 ]or 0 
            valeurs [8 ]=valeurs [8 ]or 0 

            self .tableau .insert (
            "",
            tk .END ,
            values =valeurs 
            )

    def selectionner_lecteur (self ,evenement ):

        selection =self .tableau .selection ()

        if not selection :
            return 

        valeurs =self .tableau .item (selection [0 ])["values"]

        self .id_selectionne =valeurs [0 ]

        cles =[
        "nom","prenom","telephone",
        "email","adresse"
        ]

        for cle ,valeur in zip (cles ,valeurs [1 :6 ]):

            self .champs [cle ].delete (0 ,tk .END )
            self .champs [cle ].insert (0 ,valeur or "")

    def modifier_lecteur (self ):

        if self .id_selectionne is None :
            messagebox .showwarning (
            "Attention",
            "Sélectionnez un lecteur dans le tableau."
            )
            return 

        try :

            nom =self .champs ["nom"].get ().strip ()
            prenom =self .champs ["prenom"].get ().strip ()

            if not nom or not prenom :
                raise ValueError (
                "Le nom et le prénom sont obligatoires."
                )

            lecteur =Lecteur (
            nom ,
            prenom ,
            self .champs ["telephone"].get ().strip (),
            self .champs ["email"].get ().strip ()or None ,
            self .champs ["adresse"].get ().strip (),
            date .today ().isoformat ()
            )

            self .gestion .modifier_lecteur (
            lecteur ,
            self .id_selectionne 
            )

            messagebox .showinfo (
            "Succès",
            "Lecteur modifié avec succès."
            )

            self .vider_champs ()
            self .afficher_lecteurs ()

        except Exception as erreur :

            messagebox .showerror ("Erreur",str (erreur ))

    def supprimer_lecteur (self ):

        selection =self .tableau .selection ()

        if not selection :
            messagebox .showwarning (
            "Attention",
            "Sélectionnez un lecteur."
            )
            return 

        confirmation =messagebox .askyesno (
        "Confirmation",
        "Voulez-vous supprimer ce lecteur ?"
        )

        if confirmation :

            valeurs =self .tableau .item (selection [0 ])["values"]

            try :

                self .gestion .supprimer_lecteur (valeurs [0 ])

                self .vider_champs ()
                self .afficher_lecteurs ()

                messagebox .showinfo (
                "Succès",
                "Lecteur supprimé."
                )

            except Exception as erreur :

                messagebox .showerror (
                "Suppression impossible",
                "Ce lecteur possède peut-être un historique d'emprunts.\n"
                +str (erreur )
                )

    def vider_champs (self ):

        for champ in self .champs .values ():
            champ .delete (0 ,tk .END )

        self .id_selectionne =None 

    def fermer (self ):

        self .gestion .fermer ()
        self .db .fermer ()
