# import pandas as pd


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


# def download_csv_openfoodfacts():
#     csv_url = "https://world.openfoodfacts.org/data/en.openfoodfacts.org.products.csv"

#     data = pd.read_csv(csv_url, encoding="utf-16", sep="\t")

#     print("Download in progress...")

#     data.to_csv("test.csv", index=False, encoding="utf-16", sep=";")


# download_csv_openfoodfacts()