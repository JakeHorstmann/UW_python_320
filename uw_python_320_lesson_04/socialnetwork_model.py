"""
File for establishing the database schema
"""
# pylint: disable=R0903, E0401
from peewee import Model, SqliteDatabase, CharField, ForeignKeyField

db = SqliteDatabase("database.db", pragmas={"foreign_keys": 1})
db.connect()

class RootModel(Model):
    """
    Model that all models inherit from
    """
    class Meta:
        """
        Establishes a database that all models use
        """
        database = db

class UserModel(RootModel):
    """
    Database model for users
    """
    user_id = CharField(primary_key = True, max_length = 30)
    user_name = CharField(max_length = 30)
    user_last_name = CharField(max_length = 100)
    user_email = CharField(max_length = 50)

class StatusModel(RootModel):
    """
    Database model for statuses
    """
    status_id = CharField(primary_key = True, max_length = 30)
    user_id = ForeignKeyField(UserModel, backref = "statuses", on_delete="CASCADE")
    status_text = CharField(max_length = 250)


db.create_tables([UserModel, StatusModel])
db.close()
