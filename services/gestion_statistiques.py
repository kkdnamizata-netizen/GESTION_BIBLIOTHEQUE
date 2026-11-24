from datetime import date
from database.connexion import Connexion


class GestionStatistiques:

    def __init__(self):
        self.db = Connexion()

    def obtenir_statistiques(self):
        self.db.curseur.execute("""
            SELECT
                COUNT(*),
                COALESCE(SUM(quantite_totale), 0),
                COALESCE(SUM(quantite_disponible), 0)
            FROM livres
        """)
        nb_livres, total_ex, dispo_ex = self.db.curseur.fetchone()

        self.db.curseur.execute("SELECT COUNT(*) FROM auteurs")
        nb_auteurs = self.db.curseur.fetchone()[0]

        self.db.curseur.execute("SELECT COUNT(*) FROM categories")
        nb_categories = self.db.curseur.fetchone()[0]

        self.db.curseur.execute("SELECT COUNT(*) FROM rayons")
        nb_rayons = self.db.curseur.fetchone()[0]

        self.db.curseur.execute("SELECT COUNT(*) FROM lecteurs")
        nb_lecteurs = self.db.curseur.fetchone()[0]

        self.db.curseur.execute("""
            SELECT COUNT(*) FROM emprunts WHERE statut = 'En cours'
        """)
        emprunts_en_cours = self.db.curseur.fetchone()[0]

        aujourd_hui = date.today().isoformat()
        self.db.curseur.execute("""
            SELECT COUNT(*) FROM emprunts
            WHERE statut = 'En cours' AND date_retour_prevue < ?
        """, (aujourd_hui,))
        emprunts_en_retard = self.db.curseur.fetchone()[0]

        self.db.curseur.execute("SELECT COUNT(*) FROM retours")
        total_retours = self.db.curseur.fetchone()[0]

        return {
            "nombre_livres": nb_livres,
            "total_exemplaires": total_ex,
            "exemplaires_disponibles": dispo_ex,
            "exemplaires_empruntes": total_ex - dispo_ex,
            "nombre_auteurs": nb_auteurs,
            "nombre_categories": nb_categories,
            "nombre_rayons": nb_rayons,
            "nombre_lecteurs": nb_lecteurs,
            "emprunts_en_cours": emprunts_en_cours,
            "emprunts_en_retard": emprunts_en_retard,
            "total_retours": total_retours
        }

    def fermer(self):
        self.db.fermer()
