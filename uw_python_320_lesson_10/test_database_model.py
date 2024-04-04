from peewee import SqliteDatabase, Model, CharField, ForeignKeyField

# Connect to SQLite and ensure foreign_keys are enforced
test_database = SqliteDatabase("test_database.db", pragmas={"foreign_keys": 1})
test_database.connect()


# This base class will automatically bind our models to the sqlite database we're creating
class BaseModel(Model):
    class Meta:
        database = test_database


class TestUsers(BaseModel):
    user_id = CharField(primary_key=True, max_length=30)
    user_name = CharField(max_length=30)
    user_last_name = CharField(max_length=100)
    user_email = CharField()


class TestStatus(BaseModel):
    status_id = CharField(primary_key=True, max_length=30)
    # user_id= CharField(max_length=30)
    user_id = ForeignKeyField(TestUsers, backref='status', on_delete='CASCADE')
    status_text = CharField()


def drop_tables():
    test_database.drop_tables([TestUsers, TestStatus])


def create_tables():
    test_database.create_tables([TestUsers, TestStatus])
    test_database.bind([TestUsers, TestStatus])


def close_connection():
    test_database.close()


# Creates the table
test_database.drop_tables([TestUsers, TestStatus])
test_database.create_tables([TestUsers, TestStatus])

test_database.close()