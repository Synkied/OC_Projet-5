# coding: utf8

import os.path

import pymysql
import peewee
from colorama import init
from termcolor import colored

from csv_downloader import TqdmDL
from config_parser import *
from csv_cleaner import *
from constants import *
from db_models import *
from db_feeding import *


init()  # inits colorama


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
        print("*" * 50)
        print("Menu principal".upper().center(50))
        print("*" * 50)
        print("1 - Télécharger le fichier CSV.")
        print("2 - Nettoyer le fichier CSV.")
        print("3 - Entrer ses données d'authentification MySQL.")
        print("4 - Créer la base de données MySQL.")
        print("5 - Peupler la base de données MySQL.")
        print("0 - Quitter l'application.")
        print()
        print("Saisissez votre choix : ")
        try:
            answer = input(" >> ")

            if answer in self.main_menu_actions.keys():
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

    def download_file(self):
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

            elif dl_answer.lower() == "n":
                self.main_menu_actions['main_menu'](self)

            else:
                print()
                print("Veuillez entrer une réponse valide.")
                print()
                self.main_menu_actions["1"](self)

        except KeyboardInterrupt as keyinter:
            print("Au revoir, alors!")

    def clean_file(self):
        # clean the csv file
        try:
            csv_file = CSVCleaner("../" + CSV_FNAME)
            csv_file.csv_cleaner(
                HEADERS_LIST,
                CATEGORIES_LIST,
                COUNTRIES_LIST,
            )
            self.main_menu_actions['main_menu'](self)

        except FileNotFoundError as fnferr:
            print()
            print("!" * 63)
            print("Le fichier n'a pas été trouvé.\
\nVoici le message original :\n\n", colored("{}".format(fnferr), "red"))
            print("!" * 63)
            print()
            self.main_menu_actions['main_menu'](self)

    def get_or_change_credentials(self):
        """
        If the config file exists, asks if the user wants to change
        credentials. Else, creates the config file with new credentials,
        inputted by user.
        """
        if os.path.exists("../" + CFG_FNAME):
            print("-" * 50)
            print("Voici vos informations actuelles :")
            config.read("../" + CFG_FNAME)
            print(
                "Nom d'utilisateur :",
                config["MySQL"]["user"],
                " /",
                "Mot de passe :",
                config["MySQL"]["password"]
            )
            print()
            print("Quelles informations souhaitez-vous modifier ?")
            print("=" * 50)
            print("1 - Modifier nom d'utilisateur.")
            print("2 - Modifier mot de passe.")
            print("0 - Retour au menu principal.")
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
                        "Tapez votre nouveau mot de passe : "
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
            self.credentials_menu_actions["credentials_menu"](self)

    def change_username(self, username):
        """
        Changes the username in the config file, keeping the old password
        """
        config_write(
            "../" + CFG_FNAME,
            user=username,
            pwd=config["MySQL"]["password"],
        )
        self.credentials_menu_actions['credentials_menu'](self)

    def change_password(self, password):
        """
        Changes the password in the config file, keeping the old username
        """
        config_write(
            "../" + CFG_FNAME,
            pwd=password,
            user=config["MySQL"]["user"],
        )
        self.credentials_menu_actions['credentials_menu'](self)

    def create_db(self):
        """
        Creates the database using the config file
        """
        config.read("../" + CFG_FNAME)
        try:
            """
            Connects to the database using pymysql.
            Used to create the db from python.
            """
            connection = pymysql.connect(
                host=config["MySQL"]["host"],
                user=config["MySQL"]["user"],
                password=config["MySQL"]["password"],
                charset="utf8",
            )

            try:
                """
                Creates the db using a mysql injector in python.
                """
                cursor = connection.cursor()
                create_db_query = "CREATE DATABASE " + config["MySQL"]["db"] + " CHARACTER SET 'utf8'"

                cursor.execute(create_db_query)

                print()
                print(colored("Base de données créée !", "green"))
                print()

            except Exception as e:

                print(
                    "Une exception s'est produite : \n",
                    colored("{}".format(e), "red")
                )
                self.main_menu_actions['main_menu'](self)

            else:
                connection.close()  # close pymysql connection

                openfoodfacts_db.connect()  # open peewee connection
                openfoodfacts_db.create_tables(
                    [
                        Brands,
                        Categories,
                        Stores,
                        Products,
                        Favorites,
                        Productsbrands,
                        Productsstores,
                    ]
                )
                print(colored("Tables créées !", "green"))
                print()
                self.main_menu_actions['main_menu'](self)

        except pymysql.err.OperationalError as operr:
            print()
            print("!" * 83)
            print("Veuillez renseigner des identifiants corrects \
ou lancer MySQL sur votre ordinateur.\
\nVoici le message original :\n\n", colored("{}".format(operr), "red"))
            print("!" * 83)
            print()
            self.main_menu_actions['main_menu'](self)

        except KeyError as kerr:
            print()
            print("!" * 83)
            print("Il semblerait qu'une information manque au sein du fichier\
de configuration mysql_config.ini.\
\nVoici le message original :\n\n", colored("{}".format(kerr), "red"))
            print("!" * 83)
            print()
            self.main_menu_actions['main_menu'](self)

    def populate_db(self):
        """
        Populates the db from a csv file.
        """
        print()
        print("Remplissage de la base de données...")
        try:
            dbf = DBFeed(file, HEADERS_LIST)
            dbf.fill_categories("main_category_fr")
            dbf.fill_stores("stores")
            dbf.fill_brands("brands")
            dbf.fill_products()

            print()
            print("Base de données remplie ! Vous pouvez maintenant utiliser \
menu.py pour utiliser l'application.")
            print()
            self.main_menu_actions['main_menu'](self)

        except peewee.OperationalError as operr:
            print()
            print("Une erreur s'est produite :\
\n\n", colored("{}".format(operr), "red"))
            print()
            self.main_menu_actions['main_menu'](self)

        except FileNotFoundError as fnferr:
            print()
            print("Il semblerait que le fichier " + file + " n'existe pas :\
\n\n", colored("{}".format(fnferr), "red"))
            print()
            self.main_menu_actions['main_menu'](self)

    """
    Main menu actions, used to quickly access some funcs
    """
    main_menu_actions = {
        'main_menu': main_menu,
        '1': download_file,
        '2': clean_file,
        '3': get_or_change_credentials,
        '4': create_db,
        '5': populate_db,
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
