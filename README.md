# GESTION_BIBLIOTHEQUE (Application Console)

## 1. Présentation du projet

GESTION_BIBLIOTHEQUE est une application console de bureau développée en Python. Elle permet de gérer l'intégralité des activités d'une bibliothèque directement depuis le terminal.

L'application offre un menu interactif en ligne de commande pour piloter les livres, les auteurs, les lecteurs, les catégories, les rayons, les emprunts, les retours et les statistiques.

## 2. Objectifs du projet

- Informatiser la gestion d'une bibliothèque via une application console rapide et fluide.
- Faciliter l'enregistrement et la recherche des livres, auteurs et lecteurs.
- Assurer le suivi en temps réel des emprunts, retards et retours avec mise à jour automatique des stocks.
- Fournir un tableau de bord statistique complet dans le terminal.

## 3. Technologies utilisées

- **Python 3 :** langage de programmation principal.
- **Programmation Orientée Objet (POO) :** architecture modulaire (models, services, console, database).
- **SQLite 3 :** base de données relationnelle persistante avec intégrité référentielle (`PRAGMA foreign_keys = ON`).

## 4. Fonctionnalités de l'application console

### 📊 Tableau de bord & Statistiques
- Total des livres enregistrés et nombre total d'exemplaires.
- Exemplaires disponibles vs exemplaires actuellement empruntés.
- Nombre d'auteurs, catégories, rayons et lecteurs.
- Suivi des emprunts en cours et alerte sur les emprunts en retard.
- Affichage des derniers emprunts enregistrés sous forme de tableau ASCII.

### 📚 Gestion des Livres
- Lister tous les livres avec détails (Auteur, Catégorie, Rayon, Quantités totale et disponible).
- Rechercher un livre par mot-clé (titre, auteur, catégorie, ISBN).
- Ajouter un livre avec contrôles de saisie.
- Modifier un livre avec vérification de cohérence des stocks.
- Supprimer un livre (avec protection si des emprunts sont en cours).

### ✍️ Gestion des Auteurs
- Lister tous les auteurs avec le décompte de leurs livres.
- Rechercher un auteur par nom ou prénom.
- Ajouter, modifier et supprimer un auteur (protégé si des livres lui sont associés).

### 👤 Gestion des Lecteurs
- Lister les lecteurs inscrits.
- Rechercher un lecteur par nom, prénom, téléphone ou email.
- Inscrire un nouveau lecteur avec validation de date.
- Modifier les coordonnées d'un lecteur.
- Supprimer un lecteur (protégé si des emprunts sont en cours).

### 📂 Gestion des Catégories & 🗄️ Rayons
- Organisation thématique des livres par catégorie.
- Organisation physique des livres par rayon avec description.
- Ajout, modification, suppression sécurisée.

### 🔖 Gestion des Emprunts & 📥 Retours
- Enregistrement d'un nouvel emprunt avec vérification de disponibilité en stock.
- Décrémentation automatique du stock disponible lors de l'emprunt.
- Détection automatique des emprunts en retard par rapport à la date du jour.
- Clôture d'un emprunt lors du retour et réintégration automatique de l'exemplaire au stock.
- Historique complet des retours.

## 5. Organisation du projet

```text
GESTION_BIBLIOTHEQUE/
│
├── console/
│   ├── __init__.py
│   └── app.py
│
├── database/
│   ├── connexion.py
│   ├── initialisation.py
│   └── bibliotheque.db
│
├── models/
│   ├── auteur.py
│   ├── categorie.py
│   ├── emprunt.py
│   ├── lecteur.py
│   ├── livre.py
│   └── rayon.py
│
├── services/
│   ├── gestion_auteurs.py
│   ├── gestion_categories.py
│   ├── gestion_emprunts.py
│   ├── gestion_lecteurs.py
│   ├── gestion_livres.py
│   ├── gestion_rayons.py
│   └── gestion_statistiques.py
│
├── main.py
├── requirements.txt
└── README.md
```

## 6. Lancement de l'application

### Lancement direct dans le terminal :

```powershell
python main.py
```

L'application s'exécute immédiatement dans votre terminal avec son menu interactif.
