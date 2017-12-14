import pandas as pd


def test_csv(file, headers):

    # reads the specified file.
    # sep: csv file's separator
    # low_memory: avoiding unnecessary warning msgs
    csv_file = pd.read_csv(
        fname, sep=";", encoding="utf-8", low_memory=False
    )

    # defines a dataframe, from the passed headers
    df = csv_file[headers]


    new_df = list(df["stores"].unique())
    print(new_df)
    # t = [i.split(",") for i in new_df if type(i) is not float]
    # b = set()
    # for i in t:
    #     for j in i:
    #         b.add(j.strip().capitalize())
    # print(b)


fname = "db_file.csv"

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


test_csv(fname, headers_list)
