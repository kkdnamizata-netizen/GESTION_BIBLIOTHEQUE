from database.initialisation import Initialisation
from console.app import ApplicationConsole


def main():
    bibliotheque = Initialisation()
    bibliotheque.creer_tables()
    bibliotheque.fermer()

    app = ApplicationConsole()
    try:
        app.lancer()
    except KeyboardInterrupt:
        print("\n\nFermeture de l'application...")
        app.fermer()


if __name__ == "__main__":
    main()
