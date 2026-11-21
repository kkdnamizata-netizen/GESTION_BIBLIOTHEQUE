import tkinter as tk 
from tkinter import ttk ,messagebox 

from database .connexion import Connexion 


class PageRayons :

    def __init__ (self ,parent ):

        self .parent =parent 
        self .db =Connexion ()
        self .id_selectionne =None 

        self .creer_interface ()
        self .afficher_rayons ()

    def creer_interface (self ):

        for element in self .parent .winfo_children ():
            element .destroy ()

        titre =tk .Label (
        self .parent ,
        text ="Gestion des rayons",
        bg ="#F4F6F9",
        fg ="#243447",
        font =("Arial",23 ,"bold")
        )
        titre .pack (anchor ="w",padx =30 ,pady =20 )

        formulaire =tk .LabelFrame (
        self .parent ,
        text ="Informations du rayon",
        bg ="white",
        padx =15 ,
        pady =15 ,
        font =("Arial",11 ,"bold")
        )
        formulaire .pack (fill ="x",padx =30 ,pady =10 )

        tk .Label (
        formulaire ,
        text ="Nom du rayon :",
        bg ="white"
        ).grid (row =0 ,column =0 ,padx =8 ,pady =8 ,sticky ="w")

        self .champ_nom =tk .Entry (
        formulaire ,
        width =35 
        )
        self .champ_nom .grid (row =0 ,column =1 ,padx =8 ,pady =8 )

        tk .Label (
        formulaire ,
        text ="Description :",
        bg ="white"
        ).grid (row =1 ,column =0 ,padx =8 ,pady =8 ,sticky ="w")

        self .champ_description =tk .Entry (
        formulaire ,
        width =35 
        )
        self .champ_description .grid (row =1 ,column =1 ,padx =8 ,pady =8 )

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
        command =self .ajouter_rayon 
        ).pack (side ="left",padx =5 )

        tk .Button (
        boutons ,
        text ="Modifier",
        bg ="#287A55",
        fg ="white",
        command =self .modifier_rayon 
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
        text ="Rechercher un rayon :",
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
        command =self .rechercher_rayon 
        ).pack (side ="left")

        tk .Button (
        recherche ,
        text ="Afficher tout",
        command =self .afficher_rayons 
        ).pack (side ="left",padx =8 )

        colonnes =(
        "id",
        "nom",
        "description"
        )

        self .tableau =ttk .Treeview (
        self .parent ,
        columns =colonnes ,
        show ="headings"
        )

        self .tableau .heading ("id",text ="ID")
        self .tableau .heading ("nom",text ="Nom du rayon")
        self .tableau .heading ("description",text ="Description")

        self .tableau .column ("id",width =80 )
        self .tableau .column ("nom",width =200 )
        self .tableau .column ("description",width =400 )

        self .tableau .pack (
        fill ="both",
        expand =True ,
        padx =30 ,
        pady =10 
        )

        self .tableau .bind (
        "<<TreeviewSelect>>",
        self .selectionner_rayon 
        )

        tk .Button (
        self .parent ,
        text ="Supprimer le rayon sélectionné",
        bg ="#B83232",
        fg ="white",
        command =self .supprimer_rayon 
        ).pack (anchor ="e",padx =30 ,pady =10 )

    def ajouter_rayon (self ):

        nom =self .champ_nom .get ().strip ()
        description =self .champ_description .get ().strip ()

        if not nom :
            messagebox .showwarning (
            "Attention",
            "Le nom du rayon est obligatoire."
            )
            return 

        try :

            self .db .curseur .execute ("""
                INSERT INTO rayons (nom, description)
                VALUES (?, ?)
            """,(nom ,description ))

            self .db .connexion .commit ()

            messagebox .showinfo (
            "Succès",
            "Rayon ajouté avec succès."
            )

            self .vider_champs ()
            self .afficher_rayons ()

        except Exception as erreur :

            self .db .connexion .rollback ()

            messagebox .showerror (
            "Erreur",
            "Impossible d'ajouter ce rayon.\n"+str (erreur )
            )

    def afficher_rayons (self ):

        for ligne in self .tableau .get_children ():
            self .tableau .delete (ligne )

        self .db .curseur .execute ("""
            SELECT id_rayon, nom, description
            FROM rayons
            ORDER BY nom
        """)

        for rayon in self .db .curseur .fetchall ():

            self .tableau .insert (
            "",
            tk .END ,
            values =rayon 
            )

    def rechercher_rayon (self ):

        terme =self .champ_recherche .get ().strip ()

        for ligne in self .tableau .get_children ():
            self .tableau .delete (ligne )

        self .db .curseur .execute ("""
            SELECT id_rayon, nom, description
            FROM rayons
            WHERE nom LIKE ?
               OR description LIKE ?
            ORDER BY nom
        """,(
        "%"+terme +"%",
        "%"+terme +"%"
        ))

        for rayon in self .db .curseur .fetchall ():

            self .tableau .insert (
            "",
            tk .END ,
            values =rayon 
            )

    def selectionner_rayon (self ,evenement ):

        selection =self .tableau .selection ()

        if not selection :
            return 

        valeurs =self .tableau .item (
        selection [0 ]
        )["values"]

        self .id_selectionne =valeurs [0 ]

        self .champ_nom .delete (0 ,tk .END )
        self .champ_nom .insert (0 ,valeurs [1 ]or "")

        self .champ_description .delete (0 ,tk .END )
        self .champ_description .insert (0 ,valeurs [2 ]or "")

    def modifier_rayon (self ):

        if self .id_selectionne is None :
            messagebox .showwarning (
            "Attention",
            "Sélectionnez un rayon dans le tableau."
            )
            return 

        nom =self .champ_nom .get ().strip ()
        description =self .champ_description .get ().strip ()

        if not nom :
            messagebox .showwarning (
            "Attention",
            "Le nom du rayon est obligatoire."
            )
            return 

        try :

            self .db .curseur .execute ("""
                UPDATE rayons
                SET nom = ?, description = ?
                WHERE id_rayon = ?
            """,(
            nom ,
            description ,
            self .id_selectionne 
            ))

            self .db .connexion .commit ()

            messagebox .showinfo (
            "Succès",
            "Rayon modifié avec succès."
            )

            self .vider_champs ()
            self .afficher_rayons ()

        except Exception as erreur :

            self .db .connexion .rollback ()

            messagebox .showerror (
            "Erreur",
            "Impossible de modifier ce rayon.\n"+str (erreur )
            )

    def supprimer_rayon (self ):

        selection =self .tableau .selection ()

        if not selection :
            messagebox .showwarning (
            "Attention",
            "Sélectionnez un rayon."
            )
            return 

        valeurs =self .tableau .item (
        selection [0 ]
        )["values"]

        confirmation =messagebox .askyesno (
        "Confirmation",
        "Voulez-vous vraiment supprimer ce rayon ?"
        )

        if not confirmation :
            return 

        try :

            self .db .curseur .execute ("""
                DELETE FROM rayons
                WHERE id_rayon = ?
            """,(valeurs [0 ],))

            self .db .connexion .commit ()

            messagebox .showinfo (
            "Succès",
            "Rayon supprimé."
            )

            self .vider_champs ()
            self .afficher_rayons ()

        except Exception as erreur :

            self .db .connexion .rollback ()

            messagebox .showerror (
            "Suppression impossible",
            "Ce rayon est peut-être utilisé par un livre.\n"
            +str (erreur )
            )

    def vider_champs (self ):

        self .champ_nom .delete (0 ,tk .END )
        self .champ_description .delete (0 ,tk .END )

        self .id_selectionne =None 

    def fermer (self ):

        self .db .fermer ()
