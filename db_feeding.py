import pandas as pd
import csv
from db_models import *


class DBFeed():

    def __init__(self, file_name):
        self.file_name = file_name

    def fill_categories(self, headers):
        pass

    def fill_products(self):
        pass

    def fill_stores(self):
        pass

    def fill_brands(self):
        pass

    def fill_favs(self):
        pass


headers_list = [
    "code", "url",
    "product_name",
    "brands",
    "stores",
    "traces_fr",
    "nutrition_grade_fr",
    "main_category_fr",
    "energy_100g",
    "fat_100g",
    "saturated-fat_100g",
    "carbohydrates_100g",
    "sugars_100g",
    "fiber_100g",
    "proteins_100g",
    "salt_100g",
]

file = "fr.openfoodfacts.org.products_trie_cat.csv"

# dbf = DBFeed(file)

# dbf.fill_categories(headers_list)
