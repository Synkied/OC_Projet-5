import pandas as pd
from db_models import *

file = ("db_file.csv")


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
        fname, sep=";", encoding="utf-8", low_memory=False
    )

    # defines a dataframe, from the passed headers
    df = csv_file[headers]
    return df


def csv_to_dict(fname, headers):
    """
    Returns a pandas dataframe made from a csv file
    """
    # reads the specified file.
    # sep: csv file's separator
    # low_memory: avoiding unnecessary warning msgs
    csv_file = pd.read_csv(
        fname, sep=";", encoding="utf-8", low_memory=False
    )

    # defines a dataframe, from the passed headers
    csv_dict = csv_file[headers].to_dict(orient="records")
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

        for categorie in cat_dict:
            Categories.get_or_create(name=categorie[categories_col])

    def fill_products(self):
        """
        Fills Products table with specified
        """

        products_dict = csv_to_dict(self.file_name, self.headers)

        for product in products_dict:
            Products.get_or_create(name=product["product_name"], brand=product[brand_id], store=product[store_id], cat=product[category_id])

    # def fill_stores(self, stores_col):
    #     """
    #     Fills Products table with specified
    #     """
    #     dataframe = csv_to_df(self.file_name, self.headers)
    #     stores_list = get_unique_df_values(dataframe, stores_col)

    #     # stores splitting
    #     stores_list_split = [
    #         i.split(",") for i in stores_list if type(i) is not float
    #     ]

    #     # stores cleaning
    #     stores_set = set()
    #     for stores_list in stores_list_split:
    #         for store in stores_list:
    #             stores_set.add(store.strip().capitalize())

    #     for store in stores_set:
    #         Stores.get_or_create(name=store)

    # def fill_brands(self, brands_col):
    #     """
    #     Fills Products table with specified
    #     """
    #     dataframe = csv_to_df(self.file_name, self.headers)
    #     brands_list = get_unique_df_values(dataframe, brands_col)

    #     for brand in brands_list:
    #         Brands.get_or_create(name=brand)

    # def fill_favs(self):
    #     pass


headers_list = [
    "code",
    "url",
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


tables = [
    Categories,
    Products,
    Stores,
    Brands,
    Favorites

]

file = "db_file.csv"

dbf = DBFeed(file, headers_list)


dbf.fill_categories("main_category_fr")

# dbf.fill_brands("brands")

dbf.fill_products()


# my_cat = Categories.get_or_create(name="Test_cat")

# print(my_cat2[0].url)

# for i in my_cat:
#     print(i)

# test = Products.create(name="test", cat=my_cat[0].id)

# get cats
# get or create cats
# get or create products
