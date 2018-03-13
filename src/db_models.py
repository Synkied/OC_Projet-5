# coding: utf8

"""
This file contains the peewee database models for the OFF OC project.
It was auto-converted from a .mysql file using pwiz.
http://docs.peewee-orm.com/en/latest/peewee/playhouse.html#pwiz

The MySQL file itself was generated from a schema made in MySQLWorkBench.
https://dev.mysql.com/doc/workbench/en/wb-forward-engineering-sql-scripts.html
"""

import configparser
import os.path

from peewee import *

from constants import *
from config_parser import *


# Create the config file if it does not exist.
# Had to put this here because this module is imported in install.py
if not os.path.exists("../" + CFG_FNAME):
    config_write("../" + CFG_FNAME)

config = configparser.ConfigParser()
config.read("../" + CFG_FNAME)


openfoodfacts_db = PostgresqlDatabase(config["Postgresql"]["db"], **{
    'user': config["Postgresql"]["user"], 'password': config["Postgresql"]["password"]
})


class BaseModel(Model):
    class Meta:
        database = openfoodfacts_db


class Brand(BaseModel):
    name = CharField(unique=True)

    class Meta:
        db_table = 'brand'


class Category(BaseModel):
    name = CharField(unique=True)

    class Meta:
        db_table = 'category'


class Store(BaseModel):
    name = CharField(unique=True)

    class Meta:
        db_table = 'store'


class Product(BaseModel):
    code = BigIntegerField()
    url = CharField(null=False, unique=True)
    name = CharField()
    nutri_grade = CharField(null=True)
    cat = ForeignKeyField(
        db_column='cat_id', rel_model=Category, to_field='id'
    )
    energy = IntegerField(null=True)
    fat = DoubleField(null=True)
    carbs = DoubleField(null=True)
    sugars = DoubleField(null=True)
    fibers = DoubleField(null=True)
    proteins = DoubleField(null=True)
    salt = DoubleField(null=True)
    last_modified_t = DateTimeField(null=False)

    class Meta:
        db_table = 'product'


class Favorite(BaseModel):
    product = ForeignKeyField(
        db_column='product_id',
        rel_model=Product,
        to_field='id'
    )
    substitute = ForeignKeyField(
        db_column='substitute_id',
        rel_model=Product,
        related_name='products_substitute_set',
        to_field='id'
    )

    class Meta:
        db_table = 'favorite'


class Productbrand(BaseModel):
    brand = ForeignKeyField(
        db_column='brand_id',
        rel_model=Brand,
        to_field='id'
    )
    product = ForeignKeyField(
        db_column='product_id',
        rel_model=Product,
        to_field='id'
    )

    class Meta:
        db_table = 'productbrand'
        indexes = (
            (('brand', 'product'), True),
        )
        primary_key = CompositeKey('brand', 'product')


class Productstore(BaseModel):
    product = ForeignKeyField(
        db_column='product_id', rel_model=Product, to_field='id'
    )
    store = ForeignKeyField(
        db_column='store_id', rel_model=Store, to_field='id'
    )

    class Meta:
        db_table = 'productstore'
        indexes = (
            (('product', 'store'), True),
        )
        primary_key = CompositeKey('product', 'store')
