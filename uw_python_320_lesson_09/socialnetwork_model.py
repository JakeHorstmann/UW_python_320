from peewee import SqliteDatabase, Model, CharField, ForeignKeyField

# Connect to SQLite and ensure foreign_keys are enforced
database = SqliteDatabase("socialnetwork.db", pragmas={"foreign_keys": 1})
database.connect()

# This base class will automatically bind our models to the sqlite database we're creating
class BaseModel(Model):
    class Meta:
        database = database


class Users(BaseModel):
    user_id = CharField(primary_key=True, max_length=30)
    user_name = CharField(max_length=30)
    user_last_name = CharField(max_length=100)
    user_email = CharField()


class Status(BaseModel):
    status_id = CharField(primary_key=True, max_length=30)
    user_id = ForeignKeyField(Users, backref='status', on_delete='CASCADE')
    status_text = CharField()


class Pictures(BaseModel):
    picture_id = CharField(primary_key=True, max_length=30)
    user_id = ForeignKeyField(Users, backref="picture", on_delete="CASCADE")
    tags = CharField(max_length=100)

# Creates the table
database.create_tables([Users, Status, Pictures])

database.close()
