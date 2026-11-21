import tkinter as tk 
from tkinter import ttk ,messagebox ,simpledialog 

from datetime import date 

from models .livre import Livre 
from services .gestion_livres import GestionLivres 
from database .connexion import Connexion 


class PageLivres :

    def __init__ (self ,parent ):

        self .parent =parent 
        self .gestion =GestionLivres ()
        self .db =Connexion ()
        self .id_selectionne =None 

        self .creer_interface ()
        self .charger_listes ()
        self .afficher_livres ()

    def creer_interface (self ):

        for element in self .parent .winfo_children ():
            element .destroy ()

        titre =tk .Label (
        self .parent ,
        text ="Catalogue des livres",
        bg ="#F4F6F9",
        fg ="#243447",
        font =("Arial",23 ,"bold")
        )

        titre .pack (anchor ="w",padx =30 ,pady =15 )

        formulaire =tk .LabelFrame (
        self .parent ,
        text ="Informations du livre",
        bg ="white",
        padx =15 ,
        pady =10 ,
        font =("Arial",11 ,"bold")
        )

        formulaire .pack (fill ="x",padx =30 ,pady =5 )

        self .champs ={}

        informations =[
        ("Titre","titre"),
        ("ISBN","isbn"),
        ("Année de publication","annee"),
        ("Éditeur","editeur"),
        ("Quantité totale","quantite")
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

            champ =tk .Entry (
            formulaire ,
            width =25 
            )

            champ .grid (
            row =ligne ,
            column =colonne +1 ,
            padx =8 ,
            pady =5 
            )

            self .champs [cle ]=champ 

        tk .Label (
        formulaire ,
        text ="Auteur",
        bg ="white"
        ).grid (
        row =3 ,
        column =0 ,
        padx =8 ,
        pady =5 ,
        sticky ="w"
        )

        self .auteur =ttk .Combobox (
        formulaire ,
        width =23 ,
        state ="readonly"
        )

        self .auteur .grid (
        row =3 ,
        column =1 ,
        padx =8 ,
        pady =5 
        )

        tk .Button (
        formulaire ,
        text ="+ Auteur",
        command =self .ajouter_auteur 
        ).grid (
        row =3 ,
        column =2 ,
        padx =5 
        )

        tk .Label (
        formulaire ,
        text ="Catégorie",
        bg ="white"
        ).grid (
        row =4 ,
        column =0 ,
        padx =8 ,
        pady =5 ,
        sticky ="w"
        )

        self .categorie =ttk .Combobox (
        formulaire ,
        width =23 ,
        state ="readonly"
        )

        self .categorie .grid (
        row =4 ,
        column =1 ,
        padx =8 ,
        pady =5 
        )

        tk .Label (
        formulaire ,
        text ="Rayon",
        bg ="white"
        ).grid (
        row =4 ,
        column =2 ,
        padx =8 ,
        pady =5 ,
        sticky ="w"
        )

        self .rayon =ttk .Combobox (
        formulaire ,
        width =23 ,
        state ="readonly"
        )

        self .rayon .grid (
        row =4 ,
        column =3 ,
        padx =8 ,
        pady =5 
        )

        boutons =tk .Frame (
        formulaire ,
        bg ="white"
        )

        boutons .grid (
        row =5 ,
        column =0 ,
        columnspan =4 ,
        pady =10 
        )

        tk .Button (
        boutons ,
        text ="Ajouter",
        bg ="#243447",
        fg ="white",
        command =self .ajouter_livre 
        ).pack (side ="left",padx =5 )

        tk .Button (
        boutons ,
        text ="Modifier",
        bg ="#287A55",
        fg ="white",
        command =self .modifier_livre 
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

        recherche .pack (
        fill ="x",
        padx =30 ,
        pady =8 
        )

        tk .Label (
        recherche ,
        text ="Rechercher un livre :",
        bg ="#F4F6F9"
        ).pack (side ="left")

        self .recherche =tk .Entry (
        recherche ,
        width =30 
        )

        self .recherche .pack (
        side ="left",
        padx =10 
        )

        tk .Button (
        recherche ,
        text ="Rechercher",
        command =self .rechercher_livre 
        ).pack (side ="left")

        tk .Button (
        recherche ,
        text ="Afficher tout",
        command =self .afficher_livres 
        ).pack (
        side ="left",
        padx =8 
        )

        colonnes =(
        "id",
        "titre",
        "isbn",
        "annee",
        "editeur",
        "auteur",
        "categorie",
        "rayon",
        "total",
        "disponible"
        )

        self .tableau =ttk .Treeview (
        self .parent ,
        columns =colonnes ,
        show ="headings"
        )

        entetes ={
        "id":"ID",
        "titre":"Titre",
        "isbn":"ISBN",
        "annee":"Année",
        "editeur":"Éditeur",
        "auteur":"Auteur",
        "categorie":"Catégorie",
        "rayon":"Rayon",
        "total":"Total",
        "disponible":"Disponible"
        }

        for colonne ,nom in entetes .items ():

            self .tableau .heading (
            colonne ,
            text =nom 
            )

            self .tableau .column (
            colonne ,
            width =100 
            )

        self .tableau .pack (
        fill ="both",
        expand =True ,
        padx =30 ,
        pady =8 
        )

        self .tableau .bind (
        "<<TreeviewSelect>>",
        self .selectionner_livre 
        )

        tk .Button (
        self .parent ,
        text ="Supprimer le livre sélectionné",
        bg ="#B83232",
        fg ="white",
        command =self .supprimer_livre 
        ).pack (
        anchor ="e",
        padx =30 ,
        pady =8 
        )

    def charger_listes (self ):

        self .db .curseur .execute ("""
            SELECT id_auteur, nom, prenom
            FROM auteurs
            ORDER BY nom
        """)

        self .auteurs ={}
        valeurs =[]

        for identifiant ,nom ,prenom in self .db .curseur .fetchall ():

            affichage =(
            f"{identifiant } - {nom } {prenom or ''}"
            ).strip ()

            valeurs .append (affichage )
            self .auteurs [affichage ]=identifiant 

        self .auteur ["values"]=valeurs 

        self .db .curseur .execute ("""
            SELECT id_categorie, nom
            FROM categories
            ORDER BY nom
        """)

        self .categories ={}
        valeurs =[]

        for identifiant ,nom in self .db .curseur .fetchall ():

            valeurs .append (nom )
            self .categories [nom ]=identifiant 

        self .categorie ["values"]=valeurs 

        self .db .curseur .execute ("""
            SELECT id_rayon, nom
            FROM rayons
            ORDER BY nom
        """)

        self .rayons ={}
        valeurs =[]

        for identifiant ,nom in self .db .curseur .fetchall ():

            valeurs .append (nom )
            self .rayons [nom ]=identifiant 

        self .rayon ["values"]=valeurs 

    def ajouter_auteur (self ):

        nom =simpledialog .askstring (
        "Nouvel auteur",
        "Nom de l'auteur :",
        parent =self .parent 
        )

        if not nom or not nom .strip ():
            return 

        prenom =simpledialog .askstring (
        "Nouvel auteur",
        "Prénom de l'auteur :",
        parent =self .parent 
        )

        try :

            self .db .curseur .execute ("""
                INSERT INTO auteurs (nom, prenom)
                VALUES (?, ?)
            """,(
            nom .strip (),
            prenom .strip ()if prenom and prenom .strip ()else None 
            ))

            id_auteur =self .db .curseur .lastrowid 

            self .db .connexion .commit ()

            self .charger_listes ()

            for affichage ,identifiant in self .auteurs .items ():

                if identifiant ==id_auteur :
                    self .auteur .set (affichage )
                    break 

            messagebox .showinfo (
            "Succès",
            "Auteur ajouté avec succès."
            )

        except Exception as erreur :

            self .db .connexion .rollback ()

            messagebox .showerror (
            "Erreur",
            str (erreur )
            )

    def recuperer_donnees (self ):

        titre =self .champs ["titre"].get ().strip ()
        isbn =self .champs ["isbn"].get ().strip ()or None 
        annee =self .champs ["annee"].get ().strip ()
        editeur =self .champs ["editeur"].get ().strip ()
        quantite =self .champs ["quantite"].get ().strip ()

        if not titre :
            raise ValueError (
            "Le titre du livre est obligatoire."
            )

        if not quantite :
            raise ValueError (
            "Saisissez la quantité totale."
            )

        try :
            quantite =int (quantite )
        except ValueError :
            raise ValueError (
            "La quantité doit être un nombre entier."
            )

        if quantite <1 :
            raise ValueError (
            "La quantité doit être au moins égale à 1."
            )

        if annee :

            try :
                annee =int (annee )
            except ValueError :
                raise ValueError (
                "L'année doit être un nombre entier."
                )

            if annee <1 or annee >date .today ().year :
                raise ValueError (
                "Saisissez une année de publication valide."
                )

        else :
            annee =None 

        auteur_selectionne =self .auteur .get ()
        categorie_selectionnee =self .categorie .get ()
        rayon_selectionne =self .rayon .get ()

        if not auteur_selectionne :
            raise ValueError (
            "Sélectionnez un auteur."
            )

        if not categorie_selectionnee :
            raise ValueError (
            "Sélectionnez une catégorie."
            )

        if not rayon_selectionne :
            raise ValueError (
            "Sélectionnez un rayon."
            )

        return Livre (
        titre ,
        isbn ,
        annee ,
        editeur ,
        self .auteurs [auteur_selectionne ],
        self .categories [categorie_selectionnee ],
        self .rayons [rayon_selectionne ],
        quantite ,
        quantite 
        )

    def ajouter_livre (self ):

        try :

            livre =self .recuperer_donnees ()

            self .gestion .ajouter_livre (livre )

            messagebox .showinfo (
            "Succès",
            "Livre ajouté avec succès."
            )

            self .vider_champs ()
            self .afficher_livres ()

        except Exception as erreur :

            messagebox .showerror (
            "Erreur",
            str (erreur )
            )

    def recuperer_livres (self ,terme =""):

        self .db .curseur .execute ("""
            SELECT
                livres.id_livre,
                livres.titre,
                livres.isbn,
                livres.annee_publication,
                livres.editeur,
                auteurs.nom || ' ' || COALESCE(auteurs.prenom, ''),
                categories.nom,
                rayons.nom,
                livres.quantite_totale,
                livres.quantite_disponible

            FROM livres

            LEFT JOIN auteurs
                ON livres.id_auteur = auteurs.id_auteur

            LEFT JOIN categories
                ON livres.id_categorie = categories.id_categorie

            LEFT JOIN rayons
                ON livres.id_rayon = rayons.id_rayon

            WHERE livres.titre LIKE ?
               OR livres.isbn LIKE ?
               OR auteurs.nom LIKE ?
               OR auteurs.prenom LIKE ?

            ORDER BY livres.titre
        """,(
        "%"+terme +"%",
        "%"+terme +"%",
        "%"+terme +"%",
        "%"+terme +"%"
        ))

        return self .db .curseur .fetchall ()

    def afficher_livres (self ):

        for ligne in self .tableau .get_children ():
            self .tableau .delete (ligne )

        for livre in self .recuperer_livres ():

            self .tableau .insert (
            "",
            tk .END ,
            values =livre 
            )

    def rechercher_livre (self ):

        terme =self .recherche .get ().strip ()

        for ligne in self .tableau .get_children ():
            self .tableau .delete (ligne )

        for livre in self .recuperer_livres (terme ):

            self .tableau .insert (
            "",
            tk .END ,
            values =livre 
            )

    def selectionner_livre (self ,evenement ):

        selection =self .tableau .selection ()

        if not selection :
            return 

        valeurs =self .tableau .item (
        selection [0 ]
        )["values"]

        self .id_selectionne =valeurs [0 ]

        cles =[
        "titre",
        "isbn",
        "annee",
        "editeur",
        "quantite"
        ]

        valeurs_champs =[
        valeurs [1 ],
        valeurs [2 ],
        valeurs [3 ],
        valeurs [4 ],
        valeurs [8 ]
        ]

        for cle ,valeur in zip (cles ,valeurs_champs ):

            self .champs [cle ].delete (0 ,tk .END )
            self .champs [cle ].insert (0 ,valeur or "")

        self .db .curseur .execute ("""
            SELECT id_auteur, id_categorie, id_rayon
            FROM livres
            WHERE id_livre = ?
        """,(self .id_selectionne ,))

        ids =self .db .curseur .fetchone ()

        if ids :

            for affichage ,identifiant in self .auteurs .items ():

                if identifiant ==ids [0 ]:
                    self .auteur .set (affichage )
                    break 

            for affichage ,identifiant in self .categories .items ():

                if identifiant ==ids [1 ]:
                    self .categorie .set (affichage )
                    break 

            for affichage ,identifiant in self .rayons .items ():

                if identifiant ==ids [2 ]:
                    self .rayon .set (affichage )
                    break 

    def modifier_livre (self ):

        if self .id_selectionne is None :

            messagebox .showwarning (
            "Attention",
            "Sélectionnez un livre dans le tableau."
            )
            return 

        try :

            livre =self .recuperer_donnees ()

            self .gestion .modifier_livre (
            livre ,
            self .id_selectionne 
            )

            messagebox .showinfo (
            "Succès",
            "Livre modifié avec succès."
            )

            self .vider_champs ()
            self .afficher_livres ()

        except Exception as erreur :

            messagebox .showerror (
            "Erreur",
            str (erreur )
            )

    def supprimer_livre (self ):

        selection =self .tableau .selection ()

        if not selection :

            messagebox .showwarning (
            "Attention",
            "Sélectionnez un livre."
            )
            return 

        confirmation =messagebox .askyesno (
        "Confirmation",
        "Voulez-vous vraiment supprimer ce livre ?"
        )

        if not confirmation :
            return 

        valeurs =self .tableau .item (
        selection [0 ]
        )["values"]

        try :

            self .gestion .supprimer_livre (valeurs [0 ])

            self .vider_champs ()
            self .afficher_livres ()

            messagebox .showinfo (
            "Succès",
            "Livre supprimé."
            )

        except Exception as erreur :

            messagebox .showerror (
            "Suppression impossible",
            "Ce livre possède peut-être un historique d'emprunts.\n"
            +str (erreur )
            )

    def vider_champs (self ):

        for champ in self .champs .values ():
            champ .delete (0 ,tk .END )

        self .auteur .set ("")
        self .categorie .set ("")
        self .rayon .set ("")

        self .id_selectionne =None 

    def fermer (self ):

        self .gestion .fermer ()
        self .db .fermer ()
