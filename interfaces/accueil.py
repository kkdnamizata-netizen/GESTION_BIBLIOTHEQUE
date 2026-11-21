import tkinter as tk 
from tkinter import ttk 
import os 
import datetime 

try :
    from PIL import Image ,ImageTk 
    PIL_AVAILABLE =True 
except ImportError :
    PIL_AVAILABLE =False 

from database .connexion import Connexion 

from interfaces .livres import PageLivres 
from interfaces .auteurs import PageAuteurs 
from interfaces .lecteurs import PageLecteurs 
from interfaces .emprunts import PageEmprunts 
from interfaces .retours import PageRetours 
from interfaces .categories import PageCategories 
from interfaces .rayons import PageRayons 


class Accueil :

    def __init__ (self ,fenetre ):
        self .fenetre =fenetre 
        self .fenetre .title ("Gestion de bibliothèque")
        self .fenetre .geometry ("1150x720")
        self .fenetre .minsize (950 ,600 )
        self .fenetre .configure (bg ="#F5F0EB")

        self .db =Connexion ()
        self .page_actuelle =None 

        self .configurer_styles ()
        self .creer_interface ()

        self .fenetre .protocol ("WM_DELETE_WINDOW",self .quitter_application )

    def configurer_styles (self ):
        style =ttk .Style ()
        style .theme_use ('clam')


        style .configure ('Menu.TFrame',background ='#800000')


        style .configure ('Menu.TButton',
        background ='#800000',
        foreground ='white',
        font =('Segoe UI',12 ),
        borderwidth =0 ,
        padding =(15 ,10 ))
        style .map ('Menu.TButton',
        background =[('active','#A52A2A')],
        foreground =[('active','white')])


        style .configure ('ActiveMenu.TButton',
        background ='#FFFFFF',
        foreground ='#800000',
        font =('Segoe UI',12 ,'bold'),
        borderwidth =0 ,
        padding =(15 ,10 ))
        style .map ('ActiveMenu.TButton',
        background =[('active','#F0F0F0')],
        foreground =[('active','#800000')])


        style .configure ('Treeview',
        background ='white',
        fieldbackground ='white',
        foreground ='#333333',
        font =('Segoe UI',10 ),
        rowheight =32 )
        style .configure ('Treeview.Heading',
        background ='#800000',
        foreground ='white',
        font =('Segoe UI',10 ,'bold'),
        padding =6 )
        style .map ('Treeview',
        background =[('selected','#E8D0D0')])
        style .map ('Treeview.Heading',
        background =[('active','#A52A2A')])

    def creer_interface (self ):

        self .menu =tk .Frame (self .fenetre ,bg ="#800000",width =220 )
        self .menu .pack (side ="left",fill ="y")
        self .menu .pack_propagate (False )


        logo_frame =tk .Frame (self .menu ,bg ="#800000")
        logo_frame .pack (fill ="x",pady =(25 ,5 ))

        tk .Label (logo_frame ,text ="📖",bg ="#800000",font =("Segoe UI",28 )).pack ()
        tk .Label (logo_frame ,text ="MA BIBLIOTHÈQUE",bg ="#800000",fg ="white",
        font =("Segoe UI",13 ,"bold")).pack (pady =(5 ,20 ))


        self .boutons_menu =[]
        boutons_config =[
        ("🏠","Accueil"),
        ("📚","Livres"),
        ("✍️","Auteurs"),
        ("👤","Lecteurs"),
        ("🔖","Emprunts"),
        ("✅","Retours"),
        ("📂","Catégories"),
        ("🗄️","Rayons"),
        ]

        for emoji ,nom in boutons_config :
            btn =tk .Button (
            self .menu ,
            text =f"  {emoji }  {nom }",
            bg ="#800000",
            fg ="white",
            activebackground ="#A52A2A",
            activeforeground ="white",
            font =("Segoe UI",12 ),
            bd =0 ,
            anchor ="w",
            padx =20 ,
            pady =8 ,
            cursor ="hand2",
            command =lambda p =nom :self .ouvrir_page (p )
            )
            btn .pack (fill ="x",padx =10 ,pady =2 )
            self .boutons_menu .append ((nom ,btn ))


        self .surligner_bouton ("Accueil")


        self .contenu =tk .Frame (self .fenetre ,bg ="#F5F0EB")
        self .contenu .pack (side ="right",fill ="both",expand =True )

        self .afficher_accueil ()

    def surligner_bouton (self ,page_active ):
        for nom ,btn in self .boutons_menu :
            if nom ==page_active :
                btn .configure (bg ="white",fg ="#800000",font =("Segoe UI",12 ,"bold"))
            else :
                btn .configure (bg ="#800000",fg ="white",font =("Segoe UI",12 ))

    def nettoyer_contenu (self ):
        if self .page_actuelle is not None :
            if hasattr (self .page_actuelle ,"fermer"):
                self .page_actuelle .fermer ()
            self .page_actuelle =None 

        for element in self .contenu .winfo_children ():
            element .destroy ()

    def afficher_accueil (self ):
        self .nettoyer_contenu ()


        canvas =tk .Canvas (self .contenu ,bg ="#F5F0EB",highlightthickness =0 )
        scrollbar =ttk .Scrollbar (self .contenu ,orient ="vertical",command =canvas .yview )
        scroll_frame =tk .Frame (canvas ,bg ="#F5F0EB")

        scroll_frame .bind ("<Configure>",lambda e :canvas .configure (scrollregion =canvas .bbox ("all")))
        canvas .create_window ((0 ,0 ),window =scroll_frame ,anchor ="nw")
        canvas .configure (yscrollcommand =scrollbar .set )

        canvas .pack (side ="left",fill ="both",expand =True )
        scrollbar .pack (side ="right",fill ="y")


        def on_mousewheel (event ):
            canvas .yview_scroll (int (-1 *(event .delta /120 )),"units")
        canvas .bind_all ("<MouseWheel>",on_mousewheel )


        header_frame =tk .Frame (scroll_frame ,bg ="#F5F0EB")
        header_frame .pack (fill ="x",padx =30 ,pady =(25 ,5 ))

        tk .Label (header_frame ,text ="📖",bg ="#F5F0EB",
        font =("Segoe UI",28 )).pack (side ="left",padx =(0 ,10 ))

        header_text =tk .Frame (header_frame ,bg ="#F5F0EB")
        header_text .pack (side ="left")
        tk .Label (header_text ,text ="Tableau de bord",bg ="#F5F0EB",fg ="#800000",
        font =("Segoe UI",24 ,"bold")).pack (anchor ="w")
        tk .Label (header_text ,text ="Bienvenue dans votre système de gestion de bibliothèque.",
        bg ="#F5F0EB",fg ="#888888",font =("Segoe UI",11 )).pack (anchor ="w")


        self .db .curseur .execute ("""
            SELECT COUNT(*),
                   COALESCE(SUM(quantite_totale), 0),
                   COALESCE(SUM(quantite_disponible), 0)
            FROM livres
        """)
        nombre_livres ,total_exemplaires ,disponibles =self .db .curseur .fetchone ()

        self .db .curseur .execute ("SELECT COUNT(*) FROM auteurs")
        nombre_auteurs =self .db .curseur .fetchone ()[0 ]

        self .db .curseur .execute ("SELECT COUNT(*) FROM lecteurs")
        nombre_lecteurs =self .db .curseur .fetchone ()[0 ]

        self .db .curseur .execute ("SELECT COUNT(*) FROM emprunts WHERE statut = 'En cours'")
        emprunts_en_cours =self .db .curseur .fetchone ()[0 ]

        aujourd_hui =datetime .date .today ().isoformat ()
        self .db .curseur .execute ("""
            SELECT COUNT(*) FROM emprunts
            WHERE statut = 'En cours' AND date_retour_prevue < ?
        """,(aujourd_hui ,))
        emprunts_en_retard =self .db .curseur .fetchone ()[0 ]


        cartes_data =[
        ("📕","Livres enregistrés",nombre_livres ,"#F8E8E8","#C0392B"),
        ("📗","Total des exemplaires",total_exemplaires ,"#E8F5E8","#27AE60"),
        ("✅","Exemplaires disponibles",disponibles ,"#E8F0E8","#2ECC71"),
        ("👤","Auteurs",nombre_auteurs ,"#E8F0F8","#2980B9"),
        ("👥","Lecteurs inscrits",nombre_lecteurs ,"#F8E8F0","#E91E63"),
        ("🔄","Emprunts en cours",emprunts_en_cours ,"#E8E8F8","#3498DB"),
        ("⏰","Emprunts en retard",emprunts_en_retard ,"#FDE8E8","#E74C3C"),
        ]

        cards_container =tk .Frame (scroll_frame ,bg ="#F5F0EB")
        cards_container .pack (fill ="x",padx =30 ,pady =15 )

        for i ,(emoji ,label ,valeur ,bg_card ,fg_icon )in enumerate (cartes_data ):
            row =i //3 
            col =i %3 

            card =tk .Frame (cards_container ,bg ="white",padx =15 ,pady =12 ,
            highlightbackground ="#E0E0E0",highlightthickness =1 )
            card .grid (row =row ,column =col ,padx =6 ,pady =6 ,sticky ="nsew")


            icon_label =tk .Label (card ,text =emoji ,bg ="white",
            font =("Segoe UI",22 ))
            icon_label .pack (side ="left",padx =(5 ,12 ))


            text_frame =tk .Frame (card ,bg ="white")
            text_frame .pack (side ="left",fill ="both",expand =True )

            tk .Label (text_frame ,text =label ,bg ="white",fg ="#888888",
            font =("Segoe UI",10 ),anchor ="w").pack (anchor ="w")
            tk .Label (text_frame ,text =str (valeur ),bg ="white",fg ="#333333",
            font =("Segoe UI",20 ,"bold"),anchor ="w").pack (anchor ="w")

        for c in range (3 ):
            cards_container .columnconfigure (c ,weight =1 )


        tk .Label (scroll_frame ,text ="📋  Derniers emprunts",bg ="#F5F0EB",fg ="#800000",
        font =("Segoe UI",16 ,"bold")).pack (anchor ="w",padx =30 ,pady =(15 ,8 ))

        table_frame =tk .Frame (scroll_frame ,bg ="white",
        highlightbackground ="#E0E0E0",highlightthickness =1 )
        table_frame .pack (fill ="both",expand =True ,padx =30 ,pady =(0 ,20 ))

        colonnes =("id","livre","lecteur","date","retour","statut")
        tableau =ttk .Treeview (table_frame ,columns =colonnes ,show ="headings",height =8 )

        entetes ={
        "id":"N°",
        "livre":"Livre",
        "lecteur":"Lecteur",
        "date":"Emprunt",
        "retour":"Retour prévu",
        "statut":"Statut"
        }

        for colonne ,nom in entetes .items ():
            tableau .heading (colonne ,text =nom )
            tableau .column (colonne ,width =120 ,anchor ="center")

        tableau .pack (fill ="both",expand =True )

        self .db .curseur .execute ("""
            SELECT
                emprunts.id_emprunt,
                livres.titre,
                lecteurs.nom || ' ' || lecteurs.prenom,
                emprunts.date_emprunt,
                emprunts.date_retour_prevue,
                emprunts.statut
            FROM emprunts
            INNER JOIN livres ON emprunts.id_livre = livres.id_livre
            INNER JOIN lecteurs ON emprunts.id_lecteur = lecteurs.id_lecteur
            ORDER BY emprunts.id_emprunt DESC
            LIMIT 10
        """)

        for emprunt in self .db .curseur .fetchall ():
            valeurs =list (emprunt )
            if valeurs [5 ]=="En cours"and valeurs [4 ]<aujourd_hui :
                valeurs [5 ]="En retard"
            tableau .insert ("",tk .END ,values =valeurs )

    def ouvrir_page (self ,page ):
        self .nettoyer_contenu ()
        self .surligner_bouton (page )

        if page =="Accueil":
            self .afficher_accueil ()
        elif page =="Livres":
            self .page_actuelle =PageLivres (self .contenu )
        elif page =="Auteurs":
            self .page_actuelle =PageAuteurs (self .contenu )
        elif page =="Lecteurs":
            self .page_actuelle =PageLecteurs (self .contenu )
        elif page =="Emprunts":
            self .page_actuelle =PageEmprunts (self .contenu )
        elif page =="Retours":
            self .page_actuelle =PageRetours (self .contenu )
        elif page =="Catégories":
            self .page_actuelle =PageCategories (self .contenu )
        elif page =="Rayons":
            self .page_actuelle =PageRayons (self .contenu )

    def quitter_application (self ):
        self .nettoyer_contenu ()
        self .db .fermer ()
        self .fenetre .destroy ()
