import tkinter as tk 
from tkinter import ttk ,messagebox 

from database .connexion import Connexion 


class PageCategories :

    def __init__ (self ,parent ):

        self .parent =parent 
        self .db =Connexion ()
        self .id_selectionne =None 

        self .creer_interface ()
        self .afficher_categories ()

    def creer_interface (self ):

        for element in self .parent .winfo_children ():
            element .destroy ()

        titre =tk .Label (
        self .parent ,
        text ="Gestion des catégories",
        bg ="#F4F6F9",
        fg ="#243447",
        font =("Arial",23 ,"bold")
        )
        titre .pack (anchor ="w",padx =30 ,pady =20 )

        formulaire =tk .LabelFrame (
        self .parent ,
        text ="Informations de la catégorie",
        bg ="white",
        padx =15 ,
        pady =15 ,
        font =("Arial",11 ,"bold")
        )
        formulaire .pack (fill ="x",padx =30 ,pady =10 )

        tk .Label (
        formulaire ,
        text ="Nom de la catégorie :",
        bg ="white"
        ).grid (row =0 ,column =0 ,padx =8 ,pady =10 )

        self .champ_nom =tk .Entry (
        formulaire ,
        width =35 
        )
        self .champ_nom .grid (row =0 ,column =1 ,padx =8 ,pady =10 )

        boutons =tk .Frame (formulaire ,bg ="white")
        boutons .grid (row =1 ,column =0 ,columnspan =2 ,pady =10 )

        tk .Button (
        boutons ,
        text ="Ajouter",
        bg ="#243447",
        fg ="white",
        command =self .ajouter_categorie 
        ).pack (side ="left",padx =5 )

        tk .Button (
        boutons ,
        text ="Modifier",
        bg ="#287A55",
        fg ="white",
        command =self .modifier_categorie 
        ).pack (side ="left",padx =5 )

        tk .Button (
        boutons ,
        text ="Vider",
        command =self .vider_champ 
        ).pack (side ="left",padx =5 )

        recherche =tk .Frame (
        self .parent ,
        bg ="#F4F6F9"
        )
        recherche .pack (fill ="x",padx =30 ,pady =10 )

        tk .Label (
        recherche ,
        text ="Rechercher une catégorie :",
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
        command =self .rechercher_categorie 
        ).pack (side ="left")

        tk .Button (
        recherche ,
        text ="Afficher tout",
        command =self .afficher_categories 
        ).pack (side ="left",padx =8 )

        colonnes =("id","nom")

        self .tableau =ttk .Treeview (
        self .parent ,
        columns =colonnes ,
        show ="headings"
        )

        self .tableau .heading ("id",text ="ID")
        self .tableau .heading ("nom",text ="Nom de la catégorie")

        self .tableau .column ("id",width =100 )
        self .tableau .column ("nom",width =300 )

        self .tableau .pack (
        fill ="both",
        expand =True ,
        padx =30 ,
        pady =10 
        )

        self .tableau .bind (
        "<<TreeviewSelect>>",
        self .selectionner_categorie 
        )

        tk .Button (
        self .parent ,
        text ="Supprimer la catégorie sélectionnée",
        bg ="#B83232",
        fg ="white",
        command =self .supprimer_categorie 
        ).pack (anchor ="e",padx =30 ,pady =10 )

    def ajouter_categorie (self ):

        nom =self .champ_nom .get ().strip ()

        if not nom :
            messagebox .showwarning (
            "Attention",
            "Saisissez le nom de la catégorie."
            )
            return 

        try :

            self .db .curseur .execute ("""
                INSERT INTO categories (nom)
                VALUES (?)
            """,(nom ,))

            self .db .connexion .commit ()

            messagebox .showinfo (
            "Succès",
            "Catégorie ajoutée avec succès."
            )

            self .vider_champ ()
            self .afficher_categories ()

        except Exception as erreur :

            self .db .connexion .rollback ()

            messagebox .showerror (
            "Erreur",
            "Impossible d'ajouter cette catégorie.\n"+str (erreur )
            )

    def afficher_categories (self ):

        for ligne in self .tableau .get_children ():
            self .tableau .delete (ligne )

        self .db .curseur .execute ("""
            SELECT id_categorie, nom
            FROM categories
            ORDER BY nom
        """)

        for categorie in self .db .curseur .fetchall ():

            self .tableau .insert (
            "",
            tk .END ,
            values =categorie 
            )

    def rechercher_categorie (self ):

        terme =self .champ_recherche .get ().strip ()

        for ligne in self .tableau .get_children ():
            self .tableau .delete (ligne )

        self .db .curseur .execute ("""
            SELECT id_categorie, nom
            FROM categories
            WHERE nom LIKE ?
            ORDER BY nom
        """,("%"+terme +"%",))

        for categorie in self .db .curseur .fetchall ():

            self .tableau .insert (
            "",
            tk .END ,
            values =categorie 
            )

    def selectionner_categorie (self ,evenement ):

        selection =self .tableau .selection ()

        if not selection :
            return 

        valeurs =self .tableau .item (
        selection [0 ]
        )["values"]

        self .id_selectionne =valeurs [0 ]

        self .champ_nom .delete (0 ,tk .END )
        self .champ_nom .insert (0 ,valeurs [1 ])

    def modifier_categorie (self ):

        if self .id_selectionne is None :
            messagebox .showwarning (
            "Attention",
            "Sélectionnez une catégorie dans le tableau."
            )
            return 

        nom =self .champ_nom .get ().strip ()

        if not nom :
            messagebox .showwarning (
            "Attention",
            "Le nom de la catégorie est obligatoire."
            )
            return 

        try :

            self .db .curseur .execute ("""
                UPDATE categories
                SET nom = ?
                WHERE id_categorie = ?
            """,(nom ,self .id_selectionne ))

            self .db .connexion .commit ()

            messagebox .showinfo (
            "Succès",
            "Catégorie modifiée avec succès."
            )

            self .vider_champ ()
            self .afficher_categories ()

        except Exception as erreur :

            self .db .connexion .rollback ()

            messagebox .showerror (
            "Erreur",
            "Impossible de modifier cette catégorie.\n"+str (erreur )
            )

    def supprimer_categorie (self ):

        selection =self .tableau .selection ()

        if not selection :
            messagebox .showwarning (
            "Attention",
            "Sélectionnez une catégorie."
            )
            return 

        valeurs =self .tableau .item (
        selection [0 ]
        )["values"]

        confirmation =messagebox .askyesno (
        "Confirmation",
        "Voulez-vous vraiment supprimer cette catégorie ?"
        )

        if not confirmation :
            return 

        try :

            self .db .curseur .execute ("""
                DELETE FROM categories
                WHERE id_categorie = ?
            """,(valeurs [0 ],))

            self .db .connexion .commit ()

            messagebox .showinfo (
            "Succès",
            "Catégorie supprimée."
            )

            self .vider_champ ()
            self .afficher_categories ()

        except Exception as erreur :

            self .db .connexion .rollback ()

            messagebox .showerror (
            "Suppression impossible",
            "Cette catégorie est peut-être utilisée par un livre.\n"
            +str (erreur )
            )

    def vider_champ (self ):

        self .champ_nom .delete (0 ,tk .END )
        self .id_selectionne =None 

    def fermer (self ):

        self .db .fermer ()
