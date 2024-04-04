'''
Classes for user information for the social network project
'''
# pylint: disable=R0903, E0401, C0103
from peewee import IntegrityError

USER_TABLE = "UserModel"

def add_user(db):
    """
    Adds a user to the database
    """
    def insert(**kwargs):
        try:
            with db.transaction():
                db[USER_TABLE].insert(**kwargs)
            return True
        except IntegrityError:
            print("Duplicate ID tried to be added")
            return False
    return insert

def update_user(db):
    """
    Updates a user in the database
    """
    def update(**kwargs):
        with db.transaction():
            if search_user(db)(user_id = kwargs["user_id"]):
                db[USER_TABLE].update(**kwargs, columns = ["user_id"])
                return True
            return False
    return update

def delete_user(db):
    """
    Deletes a user in the database
    """
    def delete(**kwargs):
        with db.transaction():
            if search_user(db)(user_id = kwargs["user_id"]):
                db[USER_TABLE].delete(**kwargs)
                return True
            return False
    return delete

def search_user(db):
    """
    Searches for a user in the database
    """
    def search(**kwargs):
        with db.transaction():
            return db[USER_TABLE].find_one(**kwargs)
    return search

def load_users(db):
    """
    Loads users into the database
    """
    def load(filename):
        try:
            with db.transaction():
                db[USER_TABLE].thaw(format = "csv", filename = filename, strict = True)
            return True
        except IntegrityError:
            print("User IDs were not unique")
            return False
    return load
