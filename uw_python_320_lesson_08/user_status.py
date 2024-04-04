'''
classes to manage the user status messages
'''
# pylint: disable=R0903, E0401, C0103
from peewee import IntegrityError

STATUS_TABLE = "StatusModel"
USER_TABLE = "UserModel"

def add_status(db):
    """
    Adds a status into the database
    """
    def insert(**kwargs):
        try:
            with db.transaction():
                db[STATUS_TABLE].insert(**kwargs)
            return True
        except IntegrityError:
            print("Duplicate status tried to be added")
            return False
    return insert

def update_status(db):
    """
    Updates a status in the database
    """
    def update(**kwargs):
        with db.transaction():
            if search_status(db)(status_id = kwargs["status_id"]):
                db[STATUS_TABLE].update(**kwargs, columns = ["status_id"])
                return True
            return False
    return update

def delete_status(db):
    """
    Deletes a status in the database
    """
    def delete(**kwargs):
        with db.transaction():
            if search_status(db)(status_id = kwargs["status_id"]):
                db[STATUS_TABLE].delete(**kwargs)
                return True
            return False
    return delete

def search_status(db):
    """
    Searches for a status in the database
    """
    def search(**kwargs):
        with db.transaction():
            return db[STATUS_TABLE].find_one(**kwargs)
    return search

def load_status_updates(db):
    """
    Load statuses into the database
    """
    def load(filename):
        try:
            with db.transaction():
                db[STATUS_TABLE].thaw(format = "csv", filename = filename, strict = True)
            return True
        except IntegrityError:
            print("Status IDs were not unique")
            return False
    return load

def delete_status_without_user(db):
    """
    Delete statuses without a user in the database
    """
    # get all statuses that do not have a user id
    user_table = db[USER_TABLE]
    status_table = db[STATUS_TABLE]
    user_query = user_table.find()
    status_query = status_table.find()

    status_user_id_set = set()
    for status in status_query:
        status_user_id_set.add(status["user_id"])
    user_id_set = set()
    for user in user_query:
        user_id_set.add(user["user_id"])

    difference = list(status_user_id_set.difference(user_id_set))
    with db.transaction():
        for diff in difference:
            status_table.delete(user_id = diff)
