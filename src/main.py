import os.path

from csv_downloader import TqdmDL
from config_parser import *
from csv_cleaner import *
from constants import *


# download csv
# clean csv
# connect to db
# create db from csv
# use db

print("Bienvenue au sein du programme d'installation de OpenFoodFacts OC.")


class InstallMenu():

    def __init__(self):
        print()
        print("-" * 56)
        print("*" * 56)
        print(
            """Bienvenue ! Cette application vous assiste
dans l'installation d'OpenFoodFacts OC !""".upper()
        )
        print("*" * 56)
        print("-" * 56)
        self.main_menu()

    def main_menu(self):
        """
        Main menu of the app.
        Asks what the user wants to do.
        """
        print()
        print("=" * 50)
        print("Menu principal".upper().center(50))
        print("=" * 50)
        print("1 - Télécharger et nettoyer le fichier CSV.")
        print("2 - Entrer ses données d'authentification MySQL.")
        print("0 - Quitter l'application.")
        print()
        print("Saisissez votre choix : ")
        try:
            answer = input(" >> ")

            if answer == "1":
                self.main_menu_actions[answer](self)

            elif answer == "2":
                self.main_menu_actions[answer](self)

            elif answer == "0":
                self.main_menu_actions[answer](self)

            else:
                print()
                print("!" * 31)
                print("Veuillez faire un choix valide.")
                print("!" * 31)
                self.main_menu_actions['main_menu'](self)

        except KeyboardInterrupt as keyinter:
            print("Au revoir, alors ! :)")
            exit()

    def quit(self):
        print("Bye bye !")
        exit()

    def download_file(self):
        dl_answer = input("""Souhaitez-vous télécharger le fichier CSV
d'OpenFoodFacts ? (O/N).
(Choisissez N si vous avez déjà téléchargé le fichier.)""")

        try:
            if dl_answer.lower() == "o":

                # download the csv file
                dl_file = TqdmDL()
                dl_file.download_from_url(
                    CSV_URL,
                    "../",
                    CSV_FNAME,
                )

                # clean the csv file
                csv_file = CSVCleaner(dl_file)
                csv_file.csv_cleaner(
                    headers_list,
                    categories_list,
                    countries_list,
                )

            elif dl_answer.lower() == "n":
                pass

            else:
                print("Veuillez entrer une réponse valide.")

        except KeyboardInterrupt as keyinter:
            print("Au revoir, alors!")

    def get_credentials(self):
        if os.path.exists("../" + CFG_FNAME):
            print("-" * 50)
            print("Voici vos informations actuelles :")
            print("""Quelles informations souhaitez-vous modifier ?""")
            print("=" * 50)
            print("1 - Nom d'utilisateur.")
            print("2 - Mot de passe.")
            print("0 - Annuler.")
            print("=" * 50)

        else:
            print("Création du fichier de configuration.")
            config_write("../" + CFG_FNAME)

        try:
            answer = input(" >> ")

            if answer == "1":
                self.credentials_menu_actions[answer](self, answer)

            elif answer == "2":
                self.credentials_menu_actions[answer](self, answer)

            else:
                print()
                print("!" * 31)
                print("Veuillez faire un choix valide.")
                print("!" * 31)
                self.credentials_menu_actions['credentials_menu'](self)

        except KeyboardInterrupt as keyinter:
            print("Au revoir, alors ! :)")
            exit()

    def change_config(self, answer):
        if answer == "1":
            print("ok1")

        elif answer == "2":
            print("ok2")

    """
    Menu actions, used to quickly access some funcs
    """
    main_menu_actions = {
        'main_menu': main_menu,
        '1': download_file,
        '2': get_credentials,
        '0': quit,
    }

    credentials_menu_actions = {
        'credentials_menu': get_credentials,
        '1': change_config,
        '2': change_config,
        '0': main_menu,
    }


if __name__ == "__main__":
    install = InstallMenu()
