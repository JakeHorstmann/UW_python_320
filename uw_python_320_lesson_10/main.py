'''
main driver for a simple social network project
'''
from csv import DictReader
import sys
from os import path, makedirs, listdir
from sqlite3 import IntegrityError as IntegretyError2
from loguru import logger
from peewee import IntegrityError

import users
import user_status
import pictures

logger.remove()
logger.add('logs_{time:YYYY-MM-DD}.log', level="DEBUG")
logger.add(sys.stderr, level="DEBUG")


def load_users(filename, table):
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
    try:
        with open(filename, "r", encoding="utf-8") as user_file:
            csv_reader = DictReader(user_file)
            for row in csv_reader:
                try:
                    add_user1 = users.add_user(table)
                    add_user1(user_id=row['USER_ID'],
                              user_email=row['EMAIL'],
                              user_name=row['NAME'],
                              user_last_name=row['LASTNAME'])
                except (IntegrityError, IntegretyError2):
                    logger.debug(f"User {row['USER_ID']} already exists, skipping record")
                    print(f"User {row['USER_ID']} already exists, skipping record")
                    continue
        logger.info(f"Loaded users from file {filename}")
        return True
    except FileNotFoundError:
        logger.debug(f"File with name {filename} could not be accessed")
        print("The file was not found")
        return False


def add_status(status_id, user_id, status_text, table_status, table_users):
    '''
    Creates a new instance of UserStatus and stores it in
    user_collection(which is an instance of UserStatusCollection)

    Requirements:
    - status_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
      user_collection.add_status() returns False).
    - Otherwise, it returns True.
    '''
    add_status_inner = user_status.add_status(table_status)
    if not search_user(user_id, table_users):
        print("Unable to add status, user does not exist")
        return False
    return add_status_inner(status_id=status_id, user_id=user_id, status_text=status_text)


def load_status_updates(filename, table_status, table_users):
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

    try:
        with open(filename, "r", encoding="utf-8") as csv_file:
            reader = DictReader(csv_file)
            for row in reader:
                try:
                    add_status(status_id=row["STATUS_ID"],
                                user_id=row["USER_ID"],
                                status_text=row["STATUS_TEXT"],
                                table_status=table_status,
                                table_users=table_users)
                except IntegrityError:
                    print(f"Status id {row['STATUS_ID']} already exists, skipping record")
                    continue
            logger.info(f"Loaded statuses from file '{filename}'")
            return True
    except FileNotFoundError:
        logger.error(f"File with name '{filename}' could not be accessed")
        print("The file was not found")
        return False


def add_user(user_id, user_email, user_name, user_last_name, table):
    '''
    Creates a new instance of User and stores it in user_collection
    (which is an instance of UserCollection)

    Requirements:
    - user_id cannot already exist in user_collection.
    - Returns False if there are any errors (for example, if
      user_collection.add_user() returns False).
    - Otherwise, it returns True.
    '''
    add_user_inner = users.add_user(table)
    return add_user_inner(user_id=user_id, user_email=user_email,
                          user_name=user_name, user_last_name=user_last_name)


def update_user(user_id, email, user_name, user_last_name, table):
    '''
    Updates the values of an existing user

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    update_user_inner = users.modify_user(table)
    return update_user_inner(user_id=user_id,
                             user_email=email,
                             user_name=user_name,
                             user_last_name=user_last_name,
                             columns=['user_id'])


def delete_user(user_id, table_users, table_status, table_pictures):
    '''
    Deletes a user from user_collection.

    Requirements:
    - Returns False if there are any errors (such as user_id not found)
    - Otherwise, it returns True.
    '''
    remove_user = users.delete_user(table_users)
    if search_user(user_id, table_users):
        for status in table_status.find(user_id=user_id):
            delete_status(status_id=status['status_id'], table=table_status)
        for picture in table_pictures.find(user_id=user_id):
            delete_picture(picture["picture_id"], table_pictures)
    return remove_user(user_id=user_id)


def search_user(user_id, table):
    '''
    Searches for a user in user_collection(which is an instance of
    UserCollection).

    Requirements:
    - If the user is found, returns the corresponding User instance.
    - Otherwise, it returns None.
    '''
    find_user = users.search_user(table)
    return find_user(user_id=user_id)

def get_all_users(table):
    """Retrieves all users in the db"""
    return users.get_all_users(table)

def update_status(status_id, user_id, status_text, table_users, table_status):
    '''
    Updates the values of an existing status_id

    Requirements:
    - Returns False if there any errors.
    - Otherwise, it returns True.
    '''
    if not search_user(user_id, table_users):
        print(f"Unable to update status, user {user_id} does not exist")
        return False
    update_status_inner = user_status.modify_status(table_status)
    return update_status_inner(status_id=status_id,
                               user_id=user_id,
                               status_text=status_text,
                               columns=['status_id'])


def delete_status(status_id, table):
    '''
    Deletes a status_id from user_collection.

    Requirements:
    - Returns False if there are any errors (such as status_id not found)
    - Otherwise, it returns True.
    '''
    delete_status_inner = user_status.delete_status(table)
    return delete_status_inner(status_id=status_id)


def search_status(status_id, table):
    '''
    Searches for a status in status_collection

    Requirements:
    - If the status is found, returns the corresponding
    UserStatus instance.
    - Otherwise, it returns None.
    '''
    search_status_inner = user_status.search_status(table)
    return search_status_inner(status_id=status_id)

def add_picture(user_id, tags, table_users, table_pictures):
    '''
    Adds a picture to the db
    '''
    if not search_user(user_id, table_users):
        print("Unable to add picture, user does not exist")
        return False
    add_picture_to_db = pictures.add_picture(table_pictures)
    picture_id = pictures.create_key(table_pictures)
    return add_picture_to_db(picture_id=picture_id, user_id=user_id, tags=tags)

def update_picture(picture_id, user_id, tags, table_users, table_pictures):
    '''
    Updates a picture in the db
    '''
    if search_picture(picture_id, table_pictures):
        if not search_user(user_id, table_users):
            print("Unable to update picture, user does not exist")
            return False
        update_picture_in_db = pictures.modify_picture(table_pictures)
        return update_picture_in_db(picture_id=picture_id, user_id=user_id, tags=tags)
    print(f"Picture ID {picture_id} was not found")
    return False

def search_picture(picture_id, table):
    '''
    Searches for a picture in the db
    '''
    search_picture_in_db = pictures.search_picture(table)
    return search_picture_in_db(picture_id=picture_id)

def delete_picture(picture_id, table):
    '''
    Deletes a picture in the db
    '''
    delete_picture_in_db = pictures.delete_picture(table)
    return delete_picture_in_db(picture_id=picture_id)

def get_all_pictures(table):
    """Gets all pictures in the db"""
    return pictures.get_all_pictures(table)

def save_all_pictures(table):
    '''
    Saves all pictures in the db
    '''
    pics = pictures.get_all_pictures(table)
    for pic in pics:
        picture_id = pic["picture_id"]
        user_id = pic["user_id"]
        # deconstruct tags into a list
        tags = deconstruct_tags(pic["tags"])
        # create paths and their directories
        folder_path = path.join("pictures", user_id, *tags)
        makedirs(folder_path, exist_ok=True)
        file_path = path.join(folder_path, f"{picture_id}.png")
        # create file
        with open(file_path, "w"):
            pass
    return True

def deconstruct_tags(tags):
    '''
    Deconstructs a string tags into a list of tags
    '''
    # add extra space at start so split works
    tags = " " + tags
    tags_list = tags.split(" #")
    # first slot will be empty so skip it and return sorted list
    return sorted(tags_list[1:])

def get_all_user_pictures(user_id):
    '''
    Returns all pictures for a user
    '''
    picture_paths = []
    start_path = path.join("pictures", user_id)
    if path.isdir(start_path):
        walk_user_picture_directories(start_path, picture_paths)
        return picture_paths
    return None

def walk_user_picture_directories(current_path, path_list):
    '''
    Walk user picture directories and get all paths
    '''
    if path.isfile(current_path):
        user_id = path.split(current_path)[0]
        file_name = path.split(current_path)[-1]
        path_list.append((user_id, current_path, file_name))
        return
    for sub_path in listdir(current_path):
        new_path = path.join(current_path, sub_path)
        walk_user_picture_directories(new_path, path_list)
    return path_list

def reconcile_pictures(table):
    '''
    Returns pictures that were found in the db but not the local
    file system and vice versa
    '''
    # gets all picture data for tags and ids
    db_pics_data = {}
    for pic in pictures.get_all_pictures(table):
        picture_id = pic["picture_id"]
        tags = deconstruct_tags(pic["tags"])
        pic_path = path.join("pictures", pic["user_id"], *tags, picture_id + ".png")
        db_pics_data[picture_id] = pic_path
    # if no folder in local, all pictures are missing from local
    if not path.isdir("pictures"):
        return None, [(pic_path, pic_id) for pic_id, pic_path in db_pics_data.items()]
    # gets local picture data
    local_pics_data = {}
    for file in get_all_user_pictures(""):
        local_pics_data[file[2][:-4]] = file[1]
    # cross checks to find which files are missing
    missing_from_db = [{"picture_path":pic_path, "picture_id":pic_id} for pic_id, pic_path
                       in local_pics_data.items()
                       if pic_id not in db_pics_data.keys()]
    missing_from_local = [{"picture_path":pic_path, "picture_id":pic_id} for pic_id, pic_path
                          in db_pics_data.items()
                          if pic_id not in local_pics_data.keys()]
    return missing_from_db, missing_from_local
