"""
Script tailored to assists users in easily downloading a file through CLI,
initializing a MySQL db and populating it.

OpenFoodFacts DB Seeker 0.1
"""

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
            """Welcome ! This script is tailored to assist you
through the installation of OpenFoodFacts DB Seeker !""".upper()
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
        print("Main menu".upper().center(50))
        print("*" * 50)
        print("1 - Download OpenFoodFacts CSV file.")
        print("2 - 'Clean' CSV file.")
        print("3 - Input your personal MySQL credentials.")
        print("4 - Create MySQL database.")
        print("5 - Populate MySQL database.")
        print("0 - Quit.")
        print()
        print("Input your choice: ")
        try:
            answer = input(" >> ")

            if answer in self.main_menu_actions.keys():
                self.main_menu_actions[answer](self)

            else:
                print()
                print("!" * 31)
                print("Please, input a valid choice.")
                print("!" * 31)
                self.main_menu_actions['main_menu'](self)

        except KeyboardInterrupt as keyinter:
            print("See you, then! :)")
            exit()

    def quit(self):
        """
        Quits the app with a message.
        """
        print("Bye bye!")
        exit()

    def download_file(self):
        """
        Downloads the openfoodfacts csv file and cleans it right away,
        to get a file to work with.
        """
        print()
        print("""Would you like to download OpenFoodFacts CSV file? (y/n).\
This may take several minutes, depending on your connection.""")
        dl_answer = input(" >> ")

        try:
            if dl_answer.lower() == "y":

                # download the csv file
                dl_file = TqdmDL()
                dl_file.download_from_url(
                    CSV_URL,
                    "../",
                    CSV_FNAME,
                )
                self.main_menu_actions['main_menu'](self)

            elif dl_answer.lower() == "n":
                self.main_menu_actions['main_menu'](self)

            else:
                print()
                print("Please input a valid input.")
                print()
                self.main_menu_actions["1"](self)

        except KeyboardInterrupt as keyinter:
            print("See you, then!")

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
            print("File was not found.\
\nHere is the original message:\n\n", colored("{}".format(fnferr), "red"))
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
            print("Your actual credentials:")
            config.read("../" + CFG_FNAME)
            print(
                "User:",
                config["MySQL"]["user"],
                " /",
                "Password:",
                config["MySQL"]["password"]
            )
            print()
            print("What credential would you like to edit?")
            print("=" * 50)
            print("1 - Edit username.")
            print("2 - Edit password.")
            print("0 - Back to main menu.")
            print("=" * 50)

            try:
                answer = input(" >> ")

                if answer == "1":
                    username = input(
                        "Input your new username: "
                    )
                    self.credentials_menu_actions[answer](self, username)

                elif answer == "2":
                    password = input(
                        "Input your new password: "
                    )
                    self.credentials_menu_actions[answer](self, password)

                elif answer == "0":
                    self.main_menu_actions["main_menu"](self)

                else:
                    print()
                    print("!" * 31)
                    print("Please, input a valid choice.")
                    print("!" * 31)
                    self.credentials_menu_actions['credentials_menu'](self)

            except KeyboardInterrupt as keyinter:
                print("See you, then! :)")
                exit()

        else:
            print("Creating .ini config file.")
            user, pwd = "", ""
            while user == "":
                user = input("Please input your MySQL username: ")
            while pwd == "":
                pwd = input("Please input your MySQL password: ")
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
                create_db_query = (
                    "CREATE DATABASE " +
                    config["MySQL"]["db"] +
                    " CHARACTER SET 'utf8'"
                )

                cursor.execute(create_db_query)

                print()
                print(colored("Database created!", "green"))
                print()

            except Exception as e:

                print(
                    "An exception occured: \n",
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
                print(colored("Tables created!", "green"))
                print()
                self.main_menu_actions['main_menu'](self)

        except pymysql.err.OperationalError as operr:
            print()
            print("!" * 83)
            print("Please, input valid informations \
or make sure MySQL is running on your computer.\
\nHere is the original message:\n\n", colored("{}".format(operr), "red"))
            print("!" * 83)
            print()
            self.main_menu_actions['main_menu'](self)

        except KeyError as kerr:
            print()
            print("!" * 83)
            print("There seems to be a missing info in your mysql_config.ini.\
\nHere is the original message:\n\n", colored("{}".format(kerr), "red"))
            print("!" * 83)
            print()
            self.main_menu_actions['main_menu'](self)

    def populate_db(self):
        """
        Populates the db from a csv file.
        """
        print()
        print("Filling database... Please wait...")
        try:
            dbf = DBFeed(file, HEADERS_LIST)
            dbf.fill_categories("main_category_fr")
            dbf.fill_stores("stores")
            dbf.fill_brands("brands")
            dbf.fill_products()

            print()
            print("Database filled ! You can now use menu.py to use the app.")
            print()
            self.main_menu_actions['main_menu'](self)

        except peewee.OperationalError as operr:
            print()
            print("An error occured:\
\n\n", colored("{}".format(operr), "red"))
            print()
            self.main_menu_actions['main_menu'](self)

        except FileNotFoundError as fnferr:
            print()
            print("The file " + file + " seems to be missing:\
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
