class Emprunt :

    def __init__ (self ,id_livre ,id_lecteur ,date_emprunt ,
    date_retour_prevue ,statut ="En cours"):

        self .id_livre =id_livre 
        self .id_lecteur =id_lecteur 
        self .date_emprunt =date_emprunt 
        self .date_retour_prevue =date_retour_prevue 
        self .statut =statut 
