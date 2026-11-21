import tkinter as tk 
from tkinter import ttk ,messagebox 

from database .connexion import Connexion 


class PageAuteurs :

    def __init__ (self ,parent ):

        self .parent =parent 
        self .db =Connexion ()
        self .id_selectionne =None 

        self .creer_interface ()
        self .afficher_auteurs ()

    def creer_interface (self ):

        for element in self .parent .winfo_children ():
            element .destroy ()

        titre =tk .Label (
        self .parent ,
        text ="Gestion des auteurs",
        bg ="#F4F6F9",
        fg ="#243447",
        font =("Arial",23 ,"bold")
        )
        titre .pack (anchor ="w",padx =30 ,pady =20 )

        formulaire =tk .LabelFrame (
        self .parent ,
        text ="Informations de l'auteur",
        bg ="white",
        padx =15 ,
        pady =15 ,
        font =("Arial",11 ,"bold")
        )
        formulaire .pack (fill ="x",padx =30 ,pady =10 )

        tk .Label (
        formulaire ,
        text ="Nom :",
        bg ="white"
        ).grid (row =0 ,column =0 ,padx =8 ,pady =8 ,sticky ="w")

        self .champ_nom =tk .Entry (
        formulaire ,
        width =30 
        )
        self .champ_nom .grid (row =0 ,column =1 ,padx =8 ,pady =8 )

        tk .Label (
        formulaire ,
        text ="Prénom :",
        bg ="white"
        ).grid (row =1 ,column =0 ,padx =8 ,pady =8 ,sticky ="w")

        self .champ_prenom =tk .Entry (
        formulaire ,
        width =30 
        )
        self .champ_prenom .grid (row =1 ,column =1 ,padx =8 ,pady =8 )

        boutons =tk .Frame (
        formulaire ,
        bg ="white"
        )
        boutons .grid (row =2 ,column =0 ,columnspan =2 ,pady =10 )

        tk .Button (
        boutons ,
        text ="Ajouter",
        bg ="#243447",
        fg ="white",
        command =self .ajouter_auteur 
        ).pack (side ="left",padx =5 )

        tk .Button (
        boutons ,
        text ="Modifier",
        bg ="#287A55",
        fg ="white",
        command =self .modifier_auteur 
        ).pack (side ="left",padx =5 )

        tk .Button (
        boutons ,
        text ="Vider",
        command =self .vider_champs 
        ).pack (side ="left",padx =5 )

        recherche =tk .Frame (
        self .parent ,
        bg ="#F4F6F9"
        )
        recherche .pack (fill ="x",padx =30 ,pady =10 )

        tk .Label (
        recherche ,
        text ="Rechercher un auteur :",
        bg ="#F4F6F9"
        ).pack (side ="left")

        self .champ_recherche =tk .Entry (
        recherche ,
        width =30 
        )
        self .champ_recherche .pack (side ="left",padx =10 )

        tk .Button (
        recherche ,
        text ="Rechercher",
        command =self .rechercher_auteur 
        ).pack (side ="left")

        tk .Button (
        recherche ,
        text ="Afficher tout",
        command =self .afficher_auteurs 
        ).pack (side ="left",padx =8 )

        colonnes =("id","nom","prenom")

        self .tableau =ttk .Treeview (
        self .parent ,
        columns =colonnes ,
        show ="headings"
        )

        self .tableau .heading ("id",text ="ID")
        self .tableau .heading ("nom",text ="Nom")
        self .tableau .heading ("prenom",text ="Prénom")

        self .tableau .column ("id",width =80 )
        self .tableau .column ("nom",width =200 )
        self .tableau .column ("prenom",width =200 )

        self .tableau .pack (
        fill ="both",
        expand =True ,
        padx =30 ,
        pady =10 
        )

        self .tableau .bind (
        "<<TreeviewSelect>>",
        self .selectionner_auteur 
        )

        tk .Button (
        self .parent ,
        text ="Supprimer l'auteur sélectionné",
        bg ="#B83232",
        fg ="white",
        command =self .supprimer_auteur 
        ).pack (anchor ="e",padx =30 ,pady =10 )

    def ajouter_auteur (self ):

        nom =self .champ_nom .get ().strip ()
        prenom =self .champ_prenom .get ().strip ()

        if not nom :
            messagebox .showwarning (
            "Attention",
            "Le nom de l'auteur est obligatoire."
            )
            return 

        try :

            self .db .curseur .execute ("""
                INSERT INTO auteurs (nom, prenom)
                VALUES (?, ?)
            """,(
            nom ,
            prenom or None 
            ))

            self .db .connexion .commit ()

            messagebox .showinfo (
            "Succès",
            "Auteur ajouté avec succès."
            )

            self .vider_champs ()
            self .afficher_auteurs ()

        except Exception as erreur :

            self .db .connexion .rollback ()

            messagebox .showerror (
            "Erreur",
            str (erreur )
            )

    def afficher_auteurs (self ):

        for ligne in self .tableau .get_children ():
            self .tableau .delete (ligne )

        self .db .curseur .execute ("""
            SELECT id_auteur, nom, prenom
            FROM auteurs
            ORDER BY nom
        """)

        for auteur in self .db .curseur .fetchall ():

            self .tableau .insert (
            "",
            tk .END ,
            values =auteur 
            )

    def rechercher_auteur (self ):

        terme =self .champ_recherche .get ().strip ()

        for ligne in self .tableau .get_children ():
            self .tableau .delete (ligne )

        self .db .curseur .execute ("""
            SELECT id_auteur, nom, prenom
            FROM auteurs
            WHERE nom LIKE ?
               OR prenom LIKE ?
            ORDER BY nom
        """,(
        "%"+terme +"%",
        "%"+terme +"%"
        ))

        for auteur in self .db .curseur .fetchall ():

            self .tableau .insert (
            "",
            tk .END ,
            values =auteur 
            )

    def selectionner_auteur (self ,evenement ):

        selection =self .tableau .selection ()

        if not selection :
            return 

        valeurs =self .tableau .item (
        selection [0 ]
        )["values"]

        self .id_selectionne =valeurs [0 ]

        self .champ_nom .delete (0 ,tk .END )
        self .champ_nom .insert (0 ,valeurs [1 ]or "")

        self .champ_prenom .delete (0 ,tk .END )
        self .champ_prenom .insert (0 ,valeurs [2 ]or "")

    def modifier_auteur (self ):

        if self .id_selectionne is None :
            messagebox .showwarning (
            "Attention",
            "Sélectionnez un auteur dans le tableau."
            )
            return 

        nom =self .champ_nom .get ().strip ()
        prenom =self .champ_prenom .get ().strip ()

        if not nom :
            messagebox .showwarning (
            "Attention",
            "Le nom de l'auteur est obligatoire."
            )
            return 

        try :

            self .db .curseur .execute ("""
                UPDATE auteurs
                SET nom = ?, prenom = ?
                WHERE id_auteur = ?
            """,(
            nom ,
            prenom or None ,
            self .id_selectionne 
            ))

            self .db .connexion .commit ()

            messagebox .showinfo (
            "Succès",
            "Auteur modifié avec succès."
            )

            self .vider_champs ()
            self .afficher_auteurs ()

        except Exception as erreur :

            self .db .connexion .rollback ()

            messagebox .showerror (
            "Erreur",
            str (erreur )
            )

    def supprimer_auteur (self ):

        selection =self .tableau .selection ()

        if not selection :
            messagebox .showwarning (
            "Attention",
            "Sélectionnez un auteur."
            )
            return 

        valeurs =self .tableau .item (
        selection [0 ]
        )["values"]

        confirmation =messagebox .askyesno (
        "Confirmation",
        "Voulez-vous vraiment supprimer cet auteur ?"
        )

        if not confirmation :
            return 

        try :

            self .db .curseur .execute ("""
                DELETE FROM auteurs
                WHERE id_auteur = ?
            """,(valeurs [0 ],))

            self .db .connexion .commit ()

            messagebox .showinfo (
            "Succès",
            "Auteur supprimé."
            )

            self .vider_champs ()
            self .afficher_auteurs ()

        except Exception as erreur :

            self .db .connexion .rollback ()

            messagebox .showerror (
            "Suppression impossible",
            "Cet auteur est peut-être associé à un livre.\n"
            +str (erreur )
            )

    def vider_champs (self ):

        self .champ_nom .delete (0 ,tk .END )
        self .champ_prenom .delete (0 ,tk .END )

        self .id_selectionne =None 

    def fermer (self ):

        self .db .fermer ()
