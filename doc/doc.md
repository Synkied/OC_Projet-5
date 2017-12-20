## DataBase
Categories:
Petit déjeuners,
Biscuits,
Soupes,
Jus de fruits,
Chips et frites,

## HOW TO

1. DL CSV file
2. Clean CSV file
3. Create DB credentials
4. Build DB from SQL file
5. Feed DB with db_feeding.py file
6. Use the program
7. Enjoy

## Python Program

build a script to create db and add tables automaticaly

create db model from database
python -m pwiz -e mysql openfoodfacts_oc -u quentin -P > db_models.py

What to do if the chosen product is the "best" available?

Random product chosing, to avoid having always the same "best" product (or only one product will always be the chosen substitute)

The program should be able to retrieve data from a csv (and the api?).

1. Clean the CSV file with specified headers: [code, url, product_name, brands, stores, traces_fr, nutrition_grade_fr, main_category_fr, energy_100g, fat_100g, saturated-fat_100g, carbohydrates_100g, sugars_100g, fiber_100g, proteins_100g, salt_100g, countries_fr]
2. Read the resulting CSV file
3. Put each category name in the "categories" database
4. Put stores and brands in their corresponding table
4. Put each product in the "products" database with links to brands stores and categories
5. todo

## User interactions
The user enters a product name, and gets a healthier replacement displayed.
He can fav it (maybe see another replacement?).
