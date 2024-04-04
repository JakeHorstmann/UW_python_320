'''
main driver for a simple social network project
'''

import csv

from peewee import SqliteDatabase
import verify_input
import users
import user_status

DATABASE = "database.db"

def init_user_collection():
    '''
    Creates and returns a new instance of UserCollection
    '''
    # pylint: disable=C0103
    db = SqliteDatabase(DATABASE)
    user_collection = users.UserCollection(db)
    return user_collection


def init_status_collection():
    '''
    Creates and returns a new instance of UserStatusCollection
    '''
    # pylint: disable=C0103
    db = SqliteDatabase(DATABASE)
    user_status_collection = user_status.UserStatusCollection(db)
    return user_status_collection


def load_users(filename, user_collection, batch_size = 32):
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
        with open(filename, "r") as csv_file:
            dict_reader = csv.DictReader(csv_file, delimiter=",")
            # check that the CSV has the required columns
            if sorted(dict_reader.fieldnames) != sorted(["USER_ID", "EMAIL", "NAME", "LASTNAME"]):
                return False
            batch_row = 0
            batch_data = []
            for row in dict_reader:
                if batch_row == batch_size:
                    # batch load users to database
                    user_collection.batch_load_users(batch_data)
                    batch_data = []
                    batch_row = 0
                # grab user data on row
                row_data ={"user_id": row["USER_ID"],
                           "user_email": row["EMAIL"],
                           "user_name": row["NAME"],
                           "user_last_name": row["LASTNAME"]}
                batch_data.append(row_data)
                batch_row += 1
            # load the rest of the batch
            user_collection.batch_load_users(batch_data)
        # if everything goes through this file was added successfully
        return True
    # get error message from verification
    # pylint: disable=W0612
    error_msg = verify_input.verify_csv_file(filename)[1]
    return False

def load_status_updates(filename, status_collection, batch_size = 32):
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
        with open(filename, "r") as csv_file:
            dict_reader = csv.DictReader(csv_file, delimiter=",")
            # check that the CSV has the required columns
            if sorted(dict_reader.fieldnames) != sorted(["STATUS_ID", "USER_ID", "STATUS_TEXT"]):
                return False
            batch_row = 0
            batch_data = []
            # read in each row in the csv
            for row in dict_reader:
                if batch_row == batch_size:
                    # batch load statuses to database
                    status_collection.batch_load_statuses(batch_data)
                    batch_data = []
                    batch_row = 0
                # grab status data on row
                row_data = {"status_id": row["STATUS_ID"],
                       "user_id": row["USER_ID"],
                       "status_text": row["STATUS_TEXT"]}
                batch_data.append(row_data)
                batch_row += 1
            # load the rest of the batch
            status_collection.batch_load_statuses(batch_data)
        # if everything goes through this file was added successfully
        return True
    # get error message from verification
    # pylint: disable=W0612
    error_msg = verify_input.verify_csv_file(filename)[1]
    return False

def add_user(user_id, email, user_name, user_last_name, user_collection):
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
    # add user to collection if everything is verified
    return user_collection.add_user(user_id, email, user_name, user_last_name)


def update_user(user_id, email, user_name, user_last_name, user_collection):
    '''
    Updates the values of an existing user

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    # verify the user_id is valid
    if not verify_input.verify_user_id(user_id)[0]:
        print("used id")
        return False
    # verify the email is valid
    if not verify_input.verify_email(email)[0]:
        print("email")
        return False
    # verify the user_name is valid format
    if not verify_input.verify_user_name(user_name)[0]:
        print("name")
        return False
    # verify the user_last_name is valid format
    if not verify_input.verify_user_last_name(user_last_name)[0]:
        print("name")
        return False
    # modify the collection data if everything is verified
    return user_collection.modify_user(user_id, email, user_name, user_last_name)


def delete_user(user_id, user_collection):
    '''
    Deletes a user from user_collection.

    Requirements:
    - Returns False if there are any errors (such as user_id not found)
    - Otherwise, it returns True.
    '''
    # verify the user_id is valid
    if not verify_input.verify_user_id(user_id)[0]:
        return False
    # delete user if verified
    return user_collection.delete_user(user_id)


def search_user(user_id, user_collection):
    '''
    Searches for a user in user_collection(which is an instance of
    UserCollection).

    Requirements:
    - If the user is found, returns the corresponding User instance.
    - Otherwise, it returns None.
    '''
    # verify the user_id is valid
    if not verify_input.verify_user_id(user_id)[0]:
        return False
    # search for user and return it
    return user_collection.search_user(user_id)


def add_status(user_id, status_id, status_text, status_collection):
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
    # add status to collection if everything is verified
    return status_collection.add_status(status_id, user_id, status_text)


def update_status(status_id, user_id, status_text, status_collection):
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
    # modify the collection data if everything is verified
    return status_collection.modify_status(status_id, user_id, status_text)


def delete_status(status_id, status_collection):
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
    return status_collection.delete_status(status_id)


def search_status(status_id, status_collection):
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
    return status_collection.search_status(status_id)

def search_all_status_updates(user_id, status_collection):
    """
    Finds all status updates for a user
    """
    # search the status collection for all updates
    return status_collection.search_all_status_updates(user_id)

def filter_status_by_string(phrase, status_collection):
    """
    Returns all statuses that contain a phrase
    """
    # search the status collection for statuses with the phrase
    return status_collection.filter_status_by_string(phrase)
