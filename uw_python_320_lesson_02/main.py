'''
main driver for a simple social network project
'''

import csv

import users
import user_status



def init_user_collection():
    '''
    Creates and returns a new instance of UserCollection
    '''
    user_collection = users.UserCollection()
    return user_collection


def init_status_collection():
    '''
    Creates and returns a new instance of UserStatusCollection
    '''
    user_status_collection = user_status.UserStatusCollection()
    return user_status_collection


def load_users(filename, user_collection):
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
    # try to open file it exists. if not, return false
    try:
        with open(filename, "r") as csv_file:
            dict_reader = csv.DictReader(csv_file, delimiter=",")
            # check that the CSV has the required columns
            if sorted(dict_reader.fieldnames) != sorted(["USER_ID", "EMAIL", "NAME", "LASTNAME"]):
                return False
            # read in each row in the csv
            for row in dict_reader:
                # check that the CSV has the required columns
                user_id = row["USER_ID"]
                email = row["EMAIL"]
                name = row["NAME"]
                last_name = row["LASTNAME"]
                # if the user is not already in the database, add it. skip if it is
                if not user_id in user_collection.database:
                    user_collection.add_user(user_id, email, name, last_name)
        # if everything goes through this file was added successfully
        return True
    # return False if the file is not found
    except FileNotFoundError:
        return False


def save_users(filename, user_collection):
    '''
    Saves all users in user_collection into
    a CSV file

    Requirements:
    - If there is an existing file, it will
    overwrite it.
    - Returns False if there are any errors
    (such as an invalid filename).
    - Otherwise, it returns True.
    '''
    # get extension for file
    extension = filename[-4:].lower()
    # check if the file extension is csv or txt so it can write correctly
    if extension in (".csv", ".txt"):
        with open(filename, "w", newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=",")
            # write initial column names to CSV
            fields = ["USER_ID", "EMAIL", "NAME", "LASTNAME"]
            writer.writerow(fields)
            # loop through each user to add it to the CSV
            for user in user_collection.database.values():
                # collect all data for CSV from user
                user_id = user.user_id
                user_email = user.email
                user_name = user.user_name
                user_last_name = user.user_last_name
                # write user data to CSV
                writer.writerow([user_id, user_email, user_name, user_last_name])
        # if everything goes through this file was written successfully
            return True
    # return False if extension is bad
    return False


def load_status_updates(filename, status_collection):
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
        # try to open file it exists. if not, return false
    try:
        with open(filename, "r") as csv_file:
            dict_reader = csv.DictReader(csv_file, delimiter=",")
            # check that the CSV has the required columns
            if sorted(dict_reader.fieldnames) != sorted(["STATUS_ID", "USER_ID", "STATUS_TEXT"]):
                return False
            # read in each row in the csv
            for row in dict_reader:
                status_id = row["STATUS_ID"]
                user_id = row["USER_ID"]
                status_text = row["STATUS_TEXT"]
                # if the status is not already in the database, add it. skip if it is
                if not status_id in status_collection.database:
                    status_collection.add_status(status_id, user_id, status_text)
        # if everything goes through this file was added successfully
        return True
    # return False if the file is not found
    except FileNotFoundError:
        return False


def save_status_updates(filename, status_collection):
    '''
    Saves all statuses in status_collection into a CSV file

    Requirements:
    - If there is an existing file, it will overwrite it.
    - Returns False if there are any errors(such an invalid filename).
    - Otherwise, it returns True.
    '''
    # get extension for file
    extension = filename[-4:].lower()
    # check if the file extension is csv or txt so it can write correctly
    if extension in (".csv", ".txt"):
        with open(filename, "w", newline="") as csv_file:
            writer = csv.writer(csv_file, delimiter=",")
            # write initial column names to CSV
            fields = ["STATUS_ID", "USER_ID", "STATUS_TEXT"]
            writer.writerow(fields)
            # loop through each user to add it to the CSV
            for status in status_collection.database.values():
                # collect all data for CSV from user
                status_id = status.status_id
                status_user_id = status.user_id
                status_text = status.status_text
                # write user data to CSV
                writer.writerow([status_id, status_user_id, status_text])
        # if everything goes through this file was written successfully
            return True
    # return False if extension is bad
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
    # make sure none of the values are blank
    if user_id and email and user_name and user_last_name:
        # add user to collection. return True or False based on what it returns
        return user_collection.add_user(user_id, email, user_name, user_last_name)
    # return False if data is blank
    return False


def update_user(user_id, email, user_name, user_last_name, user_collection):
    '''
    Updates the values of an existing user

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    # make sure none of the values are blank
    if user_id and email and user_name and user_last_name:
        # modify the collection data. return True or False based on what it returns
        return user_collection.modify_user(user_id, email, user_name, user_last_name)
    # return False if there is blank data
    return False


def delete_user(user_id, user_collection):
    '''
    Deletes a user from user_collection.

    Requirements:
    - Returns False if there are any errors (such as user_id not found)
    - Otherwise, it returns True.
    '''
    # delete user. return True or False based on what it returns
    if user_id:
        return user_collection.delete_user(user_id)
    return False


def search_user(user_id, user_collection):
    '''
    Searches for a user in user_collection(which is an instance of
    UserCollection).

    Requirements:
    - If the user is found, returns the corresponding User instance.
    - Otherwise, it returns None.
    '''
    # search for user. return the user when found
    # returns a None user if there is no user
    if user_id:
        return user_collection.search_user(user_id)
    return users.Users(None, None, None, None)


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
    # make sure none of the values are blank
    if status_id and user_id and status_text:
        # add status to collection. return True or False based on what it returns
        return status_collection.add_status(status_id, user_id, status_text)
    # return False if data is blank
    return False


def update_status(status_id, user_id, status_text, status_collection):
    '''
    Updates the values of an existing status_id

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    # make sure none of the values are blank
    if status_id and user_id and status_text:
        # modify the collection data. return True or False based on what it returns
        return status_collection.modify_status(status_id, user_id, status_text)
    # return False if there is blank data
    return False


def delete_status(status_id, status_collection):
    '''
    Deletes a status_id from user_collection.

    Requirements:
    - Returns False if there are any errors (such as status_id not found)
    - Otherwise, it returns True.
    '''
    # delete status. return True or False based on what it returns
    return status_collection.delete_status(status_id)


def search_status(status_id, status_collection):
    '''
    Searches for a status in status_collection

    Requirements:
    - If the status is found, returns the corresponding
    UserStatus instance.
    - Otherwise, it returns None.
    '''
    # search for status. return the status when found
    return status_collection.search_status(status_id)
