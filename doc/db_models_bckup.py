from peewee import *

# todo: check order by on nutrigrade

class ConfigRDR():
    """
    open cfg file and get the credentials
    """
    pass


database = MySQLDatabase(
    'openfoodfacts_oc',
    **{'user': "quentin", 'password': "openffoc"}
)


class BaseModel(Model):
    class Meta:
        database = database


class Brands(BaseModel):
    name = CharField(null=True, unique=True)

    class Meta:
        db_table = 'brands'


class Categories(BaseModel):
    name = CharField()
    url = CharField(null=True)

    class Meta:
        db_table = 'categories'


class Stores(BaseModel):
    name = CharField(null=True, unique=True)

    class Meta:
        db_table = 'stores'


class Products(BaseModel):
    brand = ForeignKeyField(
        db_column='brand_id', rel_model=Brands, to_field='id', null=True
    )
    carbs = FloatField(null=True)
    cat = ForeignKeyField(
        db_column='cat_id', rel_model=Categories, to_field='id'
    )
    energy = IntegerField(null=True)
    fat = FloatField(null=True)
    fibers = FloatField(null=True)
    name = CharField(null=True)
    nutri_grade = CharField(null=True)
    proteins = FloatField(null=True)
    salt = FloatField(null=True)
    store = ForeignKeyField(
        db_column='store_id', rel_model=Stores, to_field='id', null=True
    )
    sugars = FloatField(null=True)
    traces = CharField(null=True)

    class Meta:
        db_table = 'products'
        indexes = (
            (('cat', 'brand', 'store'), True),
        )


class Favorites(BaseModel):
    id = IntegerField(unique=True)
    product = ForeignKeyField(
        db_column='product_id', rel_model=Products, to_field='id'
    )
    substitute = ForeignKeyField(
        db_column='substitute_id', rel_model=Products,
        related_name='products_substitute_set', to_field='id'
    )

    class Meta:
        db_table = 'favorites'
        indexes = (
            (('id', 'product', 'substitute'), True),
        )
        primary_key = CompositeKey('id', 'product', 'substitute')

# database.drop_tables([Brands, Categories, Stores, Products, Favorites])
# database.create_tables([Brands, Categories, Stores, Products, Favorites])
