import pandas as pd


class CSVCleaner():

    def __init__(self, file_name):
        self.file_name = file_name

    def csv_cleaner(self, headers, categories, countries):

        fname = self.file_name

        csv_file = pd.read_csv(fname, sep=";", encoding="Latin-1")

        df = csv_file[headers]

        new_f = df.loc[
            df['main_category_fr'].isin(categories) &
            df['countries_fr'].isin(countries)
        ]

        new_f.to_csv("db_file.csv", index=False, encoding="Latin-1", sep=";")


headers_list = [
    "code", "url", "product_name", "brands", "stores", "traces_fr",
    "nutrition_grade_fr", "main_category_fr", "energy_100g", "fat_100g",
    "saturated-fat_100g", "carbohydrates_100g", "sugars_100g", "fiber_100g",
    "proteins_100g", "salt_100g", "countries_fr",
]

categories_list = [
    'Petit-déjeuners', 'Chips et frites', 'Soupes' 'Biscuits',
    'Jus de fruits 100% pur jus', 'Jus de pomme', "Jus d'orange 100% pur jus",
    'Jus de fruits', 'Jus de fruits à base de concentré', "Jus d'orange",
    "Jus d'orange à base de concentré", 'Jus de pamplemousse'
]

countries_list = ["France"]


new_csv = CSVCleaner("fr.openfoodfacts.org.products-2.csv")

new_csv.csv_cleaner(headers_list, categories_list, countries_list)
