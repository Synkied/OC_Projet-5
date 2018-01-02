import os.path

from csv_downloader import TqdmDL
from config_parser import *
from csv_cleaner import *
from constants import *


class InstallMenu():
    """
    InstallMenu object, helps the user to get everything he needs to
    use the OpenFoodFacts csv to db program.
    """

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
        self.config = configparser.ConfigParser()
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
        """
        Quits the app with a message.
        """
        print("Bye bye !")
        exit()

    def download_clean_file(self):
        """
        Downloads the openfoodfacts csv file and cleans it right away,
        to get a file to work with.
        """
        print()
        print("""Souhaitez-vous télécharger le fichier CSV \
d'OpenFoodFacts ? (o/n).
(Choisissez N si vous avez déjà téléchargé le fichier.)""")
        dl_answer = input(" >> ")

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
                self.main_menu_actions['main_menu'](self)

            else:
                print()
                print("Veuillez entrer une réponse valide.")
                print()
                self.main_menu_actions["1"](self)

        except KeyboardInterrupt as keyinter:
            print("Au revoir, alors!")

    def get_or_change_credentials(self):
        """
        If the config file exists, asks if the user wants to change
        credentials. Else, creates the config file with new credentials,
        inputted by user.
        """
        if os.path.exists("../" + CFG_FNAME):
            print("-" * 50)
            print("Voici vos informations actuelles :")
            self.config.read("../" + CFG_FNAME)
            print(
                "Nom d'utilisateur :",
                self.config["MySQL"]["user"],
                " /",
                "Mot de passe :",
                self.config["MySQL"]["password"]
            )
            print()
            print("Quelles informations souhaitez-vous modifier ?")
            print("=" * 50)
            print("1 - Modifier nom d'utilisateur.")
            print("2 - Modifier mot de passe.")
            print("0 - Annuler.")
            print("=" * 50)

            try:
                answer = input(" >> ")

                if answer == "1":
                    username = input(
                        "Tapez votre nouveau nom d'utilisateur : "
                    )
                    self.credentials_menu_actions[answer](self, username)

                elif answer == "2":
                    password = input(
                        "Tapez votre nouveau nom d'utilisateur : "
                    )
                    self.credentials_menu_actions[answer](self, password)

                elif answer == "0":
                    self.main_menu_actions["main_menu"](self)

                else:
                    print()
                    print("!" * 31)
                    print("Veuillez faire un choix valide.")
                    print("!" * 31)
                    self.credentials_menu_actions['credentials_menu'](self)

            except KeyboardInterrupt as keyinter:
                print("Au revoir, alors ! :)")
                exit()

        else:
            print("Création du fichier de configuration.")
            user, pwd = "", ""
            while user == "":
                user = input("Saisissez votre nom d'utilisateur MySQL: ")
            while pwd == "":
                pwd = input("Saisissez votre mot de passe MySQL: ")
            config_write("../" + CFG_FNAME, user, pwd)
            self.main_menu()

    def change_username(self, username):
        """
        Changes the username in the config file, keeping the old password
        """
        config_write(
            "../" + CFG_FNAME,
            user=username,
            pwd=self.config["MySQL"]["password"],
        )
        self.main_menu_actions['main_menu'](self)

    def change_password(self, password):
        """
        Changes the password in the config file, keeping the old username
        """
        config_write(
            "../" + CFG_FNAME,
            pwd=password,
            user=self.config["MySQL"]["user"],
        )
        self.main_menu_actions['main_menu'](self)

    """
    Main menu actions, used to quickly access some funcs
    """
    main_menu_actions = {
        'main_menu': main_menu,
        '1': download_clean_file,
        '2': get_or_change_credentials,
        '0': quit,
    }

    """
    Credentials menu actions, used to quickly access some funcs
    """
    credentials_menu_actions = {
        'credentials_menu': get_or_change_credentials,
        '1': change_username,
        '2': change_password,
        '0': main_menu,
    }


if __name__ == "__main__":
    install = InstallMenu()
