import pandas as pd


class CSVCleaner():

    # #TODO: RAISE ERRORS
    # code: puissances

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

        # reads the specified file.
        # sep: csv file's separator
        # low_memory: avoiding unnecessary warning msgs
        csv_file = pd.read_csv(
            fname, sep=";", encoding="Latin-1", low_memory=False, thousands=','
        )

        # defines a dataframe, from the passed headers
        df = csv_file[headers]

        # structures the new file to create
        # selects only specified parameters (eg. categories, countries)
        # drops products that have no name.
        new_f = df.loc[
            df['main_category_fr'].isin(categories) &
            df['countries_fr'].isin(countries) & df['product_name'].notnull()
        ]

        # save the new file to a csv file, with the name "db_file.csv"
        new_f.to_csv("db_file.csv", index=False, encoding="utf-8", sep=";")


headers_list = [
    "code",
    "url",
    "product_name",
    "brands",
    "stores",
    "nutrition_grade_fr",
    "main_category_fr",
    "energy_100g",
    "fat_100g",
    "carbohydrates_100g",
    "sugars_100g",
    "fiber_100g",
    "proteins_100g",
    "salt_100g",
    'countries_fr',
]

categories_list = [
    'Petit-déjeuners',
    'Chips et frites',
    'Soupes',
    'Biscuits',
    'Jus de fruits 100% pur jus',
    'Jus de pomme',
    "Jus d'orange 100% pur jus",
    'Jus de fruits',
    'Jus de fruits à base de concentré',
    "Jus d'orange",
    "Jus d'orange à base de concentré",
    'Jus de pamplemousse',
]

countries_list = ["France"]


new_csv = CSVCleaner("fr.openfoodfacts.org.products-2.csv")

new_csv.csv_cleaner(headers_list, categories_list, countries_list)
