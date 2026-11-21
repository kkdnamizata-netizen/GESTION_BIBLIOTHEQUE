# GESTION_BIBLIOTHEQUE

## Technologies utilisées
- **Python** : langage de programmation.
- **POO** : programmation orientée objet.
- **Tkinter** : création de l'interface graphique.
- **SQLite** : système de gestion de base de données.

## Arborescence du projet

text
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
│   ├── rayons.py
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


## Installation et exécution

### 1. Créer un environnement virtuel
bash
python -m venv .venv


### 2. Activer l'environnement
powershell
.venv\Scripts\activate


### 3. Lancer l'application

python main.py


## Définitions

- **Database** : contient les fichiers liés à la base de données.
- **Interfaces** : contient les fenêtres graphiques de l'application.
- **Models** : contient les classes représentant les données.
- **Services** : contient les opérations de gestion.
- **Main.py** : point de démarrage de l'application.
- **SQLite** : permet de stocker les données localement.