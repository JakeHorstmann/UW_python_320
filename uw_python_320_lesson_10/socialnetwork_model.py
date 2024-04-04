"""Social network app schema"""
from peewee import SqliteDatabase, Model, CharField, ForeignKeyField
# pylint: disable=R0903
# Connect to SQLite and ensure foreign_keys are enforced
database = SqliteDatabase("socialnetwork.db", pragmas={"foreign_keys": 1})
database.connect()

# This base class will automatically bind our models to the sqlite database we're creating
class BaseModel(Model):
    """Base model for database"""
    class Meta:
        """Default options for database"""
        database = database


class Users(BaseModel):
    """User model for database"""
    user_id = CharField(primary_key=True, max_length=30)
    user_name = CharField(max_length=30)
    user_last_name = CharField(max_length=100)
    user_email = CharField()


class Status(BaseModel):
    """Status model for database"""
    status_id = CharField(primary_key=True, max_length=30)
    user_id = ForeignKeyField(Users, backref='status', on_delete='CASCADE')
    status_text = CharField()


class Pictures(BaseModel):
    """Picture model for database"""
    picture_id = CharField(primary_key=True, max_length=30)
    user_id = ForeignKeyField(Users, backref="picture", on_delete="CASCADE")
    tags = CharField(max_length=100)

# Creates the table
database.create_tables([Users, Status, Pictures])

database.close()
