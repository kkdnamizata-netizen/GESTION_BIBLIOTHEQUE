import tkinter as tk 

from database .initialisation import Initialisation 
from interfaces .accueil import Accueil 


def main ():

    bibliotheque =Initialisation ()
    bibliotheque .creer_tables ()
    bibliotheque .fermer ()

    fenetre =tk .Tk ()

    application =Accueil (fenetre )

    fenetre .mainloop ()


if __name__ =="__main__":
    main ()
