import pandas as pd


# # # def test_csv(file, headers):

# # #     # reads the specified file.
# # #     # sep: csv file's separator
# # #     # low_memory: avoiding unnecessary warning msgs
# # #     csv_file = pd.read_csv(
# # #         fname, sep=";", encoding="utf-8", low_memory=False
# # #     )

# # #     # defines a dataframe, from the passed headers
# # #     df = csv_file[headers]


# # #     new_df = list(df["stores"].unique())
# # #     print(new_df)
# # #     # t = [i.split(",") for i in new_df if type(i) is not float]
# # #     # b = set()
# # #     # for i in t:
# # #     #     for j in i:
# # #     #         b.add(j.strip().capitalize())
# # #     # print(b)

# # def csv_to_dict(fname, headers):
# #     """
# #     Returns a pandas dataframe made from a csv file
# #     """
# #     # reads the specified file.
# #     # sep: csv file's separator
# #     # low_memory: avoiding unnecessary warning msgs
# #     csv_file = pd.read_csv(
# #         fname, sep=";", encoding="utf-8", low_memory=False
# #     )

# #     # defines a dataframe, from the passed headers
# #     df_to_objects = csv_file.astype(object).infer_objects()
# #     fill_nan_as_none = df_to_objects.where((pd.notnull(csv_file)), None)

# #     csv_dict = fill_nan_as_none[headers].to_dict(orient="records")

# #     # transform commas seperated values to list for brands and stores
# #     for dictionary in csv_dict:
# #         if dictionary["brands"] is not None:
# #             dictionary["brands"] = [brand.strip() for brand in dictionary["brands"].split(',')]
# #         if dictionary["stores"] is not None:
# #             dictionary["stores"] = [store.strip() for store in dictionary["stores"].split(',')]

# #     return csv_dict


# # fname = "db_file.csv"

# # headers_list = [
# #     "code",
# #     "url",
# #     "product_name",
# #     "brands",
# #     "stores",
# #     "nutrition_grade_fr",
# #     "main_category_fr",
# #     "energy_100g",
# #     "fat_100g",
# #     "carbohydrates_100g",
# #     "sugars_100g",
# #     "fiber_100g",
# #     "proteins_100g",
# #     "salt_100g",
# # ]


# # t = csv_to_dict(fname, headers_list)

# # for d in t:
# #     print(d)


# # # d = [{"test": "tss, saa, cac"}]

# # # for i in d:
# # #     for j in i["test"]:
# # #         print(j)


# import requests
# from contextlib import closing
# import csv
# import codecs

# import pandas as pd

# from io import StringIO

# from constants import *
# from tqdm import tqdm, tqdm_pandas



# # url = "https://world.openfoodfacts.org/data/fr.openfoodfacts.org.products.csv"

# # with closing(requests.get(url, stream=True)) as r:
# #     reader = csv.reader(codecs.iterdecode(r.iter_lines(), encoding='utf-8'), delimiter='\t', quotechar='"')
# #     with open("../fr.openfoodfacts.org.products.csv", "w", encoding="utf-16") as f:
# #         test = csv.writer(f, delimiter="\t", lineterminator="\n", quotechar='"')
# #         for row in reader:
# #             # print(row)
# #             # test.writerow(row.replace('\t', ','))
# #             test.writerow(row)

# t = pd.read_csv("../fr.openfoodfacts.org.products.csv", encoding="utf-16", sep="\t", nrows=4)

# print(t)

# def update_products(self):
#         """
#         Fills Products table with specified
#         """
#         today = datetime.today()
#         products_dict = csv_to_dict(self.file_name, self.headers)

#         for product in products_dict:
#             product_from_db = Products.get(url=product["url"])

#             query = Products.update(
#                 code=product["code"],
#                 url=product["url"],  # unique
#                 name=product["product_name"],
#                 nutri_grade=product["nutrition_grade_fr"],
#                 cat=Categories.get(
#                     Categories.name == product["main_category_fr"]
#                 ).id,
#                 energy=product["energy_100g"],
#                 fat=product["fat_100g"],
#                 carbs=product["carbohydrates_100g"],
#                 sugars=product["sugars_100g"],
#                 fibers=product["fiber_100g"],
#                 proteins=product["proteins_100g"],
#                 salt=product["salt_100g"],
#                 last_modified_t=product["last_modified_t"],
#             ).where(datetime.fromtimestamp(product["last_modified_t"]) > datetime.fromtimestamp(product_from_db.last_modified_t))

#             print("from_csv", datetime.fromtimestamp(product["last_modified_t"]), "from_db", datetime.fromtimestamp(product_from_db.last_modified_t))

#             query.execute()
