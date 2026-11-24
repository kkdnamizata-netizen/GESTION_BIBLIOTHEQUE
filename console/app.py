import os
import sys
from datetime import date, timedelta

from models.livre import Livre
from models.lecteur import Lecteur
from services.gestion_livres import GestionLivres
from services.gestion_lecteurs import GestionLecteurs
from services.gestion_emprunts import GestionEmprunts
from services.gestion_auteurs import GestionAuteurs
from services.gestion_categories import GestionCategories
from services.gestion_rayons import GestionRayons
from services.gestion_statistiques import GestionStatistiques


class Couleurs:
    RESET = "\033[0m"
    GRAS = "\033[1m"
    ROUGE = "\033[91m"
    VERT = "\033[92m"
    JAUNE = "\033[93m"
    BLEU = "\033[94m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    BLANC = "\033[97m"
    FOND_BLEU = "\033[44m"


class ApplicationConsole:

    def __init__(self):
        self.livres_srv = GestionLivres()
        self.lecteurs_srv = GestionLecteurs()
        self.emprunts_srv = GestionEmprunts()
        self.auteurs_srv = GestionAuteurs()
        self.categories_srv = GestionCategories()
        self.rayons_srv = GestionRayons()
        self.stats_srv = GestionStatistiques()

    def effacer_ecran(self):
        os.system("cls" if os.name == "nt" else "clear")

    def pause(self):
        input(f"\n{Couleurs.JAUNE}Appuyez sur [Entrée] pour continuer...{Couleurs.RESET}")

    def afficher_banniere(self, sous_titre=""):
        largeur = 70
        ligne = "=" * largeur
        print(f"{Couleurs.CYAN}{ligne}")
        print(f"       📚  SYSTÈME DE GESTION DE BIBLIOTHÈQUE  📚")
        if sous_titre:
            print(f"       -> {sous_titre}")
        print(f"{ligne}{Couleurs.RESET}\n")

    def afficher_succes(self, message):
        print(f"\n{Couleurs.VERT}✔ SUCCÈS : {message}{Couleurs.RESET}")

    def afficher_erreur(self, message):
        print(f"\n{Couleurs.ROUGE}✘ ERREUR : {message}{Couleurs.RESET}")

    def afficher_info(self, message):
        print(f"{Couleurs.BLEU}ℹ INFO : {message}{Couleurs.RESET}")

    def demander_texte(self, invite, obligatoire=True, defaut=None):
        while True:
            prompt = f"{invite}"
            if defaut is not None:
                prompt += f" [{defaut}]"
            prompt += " : "
            valeur = input(prompt).strip()
            if not valeur and defaut is not None:
                return defaut
            if obligatoire and not valeur:
                print(f"{Couleurs.ROUGE}Ce champ est obligatoire.{Couleurs.RESET}")
                continue
            return valeur if valeur else None

    def demander_entier(self, invite, obligatoire=True, defaut=None, min_val=None, max_val=None):
        while True:
            texte = self.demander_texte(invite, obligatoire=obligatoire, defaut=str(defaut) if defaut is not None else None)
            if texte is None:
                return None
            try:
                nombre = int(texte)
                if min_val is not None and nombre < min_val:
                    print(f"{Couleurs.ROUGE}La valeur minimale autorisée est {min_val}.{Couleurs.RESET}")
                    continue
                if max_val is not None and nombre > max_val:
                    print(f"{Couleurs.ROUGE}La valeur maximale autorisée est {max_val}.{Couleurs.RESET}")
                    continue
                return nombre
            except ValueError:
                print(f"{Couleurs.ROUGE}Veuillez saisir un nombre entier valide.{Couleurs.RESET}")

    def demander_date(self, invite, obligatoire=True, defaut=None):
        while True:
            valeur = self.demander_texte(invite, obligatoire=obligatoire, defaut=defaut)
            if valeur is None:
                return None
            try:
                d = date.fromisoformat(valeur)
                return d.isoformat()
            except ValueError:
                print(f"{Couleurs.ROUGE}Format invalide. Utilisez le format AAAA-MM-JJ (ex: 2026-12-01).{Couleurs.RESET}")

    def demander_confirmation(self, invite="Êtes-vous sûr de vouloir continuer ? (o/n)"):
        rep = input(f"{Couleurs.JAUNE}{invite} : {Couleurs.RESET}").strip().lower()
        return rep in ["o", "oui", "y", "yes"]

    def afficher_tableau(self, en_tetes, lignes):
        if not lignes:
            print(f"{Couleurs.JAUNE}Aucune donnée trouvée.{Couleurs.RESET}")
            return

        largeurs = [len(str(h)) for h in en_tetes]
        lignes_str = []
        for ligne in lignes:
            l_str = [str(col) if col is not None else "-" for col in ligne]
            lignes_str.append(l_str)
            for idx, val in enumerate(l_str):
                if len(val) > largeurs[idx]:
                    largeurs[idx] = len(val)

        largeurs = [min(l, 40) for l in largeurs]

        def formater_ligne(elements):
            res = []
            for elem, larg in zip(elements, largeurs):
                e = str(elem)
                if len(e) > larg:
                    e = e[:larg - 3] + "..."
                res.append(e.ljust(larg))
            return " | ".join(res)

        separateur = "-+-".join(["-" * w for w in largeurs])
        print(f"{Couleurs.GRAS}{formater_ligne(en_tetes)}{Couleurs.RESET}")
        print(separateur)
        for ligne in lignes_str:
            print(formater_ligne(ligne))
        print(f"\n{Couleurs.CYAN}Total : {len(lignes_str)} élément(s){Couleurs.RESET}")

    def lancer(self):
        while True:
            self.effacer_ecran()
            self.afficher_banniere("Menu Principal")
            print("  [1] 📊 Tableau de bord & Statistiques")
            print("  [2] 📚 Gestion des Livres")
            print("  [3] ✍️  Gestion des Auteurs")
            print("  [4] 👤 Gestion des Lecteurs")
            print("  [5] 📂 Gestion des Catégories")
            print("  [6] 🗄️  Gestion des Rayons")
            print("  [7] 🔖 Gestion des Emprunts")
            print("  [8] 📥 Gestion des Retours")
            print("  [0] ❌ Quitter l'application")
            print("-" * 50)

            choix = input(f"{Couleurs.GRAS}Votre choix [0-8] : {Couleurs.RESET}").strip()

            if choix == "1":
                self.menu_tableau_de_bord()
            elif choix == "2":
                self.menu_livres()
            elif choix == "3":
                self.menu_auteurs()
            elif choix == "4":
                self.menu_lecteurs()
            elif choix == "5":
                self.menu_categories()
            elif choix == "6":
                self.menu_rayons()
            elif choix == "7":
                self.menu_emprunts()
            elif choix == "8":
                self.menu_retours()
            elif choix == "0":
                print(f"\n{Couleurs.VERT}Merci d'avoir utilisé le système de gestion de bibliothèque. À bientôt !{Couleurs.RESET}")
                self.fermer()
                sys.exit(0)
            else:
                self.afficher_erreur("Choix invalide. Veuillez réessayer.")
                self.pause()

    def menu_tableau_de_bord(self):
        self.effacer_ecran()
        self.afficher_banniere("Tableau de bord & Statistiques")
        try:
            stats = self.stats_srv.obtenir_statistiques()
            print(f"{Couleurs.GRAS}--- STATISTIQUES GLOBALES ---{Couleurs.RESET}")
            print(f" • Livres distincts       : {Couleurs.BLEU}{stats['nombre_livres']}{Couleurs.RESET}")
            print(f" • Total des exemplaires  : {Couleurs.BLEU}{stats['total_exemplaires']}{Couleurs.RESET}")
            print(f" • Exemplaires disponibles: {Couleurs.VERT}{stats['exemplaires_disponibles']}{Couleurs.RESET}")
            print(f" • Exemplaires empruntés  : {Couleurs.JAUNE}{stats['exemplaires_empruntes']}{Couleurs.RESET}")
            print(f" • Auteurs enregistrés    : {stats['nombre_auteurs']}")
            print(f" • Catégories             : {stats['nombre_categories']}")
            print(f" • Rayons de classement   : {stats['nombre_rayons']}")
            print(f" • Lecteurs inscrits      : {stats['nombre_lecteurs']}")
            print(f" • Emprunts en cours      : {Couleurs.JAUNE}{stats['emprunts_en_cours']}{Couleurs.RESET}")
            print(f" • Emprunts en retard     : {Couleurs.ROUGE}{stats['emprunts_en_retard']}{Couleurs.RESET}")
            print(f" • Total des retours      : {Couleurs.VERT}{stats['total_retours']}{Couleurs.RESET}")

            print(f"\n{Couleurs.GRAS}--- DERNIERS EMPRUNTS ENREGISTRÉS ---{Couleurs.RESET}")
            emprunts = self.emprunts_srv.afficher_emprunts()[:5]
            if emprunts:
                lignes = [[e[0], e[1], e[2], e[3], e[4], e[5]] for e in emprunts]
                self.afficher_tableau(["N°", "Livre", "Lecteur", "Date Emprunt", "Retour Prévu", "Statut"], lignes)
            else:
                print("Aucun emprunt enregistré.")
        except Exception as e:
            self.afficher_erreur(f"Impossible de charger les statistiques : {e}")

        self.pause()

    def menu_livres(self):
        while True:
            self.effacer_ecran()
            self.afficher_banniere("Gestion des Livres")
            print("  [1] Lister tous les livres")
            print("  [2] Rechercher un livre")
            print("  [3] Ajouter un nouveau livre")
            print("  [4] Modifier un livre")
            print("  [5] Supprimer un livre")
            print("  [0] Retour au menu principal")
            print("-" * 50)

            choix = input(f"{Couleurs.GRAS}Votre choix [0-5] : {Couleurs.RESET}").strip()

            if choix == "1":
                self.lister_livres()
            elif choix == "2":
                self.rechercher_livre()
            elif choix == "3":
                self.ajouter_livre()
            elif choix == "4":
                self.modifier_livre()
            elif choix == "5":
                self.supprimer_livre()
            elif choix == "0":
                break
            else:
                self.afficher_erreur("Choix invalide.")
                self.pause()

    def lister_livres(self):
        self.effacer_ecran()
        self.afficher_banniere("Liste des Livres")
        livres = self.livres_srv.afficher_livres_details()
        lignes = [[l[0], l[1], l[2], l[3], l[4], l[8], l[9]] for l in livres]
        self.afficher_tableau(["ID", "Titre", "Auteur", "Catégorie", "Rayon", "Total", "Dispo"], lignes)
        self.pause()

    def rechercher_livre(self):
        self.effacer_ecran()
        self.afficher_banniere("Recherche de Livres")
        terme = self.demander_texte("Mot-clé (titre, auteur, catégorie ou ISBN)")
        resultats = self.livres_srv.rechercher_livre(terme)
        lignes = [[l[0], l[1], l[2], l[3], l[4], l[8], l[9]] for l in resultats]
        self.afficher_tableau(["ID", "Titre", "Auteur", "Catégorie", "Rayon", "Total", "Dispo"], lignes)
        self.pause()

    def ajouter_livre(self):
        self.effacer_ecran()
        self.afficher_banniere("Ajouter un Livre")

        titre = self.demander_texte("Titre du livre")
        isbn = self.demander_texte("ISBN (optionnel)", obligatoire=False)
        annee = self.demander_entier("Année de publication", obligatoire=False)
        editeur = self.demander_texte("Éditeur (optionnel)", obligatoire=False)

        auteurs = self.auteurs_srv.afficher_auteurs()
        id_auteur = None
        if auteurs:
            print("\nAuteurs disponibles :")
            for a in auteurs:
                print(f"  [{a[0]}] {a[1]} {a[2]}")
            id_auteur = self.demander_entier("ID de l'auteur (ou laisser vide pour aucun)", obligatoire=False)

        categories = self.categories_srv.afficher_categories()
        id_cat = None
        if categories:
            print("\nCatégories disponibles :")
            for c in categories:
                print(f"  [{c[0]}] {c[1]}")
            id_cat = self.demander_entier("ID de la catégorie (ou laisser vide)", obligatoire=False)

        rayons = self.rayons_srv.afficher_rayons()
        id_rayon = None
        if rayons:
            print("\nRayons disponibles :")
            for r in rayons:
                print(f"  [{r[0]}] {r[1]}")
            id_rayon = self.demander_entier("ID du rayon (ou laisser vide)", obligatoire=False)

        quantite = self.demander_entier("Quantité totale d'exemplaires", obligatoire=True, defaut=1, min_val=1)

        try:
            nouveau_livre = Livre(
                titre=titre,
                isbn=isbn,
                annee_publication=annee,
                editeur=editeur,
                id_auteur=id_auteur,
                id_categorie=id_cat,
                id_rayon=id_rayon,
                quantite_totale=quantite,
                quantite_disponible=quantite
            )
            id_cree = self.livres_srv.ajouter_livre(nouveau_livre)
            self.afficher_succes(f"Livre ajouté avec succès (ID #{id_cree}) !")
        except Exception as e:
            self.afficher_erreur(f"Échec de l'ajout : {e}")

        self.pause()

    def modifier_livre(self):
        self.effacer_ecran()
        self.afficher_banniere("Modifier un Livre")
        id_livre = self.demander_entier("ID du livre à modifier")
        livre_actuel = self.livres_srv.obtenir_livre(id_livre)

        if not livre_actuel:
            self.afficher_erreur("Aucun livre trouvé avec cet ID.")
            self.pause()
            return

        print(f"\nModification du livre : {Couleurs.CYAN}{livre_actuel[1]}{Couleurs.RESET}")
        print("(Appuyez sur Entrée pour conserver la valeur actuelle)")

        nouveau_titre = self.demander_texte("Nouveau titre", obligatoire=False, defaut=livre_actuel[1])
        nouveau_isbn = self.demander_texte("Nouvel ISBN", obligatoire=False, defaut=livre_actuel[2] or "")
        nouvelle_annee = self.demander_entier("Nouvelle année", obligatoire=False, defaut=livre_actuel[3] or "")
        nouvel_editeur = self.demander_texte("Nouvel éditeur", obligatoire=False, defaut=livre_actuel[4] or "")

        auteurs = self.auteurs_srv.afficher_auteurs()
        if auteurs:
            print("\nAuteurs : " + ", ".join([f"[{a[0]}] {a[1]} {a[2]}" for a in auteurs]))
        nouvel_auteur = self.demander_entier("ID Auteur", obligatoire=False, defaut=livre_actuel[5] or "")

        categories = self.categories_srv.afficher_categories()
        if categories:
            print("Catégories : " + ", ".join([f"[{c[0]}] {c[1]}" for c in categories]))
        nouvelle_cat = self.demander_entier("ID Catégorie", obligatoire=False, defaut=livre_actuel[6] or "")

        rayons = self.rayons_srv.afficher_rayons()
        if rayons:
            print("Rayons : " + ", ".join([f"[{r[0]}] {r[1]}" for r in rayons]))
        nouveau_rayon = self.demander_entier("ID Rayon", obligatoire=False, defaut=livre_actuel[7] or "")

        nouvelle_qte = self.demander_entier("Quantité totale", obligatoire=True, defaut=livre_actuel[8], min_val=1)

        try:
            livre_maj = Livre(
                titre=nouveau_titre,
                isbn=nouveau_isbn if nouveau_isbn else None,
                annee_publication=nouvelle_annee,
                editeur=nouvel_editeur if nouvel_editeur else None,
                id_auteur=nouvel_auteur,
                id_categorie=nouvelle_cat,
                id_rayon=nouveau_rayon,
                quantite_totale=nouvelle_qte
            )
            self.livres_srv.modifier_livre(livre_maj, id_livre)
            self.afficher_succes("Livre mis à jour avec succès !")
        except Exception as e:
            self.afficher_erreur(f"Erreur lors de la modification : {e}")

        self.pause()

    def supprimer_livre(self):
        self.effacer_ecran()
        self.afficher_banniere("Supprimer un Livre")
        id_livre = self.demander_entier("ID du livre à supprimer")
        livre = self.livres_srv.obtenir_livre(id_livre)

        if not livre:
            self.afficher_erreur("Livre introuvable.")
            self.pause()
            return

        if self.demander_confirmation(f"Êtes-vous sûr de vouloir supprimer '{livre[1]}' (ID #{id_livre}) ?"):
            try:
                self.livres_srv.supprimer_livre(id_livre)
                self.afficher_succes("Livre supprimé avec succès.")
            except Exception as e:
                self.afficher_erreur(f"Impossible de supprimer : {e}")
        else:
            self.afficher_info("Suppression annulée.")

        self.pause()

    def menu_auteurs(self):
        while True:
            self.effacer_ecran()
            self.afficher_banniere("Gestion des Auteurs")
            print("  [1] Lister tous les auteurs")
            print("  [2] Rechercher un auteur")
            print("  [3] Ajouter un auteur")
            print("  [4] Modifier un auteur")
            print("  [5] Supprimer un auteur")
            print("  [0] Retour au menu principal")
            print("-" * 50)

            choix = input(f"{Couleurs.GRAS}Votre choix [0-5] : {Couleurs.RESET}").strip()

            if choix == "1":
                self.effacer_ecran()
                self.afficher_banniere("Liste des Auteurs")
                auteurs = self.auteurs_srv.afficher_auteurs_avec_stats()
                lignes = [[a[0], a[1], a[2], f"{a[3]} livre(s)"] for a in auteurs]
                self.afficher_tableau(["ID", "Nom", "Prénom", "Livres associés"], lignes)
                self.pause()
            elif choix == "2":
                self.effacer_ecran()
                self.afficher_banniere("Recherche d'Auteurs")
                terme = self.demander_texte("Nom ou prénom recherché")
                res = self.auteurs_srv.rechercher_auteur(terme)
                self.afficher_tableau(["ID", "Nom", "Prénom"], res)
                self.pause()
            elif choix == "3":
                self.effacer_ecran()
                self.afficher_banniere("Ajouter un Auteur")
                nom = self.demander_texte("Nom de l'auteur")
                prenom = self.demander_texte("Prénom (optionnel)", obligatoire=False)
                try:
                    nouvel_id = self.auteurs_srv.ajouter_auteur(nom, prenom)
                    self.afficher_succes(f"Auteur créé avec succès (ID #{nouvel_id}).")
                except Exception as e:
                    self.afficher_erreur(f"Erreur : {e}")
                self.pause()
            elif choix == "4":
                self.effacer_ecran()
                self.afficher_banniere("Modifier un Auteur")
                id_a = self.demander_entier("ID de l'auteur à modifier")
                auteur = self.auteurs_srv.obtenir_auteur(id_a)
                if not auteur:
                    self.afficher_erreur("Auteur introuvable.")
                else:
                    nom = self.demander_texte("Nouveau nom", defaut=auteur[1])
                    prenom = self.demander_texte("Nouveau prénom", obligatoire=False, defaut=auteur[2])
                    try:
                        self.auteurs_srv.modifier_auteur(id_a, nom, prenom)
                        self.afficher_succes("Auteur modifié avec succès.")
                    except Exception as e:
                        self.afficher_erreur(f"Erreur : {e}")
                self.pause()
            elif choix == "5":
                self.effacer_ecran()
                self.afficher_banniere("Supprimer un Auteur")
                id_a = self.demander_entier("ID de l'auteur à supprimer")
                auteur = self.auteurs_srv.obtenir_auteur(id_a)
                if not auteur:
                    self.afficher_erreur("Auteur introuvable.")
                elif self.demander_confirmation(f"Supprimer l'auteur '{auteur[1]} {auteur[2]}' ?"):
                    try:
                        self.auteurs_srv.supprimer_auteur(id_a)
                        self.afficher_succes("Auteur supprimé.")
                    except Exception as e:
                        self.afficher_erreur(f"Erreur : {e}")
                self.pause()
            elif choix == "0":
                break

    def menu_lecteurs(self):
        while True:
            self.effacer_ecran()
            self.afficher_banniere("Gestion des Lecteurs")
            print("  [1] Lister tous les lecteurs")
            print("  [2] Rechercher un lecteur")
            print("  [3] Inscrire un nouveau lecteur")
            print("  [4] Modifier un lecteur")
            print("  [5] Supprimer un lecteur")
            print("  [0] Retour au menu principal")
            print("-" * 50)

            choix = input(f"{Couleurs.GRAS}Votre choix [0-5] : {Couleurs.RESET}").strip()

            if choix == "1":
                self.effacer_ecran()
                self.afficher_banniere("Liste des Lecteurs")
                lecteurs = self.lecteurs_srv.afficher_lecteurs()
                lignes = [[l[0], f"{l[1]} {l[2]}", l[3] or "-", l[4] or "-", l[6]] for l in lecteurs]
                self.afficher_tableau(["ID", "Nom & Prénom", "Téléphone", "Email", "Date Inscription"], lignes)
                self.pause()
            elif choix == "2":
                self.effacer_ecran()
                self.afficher_banniere("Rechercher un Lecteur")
                terme = self.demander_texte("Nom, prénom, téléphone ou email")
                res = self.lecteurs_srv.rechercher_lecteur(terme)
                lignes = [[l[0], f"{l[1]} {l[2]}", l[3] or "-", l[4] or "-", l[6]] for l in res]
                self.afficher_tableau(["ID", "Nom & Prénom", "Téléphone", "Email", "Date Inscription"], lignes)
                self.pause()
            elif choix == "3":
                self.effacer_ecran()
                self.afficher_banniere("Inscrire un Lecteur")
                nom = self.demander_texte("Nom")
                prenom = self.demander_texte("Prénom")
                tel = self.demander_texte("Téléphone (optionnel)", obligatoire=False)
                email = self.demander_texte("Email (optionnel)", obligatoire=False)
                adresse = self.demander_texte("Adresse (optionnel)", obligatoire=False)
                date_insc = self.demander_date("Date d'inscription", obligatoire=False, defaut=date.today().isoformat())
                try:
                    lec = Lecteur(nom, prenom, tel, email, adresse, date_insc)
                    nouvel_id = self.lecteurs_srv.ajouter_lecteur(lec)
                    self.afficher_succes(f"Lecteur inscrit avec succès (ID #{nouvel_id}).")
                except Exception as e:
                    self.afficher_erreur(f"Erreur d'inscription : {e}")
                self.pause()
            elif choix == "4":
                self.effacer_ecran()
                self.afficher_banniere("Modifier un Lecteur")
                id_l = self.demander_entier("ID du lecteur à modifier")
                lecteur = self.lecteurs_srv.obtenir_lecteur(id_l)
                if not lecteur:
                    self.afficher_erreur("Lecteur introuvable.")
                else:
                    nom = self.demander_texte("Nom", defaut=lecteur[1])
                    prenom = self.demander_texte("Prénom", defaut=lecteur[2])
                    tel = self.demander_texte("Téléphone", obligatoire=False, defaut=lecteur[3] or "")
                    email = self.demander_texte("Email", obligatoire=False, defaut=lecteur[4] or "")
                    adresse = self.demander_texte("Adresse", obligatoire=False, defaut=lecteur[5] or "")
                    try:
                        lec = Lecteur(nom, prenom, tel, email, adresse)
                        self.lecteurs_srv.modifier_lecteur(lec, id_l)
                        self.afficher_succes("Informations du lecteur mises à jour.")
                    except Exception as e:
                        self.afficher_erreur(f"Erreur : {e}")
                self.pause()
            elif choix == "5":
                self.effacer_ecran()
                self.afficher_banniere("Supprimer un Lecteur")
                id_l = self.demander_entier("ID du lecteur à supprimer")
                lecteur = self.lecteurs_srv.obtenir_lecteur(id_l)
                if not lecteur:
                    self.afficher_erreur("Lecteur introuvable.")
                elif self.demander_confirmation(f"Supprimer le lecteur '{lecteur[1]} {lecteur[2]}' ?"):
                    try:
                        self.lecteurs_srv.supprimer_lecteur(id_l)
                        self.afficher_succes("Lecteur supprimé.")
                    except Exception as e:
                        self.afficher_erreur(f"Erreur : {e}")
                self.pause()
            elif choix == "0":
                break

    def menu_categories(self):
        while True:
            self.effacer_ecran()
            self.afficher_banniere("Gestion des Catégories")
            print("  [1] Lister toutes les catégories")
            print("  [2] Ajouter une catégorie")
            print("  [3] Modifier une catégorie")
            print("  [4] Supprimer une catégorie")
            print("  [0] Retour au menu principal")
            print("-" * 50)

            choix = input(f"{Couleurs.GRAS}Votre choix [0-4] : {Couleurs.RESET}").strip()

            if choix == "1":
                self.effacer_ecran()
                self.afficher_banniere("Liste des Catégories")
                cats = self.categories_srv.afficher_categories_avec_stats()
                lignes = [[c[0], c[1], f"{c[2]} livre(s)"] for c in cats]
                self.afficher_tableau(["ID", "Nom de la Catégorie", "Livres rattachés"], lignes)
                self.pause()
            elif choix == "2":
                self.effacer_ecran()
                self.afficher_banniere("Ajouter une Catégorie")
                nom = self.demander_texte("Nom de la catégorie")
                try:
                    nouvel_id = self.categories_srv.ajouter_categorie(nom)
                    self.afficher_succes(f"Catégorie créée (ID #{nouvel_id}).")
                except Exception as e:
                    self.afficher_erreur(f"Erreur : {e}")
                self.pause()
            elif choix == "3":
                self.effacer_ecran()
                self.afficher_banniere("Modifier une Catégorie")
                id_c = self.demander_entier("ID de la catégorie à modifier")
                cat = self.categories_srv.obtenir_categorie(id_c)
                if not cat:
                    self.afficher_erreur("Catégorie introuvable.")
                else:
                    nom = self.demander_texte("Nouveau nom", defaut=cat[1])
                    try:
                        self.categories_srv.modifier_categorie(id_c, nom)
                        self.afficher_succes("Catégorie modifiée avec succès.")
                    except Exception as e:
                        self.afficher_erreur(f"Erreur : {e}")
                self.pause()
            elif choix == "4":
                self.effacer_ecran()
                self.afficher_banniere("Supprimer une Catégorie")
                id_c = self.demander_entier("ID de la catégorie à supprimer")
                cat = self.categories_srv.obtenir_categorie(id_c)
                if not cat:
                    self.afficher_erreur("Catégorie introuvable.")
                elif self.demander_confirmation(f"Supprimer la catégorie '{cat[1]}' ?"):
                    try:
                        self.categories_srv.supprimer_categorie(id_c)
                        self.afficher_succes("Catégorie supprimée.")
                    except Exception as e:
                        self.afficher_erreur(f"Erreur : {e}")
                self.pause()
            elif choix == "0":
                break

    def menu_rayons(self):
        while True:
            self.effacer_ecran()
            self.afficher_banniere("Gestion des Rayons")
            print("  [1] Lister tous les rayons")
            print("  [2] Ajouter un rayon")
            print("  [3] Modifier un rayon")
            print("  [4] Supprimer un rayon")
            print("  [0] Retour au menu principal")
            print("-" * 50)

            choix = input(f"{Couleurs.GRAS}Votre choix [0-4] : {Couleurs.RESET}").strip()

            if choix == "1":
                self.effacer_ecran()
                self.afficher_banniere("Liste des Rayons")
                rayons = self.rayons_srv.afficher_rayons_avec_stats()
                lignes = [[r[0], r[1], r[2] or "-", f"{r[3]} livre(s)"] for r in rayons]
                self.afficher_tableau(["ID", "Nom du Rayon", "Description", "Livres placés"], lignes)
                self.pause()
            elif choix == "2":
                self.effacer_ecran()
                self.afficher_banniere("Ajouter un Rayon")
                nom = self.demander_texte("Nom du rayon")
                desc = self.demander_texte("Description (optionnel)", obligatoire=False)
                try:
                    nouvel_id = self.rayons_srv.ajouter_rayon(nom, desc)
                    self.afficher_succes(f"Rayon créé (ID #{nouvel_id}).")
                except Exception as e:
                    self.afficher_erreur(f"Erreur : {e}")
                self.pause()
            elif choix == "3":
                self.effacer_ecran()
                self.afficher_banniere("Modifier un Rayon")
                id_r = self.demander_entier("ID du rayon à modifier")
                rayon = self.rayons_srv.obtenir_rayon(id_r)
                if not rayon:
                    self.afficher_erreur("Rayon introuvable.")
                else:
                    nom = self.demander_texte("Nouveau nom", defaut=rayon[1])
                    desc = self.demander_texte("Nouvelle description", obligatoire=False, defaut=rayon[2] or "")
                    try:
                        self.rayons_srv.modifier_rayon(id_r, nom, desc)
                        self.afficher_succes("Rayon modifié avec succès.")
                    except Exception as e:
                        self.afficher_erreur(f"Erreur : {e}")
                self.pause()
            elif choix == "4":
                self.effacer_ecran()
                self.afficher_banniere("Supprimer un Rayon")
                id_r = self.demander_entier("ID du rayon à supprimer")
                rayon = self.rayons_srv.obtenir_rayon(id_r)
                if not rayon:
                    self.afficher_erreur("Rayon introuvable.")
                elif self.demander_confirmation(f"Supprimer le rayon '{rayon[1]}' ?"):
                    try:
                        self.rayons_srv.supprimer_rayon(id_r)
                        self.afficher_succes("Rayon supprimé.")
                    except Exception as e:
                        self.afficher_erreur(f"Erreur : {e}")
                self.pause()
            elif choix == "0":
                break

    def menu_emprunts(self):
        while True:
            self.effacer_ecran()
            self.afficher_banniere("Gestion des Emprunts")
            print("  [1] Afficher tous les emprunts")
            print("  [2] Afficher uniquement les emprunts en cours")
            print("  [3] Afficher les emprunts en retard ⚠️")
            print("  [4] Enregistrer un nouvel emprunt")
            print("  [0] Retour au menu principal")
            print("-" * 50)

            choix = input(f"{Couleurs.GRAS}Votre choix [0-4] : {Couleurs.RESET}").strip()

            if choix == "1":
                self.effacer_ecran()
                self.afficher_banniere("Historique complet des Emprunts")
                emprunts = self.emprunts_srv.afficher_emprunts()
                lignes = [[e[0], e[1], e[2], e[3], e[4], e[5]] for e in emprunts]
                self.afficher_tableau(["N°", "Livre", "Lecteur", "Date Emprunt", "Retour Prévu", "Statut"], lignes)
                self.pause()
            elif choix == "2":
                self.effacer_ecran()
                self.afficher_banniere("Emprunts En Cours")
                emprunts = self.emprunts_srv.afficher_emprunts_en_cours()
                lignes = [[e[0], e[1], e[2], e[3], e[4], e[5]] for e in emprunts]
                self.afficher_tableau(["N°", "Livre", "Lecteur", "Date Emprunt", "Retour Prévu", "Statut"], lignes)
                self.pause()
            elif choix == "3":
                self.effacer_ecran()
                self.afficher_banniere("Emprunts en Retard")
                retards = self.emprunts_srv.afficher_retards()
                if retards:
                    lignes = [[e[0], e[1], e[2], e[3], e[4], f"{Couleurs.ROUGE}EN RETARD{Couleurs.RESET}"] for e in retards]
                    self.afficher_tableau(["N°", "Livre", "Lecteur", "Date Emprunt", "Retour Prévu", "Alerte"], lignes)
                else:
                    self.afficher_succes("Aucun emprunt en retard actuellement !")
                self.pause()
            elif choix == "4":
                self.enregistrer_nouvel_emprunt()
            elif choix == "0":
                break

    def enregistrer_nouvel_emprunt(self):
        self.effacer_ecran()
        self.afficher_banniere("Enregistrer un Emprunt")

        id_livre = self.demander_entier("ID du livre à emprunter")
        livre = self.livres_srv.obtenir_livre(id_livre)
        if not livre:
            self.afficher_erreur("Livre introuvable.")
            self.pause()
            return

        if livre[9] <= 0:
            self.afficher_erreur(f"Stock épuisé pour '{livre[1]}' (Disponibles : {livre[9]}).")
            self.pause()
            return

        print(f"Livre sélectionné : {Couleurs.VERT}{livre[1]}{Couleurs.RESET} ({livre[9]} exemplaire(s) disponible(s))")

        id_lecteur = self.demander_entier("ID du lecteur emprunteur")
        lecteur = self.lecteurs_srv.obtenir_lecteur(id_lecteur)
        if not lecteur:
            self.afficher_erreur("Lecteur introuvable.")
            self.pause()
            return

        print(f"Lecteur : {Couleurs.VERT}{lecteur[1]} {lecteur[2]}{Couleurs.RESET}")

        ajd = date.today()
        date_emp = self.demander_date("Date de l'emprunt", defaut=ajd.isoformat())
        date_prevue_defaut = (ajd + timedelta(days=14)).isoformat()
        date_prevue = self.demander_date("Date de retour prévue (+14 jours par défaut)", defaut=date_prevue_defaut)

        try:
            nouvel_id = self.emprunts_srv.emprunter_livre(id_livre, id_lecteur, date_emp, date_prevue)
            self.afficher_succes(f"Emprunt #{nouvel_id} validé avec succès ! Stock mis à jour.")
        except Exception as e:
            self.afficher_erreur(f"Échec de l'emprunt : {e}")

        self.pause()

    def menu_retours(self):
        while True:
            self.effacer_ecran()
            self.afficher_banniere("Gestion des Retours")
            print("  [1] Enregistrer le retour d'un livre")
            print("  [2] Historique des retours effectués")
            print("  [0] Retour au menu principal")
            print("-" * 50)

            choix = input(f"{Couleurs.GRAS}Votre choix [0-2] : {Couleurs.RESET}").strip()

            if choix == "1":
                self.enregistrer_retour_livre()
            elif choix == "2":
                self.effacer_ecran()
                self.afficher_banniere("Historique des Retours")
                retours = self.emprunts_srv.afficher_retours()
                lignes = [[r[0], r[1], r[2], r[3], r[4], r[5], r[6]] for r in retours]
                self.afficher_tableau(["ID Retour", "N° Emprunt", "Livre", "Lecteur", "Date Emprunt", "Date Prévue", "Date Effective"], lignes)
                self.pause()
            elif choix == "0":
                break

    def enregistrer_retour_livre(self):
        self.effacer_ecran()
        self.afficher_banniere("Enregistrer un Retour de Livre")

        emprunts_actifs = self.emprunts_srv.afficher_emprunts_en_cours()
        if not emprunts_actifs:
            self.afficher_info("Aucun emprunt en cours à retourner.")
            self.pause()
            return

        print("Emprunts en cours actuellement :")
        lignes = [[e[0], e[1], e[2], e[3], e[4]] for e in emprunts_actifs]
        self.afficher_tableau(["N° Emprunt", "Livre", "Lecteur", "Date Emprunt", "Retour Prévu"], lignes)

        print("-" * 60)
        id_emprunt = self.demander_entier("Numéro de l'emprunt à clôturer")

        trouve = any(e[0] == id_emprunt for e in emprunts_actifs)
        if not trouve:
            self.afficher_erreur("Ce numéro d'emprunt n'est pas dans la liste des emprunts en cours.")
            self.pause()
            return

        date_ret = self.demander_date("Date de retour effective", defaut=date.today().isoformat())

        try:
            self.emprunts_srv.enregistrer_retour(id_emprunt, date_ret)
            self.afficher_succes(f"Retour de l'emprunt #{id_emprunt} validé ! L'exemplaire a été réintégré au stock.")
        except Exception as e:
            self.afficher_erreur(f"Échec de l'enregistrement du retour : {e}")

        self.pause()

    def fermer(self):
        self.livres_srv.fermer()
        self.lecteurs_srv.fermer()
        self.emprunts_srv.fermer()
        self.auteurs_srv.fermer()
        self.categories_srv.fermer()
        self.rayons_srv.fermer()
        self.stats_srv.fermer()
