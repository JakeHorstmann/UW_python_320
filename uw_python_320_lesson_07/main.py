'''
main driver for a simple social network project
'''

import csv

import pandas as pd
from multiprocessing import Process, cpu_count

from pymongo import MongoClient
import verify_input
from users import UserCollection
from user_status import UserStatusCollection

DATABASE = "database.db"

def init_user_collection(host, port, database_name, table_name = "UserAccounts"):
    '''
    Creates and returns a new instance of UserCollection
    '''
    # pylint: disable=C0103
    user_collection = UserCollection(host, port, database_name, table_name)
    return user_collection


def init_status_collection(host, port, database_name, table_name = "StatusUpdates"):
    '''
    Creates and returns a new instance of UserStatusCollection
    '''
    # pylint: disable=C0103
    status_collection = UserStatusCollection(host, port, database_name, table_name)
    return status_collection


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
                row_data ={"_id": row["USER_ID"],
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

def load_users_multiprocess(filename, host = "localhost", port = 27017, database_name = "database"):
    '''
    Loads the user file with multiprocessing
    '''
    # verify that the file is a CSV
    if verify_input.verify_csv_file(filename)[0]:
        # optimize batch size
        file_length = len(pd.read_csv(filename))
        processors = cpu_count()
        optimal_batch_size = int(file_length / processors) + 1
        chunks = pd.read_csv(filename, chunksize = optimal_batch_size, iterator = True)
        # begin multiprocessing
        processes = []
        for _ in range(processors):
            data = next(chunks)
            process = Process(target = load_users_multiprocess_worker, args = (data, host, port, database_name,))
            process.start()
            processes.append(process)
        # wait for all processes to finish
        for process in processes:
            process.join()
        return True
    # get error message if CSV was not valid
    error_msg = verify_input.verify_csv_file(filename)[1]
    return False

def load_users_multiprocess_worker(data, host, port, database_name):
    """
    Helper function for multiprocessing to load users
    """
    user_collection = init_user_collection(host, port, database_name)
    column_map = {"USER_ID": "_id",
                    "EMAIL": "user_email",
                    "NAME": "user_name",
                    "LAST_NAME": "user_last_name"}
    data.rename(columns = column_map, inplace = True)
    # adds users in MongoDB format
    user_collection.batch_load_users(data.to_dict("records"))

def load_status_updates(filename, status_collection, user_collection, batch_size = 32):
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
            user_ids = set()
            # read in each row in the csv
            for row in dict_reader:
                if batch_row == batch_size:
                    # batch load statuses to database
                    matched_users = user_collection.count_users_with_id(list(user_ids))
                    if matched_users != len(user_ids):
                        print("STATUSES DID NOT HAVE CORRESPONDING USER ID")
                    else:
                        status_collection.batch_load_statuses(batch_data)
                    batch_data = []
                    user_ids = set()
                    batch_row = 0
                # grab status data on row if the user exists
                user_id = row["USER_ID"]
                row_data = {"_id": row["STATUS_ID"],
                    "user_id": user_id,
                    "status_text": row["STATUS_TEXT"]}
                batch_data.append(row_data)
                user_ids.add(user_id)
                batch_row += 1

            # load the rest of the batch
            status_collection.batch_load_statuses(batch_data)
        # if everything goes through this file was added successfully
        return True
    # get error message from verification
    # pylint: disable=W0612
    error_msg = verify_input.verify_csv_file(filename)[1]
    return False

def load_status_updates_multiprocess(filename, host = "localhost", port = 27017, database_name = "database"):
    # verify that the file is a CSV
    if verify_input.verify_csv_file(filename)[0]:
        # optimize batch size
        file_length = len(pd.read_csv(filename))
        processors = cpu_count()
        optimal_batch_size = int(file_length / processors) + 1
        chunks = pd.read_csv(filename, chunksize = optimal_batch_size, iterator = True)
        # begin multiprocessing
        processes = []
        try:
            for _ in range(processors):
                data = next(chunks)
                process = Process(target = load_user_status_multiprocess_worker, args = (data, host, port, database_name,))
                process.start()
                processes.append(process)
        # skip if there is no more chunks left
        except StopIteration:
            pass
        # wait for all processes to finish
        for process in processes:
            process.join()
        return True
    # get error message if CSV was not valid
    error_msg = verify_input.verify_csv_file(filename)[1]
    return False

def load_user_status_multiprocess_worker(data, host, port, database_name):
    """
    Helper function for multiprocessing to load users
    """
    user_collection = init_user_collection(host, port, database_name)
    status_collection = init_status_collection(host, port, database_name)
    column_map = {"STATUS_ID": "_id",
                    "USER_ID": "user_id",
                    "STATUS_TEXT": "status_text"}
    data.rename(columns = column_map, inplace = True)
    # check that the user_id exists for each status
    ids = data["user_id"].unique().tolist()
    matched_users = user_collection.count_users_with_id(ids)
    if matched_users != len(ids):
        print("STATUSES DID NOT HAVE CORRESPONDING USER ID")
        return False
    # adds users in MongoDB format
    return status_collection.batch_load_statuses(data.to_dict("records"))

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


def delete_user(user_id, user_collection, status_collection):
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
    if user_collection.delete_user(user_id):
        _, all_user_statuses = search_all_status_updates(user_id, status_collection)
        for status in all_user_statuses:
            delete_status(status["_id"], status_collection)
        return True
    return False


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


def add_status(user_id, status_id, status_text, status_collection, user_collection):
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
    if user_collection.search_user(user_id):
        return status_collection.add_status(status_id, user_id, status_text)
    return False


def update_status(status_id, user_id, status_text, status_collection, user_collection):
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
    if user_collection.search_user(user_id):
        return status_collection.modify_status(status_id, user_id, status_text)
    return False


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

def nuke_databases(database_name, table_names, host = "localhost", port = 27017):
    client = MongoClient(host = host, port = port)
    for table_name in table_names:
        client[database_name][table_name].drop()
    return True
