# OpenFoodFacts DB

The aim of this project is to query the OpenFoodFacts (OFF) API in order to populate a local SQL database (MariaDB in my case). We should then provide a CLI interface to search for products and substitutes in that database. It should also be possible to save the found substitutes.

This project's development has to be documentation-driven, so the different classes will be detailed in this README.
Create the database

## To create the database, use the following command:

$ mysql -h [db_host] -u root -p[root_password] < db_build.sql

CAUTION: If the my_openfoodfacts database already exists, db_build.sql will delete it.

To populate the database, use the populate_database.py script:

$ ./populate_database.py
WARNING: Refreshing categories, this may take some time...Done.
WARNING: Refreshing products, this may take some time...Done
Updating categories in the DB...Done.
Updating products in the database...Done

