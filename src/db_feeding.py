# coding: utf8

import pandas as pd
from peewee import *

from db_models import *
from constants import *


# #####--- FUNCTIONS ----##### #
def get_unique_df_values(df_name, col_name):
    """
    Gets unique values from a dataframe.
    """
    unique_value_list = df_name[col_name].unique()
    return unique_value_list


def csv_to_df(fname, headers):
    """
    Returns a pandas dataframe made from a csv file
    """

    # reads the specified file.
    # sep: csv file's separator
    # low_memory: avoiding unnecessary warning msgs
    csv_file = pd.read_csv(
        fname,
        sep=";",
        encoding="utf-16",
        low_memory=False
    )

    # defines a dataframe, from the passed headers
    df = csv_file[headers]
    return df


def csv_to_dict(fname, headers):
    """
    Returns a cleaned list of dicts made from a csv
    """

    # reads the specified file.
    # sep: csv file's separator
    # low_memory: avoiding unnecessary warning msgs
    csv_file = pd.read_csv(
        fname,
        sep=";",
        encoding="utf-16",
        low_memory=False
    )

    # Soft conversion of columns to pandas objects
    df_to_objects = csv_file.astype(object).infer_objects()

    # replace nan fields by None python type
    fill_nan_as_none = df_to_objects.where((pd.notnull(csv_file)), None)

    # dict conversion of pandas dataframe as records (list of dicts)
    # [{k1:v1, kn:vn}, {k1:v1, kn:vn}]
    csv_dict = fill_nan_as_none[headers].to_dict(orient="records")

    # transforms commas seperated values to list for brands and stores
    # list comprehension to strip spaces from strings in list
    for dictionary in csv_dict:
        if dictionary["brands"] is not None:
            dictionary["brands"] = [
                brand.strip()
                for brand
                in dictionary["brands"].split(',')
            ]

        if dictionary["stores"] is not None:
            dictionary["stores"] = [
                store.strip()
                for store
                in dictionary["stores"].split(',')
            ]

    return csv_dict


# #####--- CLASSES ----##### #
class DBFeed():
    def __init__(self, file_name, headers):
        self.file_name = file_name
        self.headers = headers

    def fill_categories(self, categories_col):
        """
        Fills Categories table with specified categories column
        """
        cat_dict = csv_to_dict(self.file_name, self.headers)

        for category in cat_dict:
            Category.get_or_create(name=category[categories_col])

    def fill_stores(self, stores_col):
        """
        Fills stores table with specified stores (stores_col).
        Fills the table with unique values.
        """
        dataframe = csv_to_df(self.file_name, self.headers)
        stores_list = get_unique_df_values(dataframe, stores_col)

        # stores splitting
        stores_list_split = [
            i.split(",") for i in stores_list if type(i) is not float
        ]

        # stores cleaning
        stores_set = set()
        for stores_list in stores_list_split:
            for store in stores_list:
                stores_set.add(store.strip().capitalize())

        for store in stores_set:
            Store.get_or_create(name=store)

    def fill_brands(self, brands_col):
        """
        Fills brands table with specified brands (brands_col).
        Fills the table with unique values.
        """

        dataframe = csv_to_df(self.file_name, self.headers)
        brands_list = get_unique_df_values(dataframe, brands_col)

        # brands splitting
        brands_list_split = [
            i.split(",") for i in brands_list if type(i) is not float
        ]

        # brands cleaning
        brands_set = set()
        for brands_list in brands_list_split:
            for brand in brands_list:
                brands_set.add(brand.strip().capitalize())

        for brand in brands_set:
            Brand.get_or_create(name=brand)

    def fill_products(self):
        """
        Fills Products table with specified
        """

        products_dict = csv_to_dict(self.file_name, self.headers)

        for product in products_dict:
            Product.get_or_create(
                code=product["code"],
                url=product["url"],  # unique
                name=product["product_name"],
                nutri_grade=product["nutrition_grade_fr"],
                cat=Category.get(
                    Category.name == product["main_category_fr"]
                ).id,
                energy=product["energy_100g"],
                fat=product["fat_100g"],
                carbs=product["carbohydrates_100g"],
                sugars=product["sugars_100g"],
                fibers=product["fiber_100g"],
                proteins=product["proteins_100g"],
                salt=product["salt_100g"],
                last_modified_t=product["last_modified_t"],
            )

        self.fill_productsbrands(products_dict)
        self.fill_productsstores(products_dict)

    def fill_productsbrands(self, products_dict):
        # this loop gets all dicts in the products_dict list.
        # for each dict if the brands value is not None,
        # for each brand, get or create the productsbrands table
        # based on brand name and product name of each dict.
        for dic in products_dict:
            if dic["brands"] is not None:
                for brand in dic["brands"]:
                    # get or create brands and products id
                    Productbrand.get_or_create(
                        # select brands.id
                        # from Brands table
                        # where brands.name = brand
                        brand=Brand.get(
                            Brand.name == brand
                        ).id,
                        # select product.id
                        # from Products table
                        # where products.name = dic["product_name"]
                        product=Product.get(
                            Product.name == dic["product_name"]
                        ).id
                    )

    def fill_productsstores(self, products_dict):
        # this loop gets all dicts in the products_dict list.
        # for each dict if the brands value is not None,
        # for each store, get or create the productsstores table
        # based on store name and product name of each dict.
        for dic in products_dict:
            if dic["stores"] is not None:
                for store in dic["stores"]:
                    # get or create stores and products id
                    Productstore.get_or_create(
                        # select stores.id
                        # from stores table
                        # where stores.name = store
                        store=Store.get(
                            Store.name == store
                        ).id,
                        # select products.id
                        # from Products table
                        # where products.name = dic["product_name"]
                        product=Product.get(
                            Product.name == dic["product_name"]
                        ).id
                    )

    def delete_productsstores(self, products_dict):
        for t in Productstore.select():
            b = t.product_id
            s = Product.get(Product.id == b)
            print(s.id)
            # for dic in products_dict:
            #     if dic["stores"] is not None:
            #         for store in dic["stores"]:
            #             print(store)
            # list every brands for each product, check if it is in the csv, else delete the row that is not in the csv

    def update_products(self):
        """
        Fills Products table with specified
        """
        products_dict = csv_to_dict(self.file_name, self.headers)

        for product_from_csv in products_dict:
            product_from_db = Product.get(url=product_from_csv["url"])

            if (
                product_from_db.last_modified_t <
                product_from_csv["last_modified_t"]
            ):

                product_from_db.code = product_from_csv["code"]
                product_from_db.url = product_from_csv["url"]
                product_from_db.name = product_from_csv["product_name"]
                product_from_db.nutri_grade = product_from_csv[
                    "nutrition_grade_fr"
                ]
                product_from_db.cat = Category.get(
                    Category.name == product_from_csv["main_category_fr"]
                ).id
                product_from_db.energy = product_from_csv["energy_100g"]
                product_from_db.fat = product_from_csv["fat_100g"]
                product_from_db.carbs = product_from_csv["carbohydrates_100g"]
                product_from_db.sugars = product_from_csv["sugars_100g"]
                product_from_db.fibers = product_from_csv["fiber_100g"]
                product_from_db.proteins = product_from_csv["proteins_100g"]
                product_from_db.salt = product_from_csv["salt_100g"]
                product_from_db.last_modified_t = product_from_csv[
                    "last_modified_t"
                ]
                product_from_db.save()

                self.fill_brands("brands")
                self.fill_stores("stores")
                self.fill_productsbrands(products_dict)
                self.fill_productsstores(products_dict)


def main():
    dbf = DBFeed("../" + CLEANED_CSV_FILE, HEADERS_LIST)

    # dbf.fill_categories("main_category_fr")

    # dbf.fill_stores("stores")

    # dbf.fill_brands("brands")

    # dbf.fill_products()

    products_dict = csv_to_dict("../" + CLEANED_CSV_FILE, HEADERS_LIST)
    # dbf.fill_productsstores(products_dict)
    dbf.delete_productsstores(products_dict)

    # dbf.update_products()


if __name__ == "__main__":
    main()
