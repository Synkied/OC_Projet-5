# coding: utf8

from sys import platform as _platform

import pandas as pd

from constants import *


class CSVCleaner():

    def __init__(self, file_name):
        self.file_name = file_name

    def csv_cleaner(self, headers, categories=[], countries=[]):
        """
        Cleans the csv passed to the instanciation of the class.
        headers: a list of headers that must be in the file.
        Optionals:
        categories: a list of categories to keep in the csv
        countries: a list of countries to filter the csv
        """
        fname = self.file_name

        print("Nettoyage du fichier CSV en cours...")

        # reads the specified file.
        # sep: csv file's separator
        # low_memory: avoiding unnecessary warning msgs
        if (_platform == "linux" or
                _platform == "linux2" or
                _platform == "darwin"):
            csv_file = pd.read_csv(
                fname,
                sep="\t",
                encoding="utf-16",
                low_memory=False,
                thousands=',',
            )

        elif _platform == "win32" or _platform == "win64":
            csv_file = pd.read_csv(
                fname,
                sep="\t",
                encoding="utf-16",
                low_memory=False,
                thousands=',',
            )

        # defines a dataframe, from the passed headers
        df = csv_file[headers]

        # structures the new file to create
        # selects only specified parameters (eg. categories, countries)
        # drops products that have no name.
        new_f = df.loc[
            df['main_category_fr'].isin(categories) &
            df['countries_fr'].isin(countries) & df['product_name'].notnull() &
            df['nutrition_grade_fr'].notnull()
        ]

        # save the new file to a csv file, with the name "db_file.csv"
        new_f.to_csv(
            "../db_file.csv",
            index=False,
            encoding="utf-16",
            sep=";",
        )


if __name__ == "__main__":

    new_csv = CSVCleaner("../fr.openfoodfacts.org.products.csv")

    new_csv.csv_cleaner(HEADERS_LIST, CATEGORIES_LIST, COUNTRIES_LIST)
