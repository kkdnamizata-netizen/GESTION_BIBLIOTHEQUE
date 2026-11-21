# GESTION_BIBLIOTHEQUE

## 1. Présentation du projet

GESTION_BIBLIOTHEQUE est une application de bureau développée en Python. Elle permet de gérer les activités d'une bibliothèque de manière simple et organisée.

L'application dispose d'une interface graphique permettant de gérer les livres, les auteurs, les lecteurs, les catégories, les rayons, les emprunts et les retours.

## 2. Objectifs du projet

- Informatiser la gestion d'une bibliothèque.
- Faciliter l'enregistrement des livres et des lecteurs.
- Suivre les emprunts et les retours.
- Connaître la disponibilité des exemplaires.
- Consulter les statistiques de la bibliothèque.

## 3. Technologies utilisées

- **Python :** langage de programmation.
- **Programmation orientée objet (POO) :** organisation du code en classes.
- **Tkinter :** création de l'interface graphique.
- **SQLite :** gestion de la base de données.
- **Visual Studio Code :** environnement de développement.

## 4. Fonctionnalités principales

### Gestion des livres
- Ajouter un livre.
- Afficher la liste des livres.
- Rechercher un livre.
- Modifier les informations d'un livre.
- Supprimer un livre.

### Gestion des auteurs
- Ajouter, afficher, rechercher, modifier et supprimer un auteur.

### Gestion des lecteurs
- Enregistrer les lecteurs.
- Consulter leurs informations.
- Rechercher, modifier et supprimer un lecteur.

### Gestion des catégories et des rayons
- Ajouter des catégories.
- Organiser les livres par rayon.
- Modifier et supprimer les catégories et les rayons.

### Gestion des emprunts
- Enregistrer un emprunt.
- Consulter les emprunts.
- Vérifier la disponibilité des livres.
- Identifier les emprunts en retard.

### Gestion des retours
- Enregistrer le retour d'un livre.
- Consulter l'historique des retours.
- Mettre à jour automatiquement la quantité disponible.

### Tableau de bord
- Nombre de livres enregistrés.
- Nombre total d'exemplaires.
- Nombre d'exemplaires disponibles.
- Nombre d'auteurs.
- Nombre de lecteurs.
- Nombre d'emprunts en cours.
- Nombre d'emprunts en retard.

## 5. Organisation du projet

```text
GESTION_BIBLIOTHEQUE/
│
├── database/
│   ├── connexion.py
│   ├── initialisation.py
│   └── bibliotheque.db
│
├── interfaces/
│   ├── accueil.py
│   ├── livres.py
│   ├── auteurs.py
│   ├── lecteurs.py
│   ├── emprunts.py
│   ├── retours.py
│   ├── categories.py
│   └── rayons.py
│
├── models/
│   ├── livre.py
│   ├── lecteur.py
│   └── emprunt.py
│
├── services/
│   ├── gestion_livres.py
│   ├── gestion_lecteurs.py
│   └── gestion_emprunts.py
│
├── main.py
├── requirements.txt
└── README.md
```


## 6. Installation et lancement

### Prérequis

- Python 3 installé.
- Visual Studio Code.

### Étape 1 : Ouvrir le projet

Ouvrir le dossier GESTION_BIBLIOTHEQUE dans Visual Studio Code.

### Étape 2 : Activer l'environnement virtuel

Sous Windows :

```powershell
.venv\Scripts\activate
```

### Étape 3 : Lancer l'application

Dans le terminal, exécuter :

```powershell
python main.py
```

La fenêtre principale de l'application s'ouvre.

## 7. Base de données

L'application utilise SQLite pour stocker les informations.

La base de données est enregistrée dans :

```text
database/bibliotheque.db
```


Elle contient les tables nécessaires à la gestion des livres, des auteurs, des catégories, des rayons, des lecteurs, des emprunts et des retours.

## 8. Auteur du projet

Projet réalisé dans le cadre d'un travail pratique en programmation Python.

**Nom du projet :** GESTION_BIBLIOTHEQUE

**Langage :** Python

**Année :** 2026