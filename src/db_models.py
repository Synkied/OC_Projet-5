import configparser

from peewee import *

from constants import *

config = configparser.ConfigParser()
config.read("../" + CFG_FNAME)

db_conn = MySQLDatabase(config["MySQL"]["db"], **{
    'user': config["MySQL"]["user"], 'password': config["MySQL"]["password"]
})


class BaseModel(Model):
    class Meta:
        database = db_conn


class Brands(BaseModel):
    name = CharField(unique=True)

    class Meta:
        db_table = 'brands'


class Categories(BaseModel):
    name = CharField(unique=True)

    class Meta:
        db_table = 'categories'


class Stores(BaseModel):
    name = CharField(unique=True)

    class Meta:
        db_table = 'stores'


class Products(BaseModel):
    carbs = FloatField(null=True)
    cat = ForeignKeyField(
        db_column='cat_id', rel_model=Categories, to_field='id'
    )
    code = IntegerField(unique=True)
    energy = IntegerField(null=True)
    fat = FloatField(null=True)
    fibers = FloatField(null=True)
    name = CharField()
    nutri_grade = CharField(null=True)
    proteins = FloatField(null=True)
    salt = FloatField(null=True)
    sugars = FloatField(null=True)
    url = CharField(null=True)

    class Meta:
        db_table = 'products'


class Favorites(BaseModel):
    product = ForeignKeyField(
        db_column='product_id',
        rel_model=Products,
        to_field='id'
    )
    substitute = ForeignKeyField(
        db_column='substitute_id',
        rel_model=Products,
        related_name='products_substitute_set',
        to_field='id'
    )

    class Meta:
        db_table = 'favorites'


class Productsbrands(BaseModel):
    brands = ForeignKeyField(
        db_column='Brands_id',
        rel_model=Brands,
        to_field='id'
    )
    products = ForeignKeyField(
        db_column='Products_id',
        rel_model=Products,
        to_field='id'
    )

    class Meta:
        db_table = 'productsbrands'
        indexes = (
            (('brands', 'products'), True),
        )
        primary_key = CompositeKey('brands', 'products')


class Productsstores(BaseModel):
    products = ForeignKeyField(
        db_column='Products_id', rel_model=Products, to_field='id'
    )
    stores = ForeignKeyField(
        db_column='Stores_id', rel_model=Stores, to_field='id'
    )

    class Meta:
        db_table = 'productsstores'
        indexes = (
            (('products', 'stores'), True),
        )
        primary_key = CompositeKey('products', 'stores')
