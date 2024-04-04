'''
main driver for a simple social network project
'''

import verify_input
import users
import user_status
from socialnetwork_model import get_ds
# pylint: disable=C0103
USER_TABLE = "UserModel"
STATUS_TABLE = "StatusModel"

def init_database():
    '''
    Creates and returns a new instance of a database
    '''
    db = get_ds()
    # make sure user_id column is unique
    if db[USER_TABLE].columns == ["id"]:
        db[USER_TABLE].insert(id = -1,
                              user_id = "dummy",
                              user_email = "dummy",
                              user_name = "dummy",
                              user_last_name = "dummy")
        db[USER_TABLE].delete(id = -1)
    db[USER_TABLE].create_index(["user_id"], unique = True)
    # make sure status_id column is unique
    if db[STATUS_TABLE].columns == ["id"]:
        db[STATUS_TABLE].insert(id = -1,
                                status_id = "dummy",
                                user_id = "dummy",
                                status_text = "dummy")
        db[STATUS_TABLE].delete(id = -1)
    db[STATUS_TABLE].create_index(["status_id"], unique = True)
    return db


def load_users(filename, db):
    '''
    Opens a CSV file with user data and
    adds it to an existing instance of
    UserCollection

    Requirements:
    - If a user_id already exists, it
    will ignore it and continue to the
    next.
    - Returns False if there are any errors
    (such as empty fields in the source CSV file)
    - Otherwise, it returns True.
    '''
    # verify that the file is a CSV
    if verify_input.verify_csv_file(filename)[0]:
        load_users_to_db = users.load_users(db)
        return load_users_to_db(filename)
    # get error message from verification
    # pylint: disable=W0612
    error_msg = verify_input.verify_csv_file(filename)[1]
    return False

def load_status_updates(filename, db):
    '''
    Opens a CSV file with status data and adds it to an existing
    instance of UserStatusCollection

    Requirements:
    - If a status_id already exists, it will ignore it and continue to
      the next.
    - Returns False if there are any errors(such as empty fields in the
      source CSV file)
    - Otherwise, it returns True.
    '''
    # verify that the file is a CSV
    if verify_input.verify_csv_file(filename)[0]:
        # load statuses into db
        load_status_updates_to_db = user_status.load_status_updates(db)
        load_status_updates_to_db(filename)
        # delete any statuses without a user
        user_status.delete_status_without_user(db)
        return True
    # get error message from verification
    # pylint: disable=W0612
    error_msg = verify_input.verify_csv_file(filename)[1]
    return False

def add_user(user_id, email, user_name, user_last_name, db):
    '''
    Creates a new instance of User and stores it in user_collection
    (which is an instance of UserCollection)

    Requirements:
    - user_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
      user_collection.add_user() returns False).
    - Otherwise, it returns True.
    '''
    # verify the user_id is valid
    if not verify_input.verify_user_id(user_id)[0]:
        return False
    # verify the email is valid
    if not verify_input.verify_email(email)[0]:
        return False
    # verify the user_name is valid format
    if not verify_input.verify_user_name(user_name)[0]:
        return False
    # verify the user_last_name is valid format
    if not verify_input.verify_user_last_name(user_last_name)[0]:
        return False
    # check for duplicate
    if search_user(user_id, db):
        return False
    # add user to collection if everything is verified
    add_user_to_db = users.add_user(db)
    return add_user_to_db(user_id = user_id,
                          user_email = email,
                           user_name = user_name,
                            user_last_name = user_last_name)


def update_user(user_id, email, user_name, user_last_name, db):
    '''
    Updates the values of an existing user

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    # verify the user_id is valid
    if not verify_input.verify_user_id(user_id)[0]:
        return False
    # verify the email is valid
    if not verify_input.verify_email(email)[0]:
        return False
    # verify the user_name is valid format
    if not verify_input.verify_user_name(user_name)[0]:
        return False
    # verify the user_last_name is valid format
    if not verify_input.verify_user_last_name(user_last_name)[0]:
        return False
    # check if user exists
    user_to_modify = search_user(user_id, db)
    if not user_to_modify:
        return False
    update_user_in_db = users.update_user(db)
    return update_user_in_db(user_id = user_id,
                              user_email = email,
                                user_name = user_name,
                                  user_last_name = user_last_name)


def delete_user(user_id, db):
    '''
    Deletes a user from user_collection.

    Requirements:
    - Returns False if there are any errors (such as user_id not found)
    - Otherwise, it returns True.
    '''
    # verify the user_id is valid
    if not verify_input.verify_user_id(user_id)[0]:
        return False
    # check if they exist
    if not search_user(user_id, db):
        return False
    # delete user if verified
    delete_user_from_db = users.delete_user(db)
    delete_user_status_from_db = user_status.delete_status(db)
    if delete_user_from_db(user_id = user_id) and delete_user_status_from_db(user_id = user_id):
        return True
    return False


def search_user(user_id, db):
    '''
    Searches for a user in user collection(which is an instance of
    UserCollection).

    Requirements:
    - If the user is found, returns the corresponding User instance.
    - Otherwise, it returns None.
    '''
    # verify the user_id is valid
    if not verify_input.verify_user_id(user_id)[0]:
        return False
    # search for user and return it
    search_user_in_db = users.search_user(db)
    return search_user_in_db(user_id = user_id)


def add_status(user_id, status_id, status_text, db):
    '''
    Creates a new instance of UserStatus and stores it in
    user_collection(which is an instance of UserStatusCollection)

    Requirements:
    - status_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
      user_collection.add_status() returns False).
    - Otherwise, it returns True.
    '''
    # verify the user_id is valid
    if not verify_input.verify_user_id(user_id)[0]:
        return False
    # verify the status_id is valid
    if not verify_input.verify_status_id(status_id)[0]:
        return False
    # verify the status_text is valid
    if not verify_input.verify_status_text(status_text)[0]:
        return False
    # make sure user ID exists
    if not search_user(user_id, db):
        return False
    # add status to collection if everything is verified
    add_status_to_db = user_status.add_status(db)
    return add_status_to_db(status_id = status_id,
                            user_id = user_id,
                            status_text = status_text)


def update_status(status_id, user_id, status_text, db):
    '''
    Updates the values of an existing status_id

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    # verify the user_id is valid
    if not verify_input.verify_user_id(user_id)[0]:
        return False
    # verify the status_id is valid
    if not verify_input.verify_status_id(status_id)[0]:
        return False
    # verify the status_text is valid
    if not verify_input.verify_status_text(status_text)[0]:
        return False
    # make sure user ID exists
    if not search_user(user_id, db):
        return False
    # modify the collection data if everything is verified
    update_status_in_db = user_status.update_status(db)
    return update_status_in_db(status_id = status_id,
                                user_id = user_id,
                                status_text = status_text)


def delete_status(status_id, db):
    '''
    Deletes a status_id from user_collection.

    Requirements:
    - Returns False if there are any errors (such as status_id not found)
    - Otherwise, it returns True.
    '''
    # verify the status_id is valid
    if not verify_input.verify_status_id(status_id)[0]:
        return False
    # delete status if verified
    delete_status_in_db = user_status.delete_status(db)
    return delete_status_in_db(status_id = status_id)


def search_status(status_id, db):
    '''
    Searches for a status in status_collection

    Requirements:
    - If the status is found, returns the corresponding
    UserStatus instance.
    - Otherwise, it returns None.
    '''
    # verify the status_id is valid
    if not verify_input.verify_status_id(status_id)[0]:
        return False
    # search for status if verified
    search_status_in_db = user_status.search_status(db)
    return search_status_in_db(status_id = status_id)
