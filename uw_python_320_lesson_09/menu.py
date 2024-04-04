'''
Provides a basic frontend
'''
import sys
from loguru import logger
from connection import Connection
from verify_input import verify_tag
import main

logger.remove()
logger.add('logs_{time:YYYY-MM-DD}.log', level="DEBUG")
logger.add(sys.stderr, level="DEBUG")

def load_users():
    '''
    Loads user accounts from a file
    '''
    filename = input('Enter filename of user file: ')
    main.load_users(filename, user_table)


def load_status_updates():
    '''
    Loads status updates from a file
    '''
    filename = input('Enter filename for status file: ')
    main.load_status_updates(filename, table_status=status_table, table_users=user_table)


def add_user():
    '''
    Adds a new user into the database
    '''
    user_id = input('User ID: ')
    while len(user_id) >= 30 or len(user_id) == 0:
        user_id = input('User ID cannot be blank or more than 30 characters: ')
    email = input('User email: ')
    while len(email) == 0:
        email = input('Email cannot be blank: ')
    user_name = input('User name: ')
    while len(user_name) >= 30 or len(user_name) == 0:
        user_name = input('User name cannot be blank or more than 30 characters: ')
    user_last_name = input('User last name: ')
    while len(user_last_name) > 100 or len(user_last_name) == 0:
        user_last_name = input('User last name cannot be blank or more than 100 characters: ')
    if main.add_user(user_id, email, user_name, user_last_name, user_table):
        print("User was successfully added")


def update_user():
    '''
    Updates information for an existing user
    '''
    user_id = input('User ID: ')
    while len(user_id) == 0:
        user_id = input('User ID cannot be blank: ')
    email = input('User email: ')
    while len(email) == 0:
        email = input('Email cannot be blank: ')
    user_name = input('User name: ')
    while len(user_name) > 30 or len(user_name) == 0:
        user_name = input('User name cannot be blank or more than 30 characters: ')
    user_last_name = input('User last name: ')
    while len(user_last_name) > 100 or len(user_last_name) == 0:
        user_last_name = input('User last name cannot be blank or more than 100 characters: ')
    if main.update_user(user_id, email, user_name, user_last_name, user_table) == 1:
        print("User was successfully updated")
    else:
        print("An error occurred while trying to update user")



def search_user():
    '''
    Searches a user in the database
    '''
    user_id = input('Enter user ID to search: ')
    result = main.search_user(user_id, table=user_table)
    if not result:
        print(f"ERROR: User {user_id} does not exist")
    else:
        print(f"User ID: {result['user_id']}")
        print(f"Email: {result['user_email']}")
        print(f"Name: {result['user_name']}")
        print(f"Last name: {result['user_last_name']}")


def delete_user():
    '''
    Deletes user from the database
    '''
    user_id = input('User ID: ')
    if main.delete_user(user_id, table_users=user_table, table_status=status_table):
        print(f"User {user_id} was successfully deleted")
    else:
        print(f"ERROR: User {user_id} does not exist")


def add_status():
    '''
    Adds a new status into the database
    '''
    user_id = input('User ID: ')
    while len(user_id) == 0:
        user_id = input('User ID cannot be blank: ')
    status_id = input('Status ID: ')
    while len(status_id) >= 30 or len(status_id) == 0:
        status_id = input('Status ID cannot be blank or more than 30 characters: ')
    status_text = input('Status text: ')
    if main.add_status(status_id=status_id,
                       user_id=user_id,
                       status_text=status_text,
                       table_status=status_table,
                       table_users=user_table):
        print("New status was successfully added")


def update_status():
    '''
    Updates information for an existing status
    '''
    user_id = input('User ID: ')
    while len(user_id) == 0:
        user_id = input('User ID cannot be blank: ')
    status_id = input('Status ID: ')
    while len(status_id) >= 30 or len(status_id) == 0:
        status_id = input('Status ID cannot be blank or more than 30 characters: ')
    status_text = input('Status text: ')
    while len(status_text) == 0:
        status_text = input('Status text cannot be blank: ')
    if main.update_status(status_id=status_id,
                          user_id=user_id,
                          status_text=status_text,
                          table_status=status_table,
                          table_users=user_table):
        print("Status was successfully updated")
    else:
        print("An error occurred while trying to update status")


def search_status():
    '''
    Searches a status in the database
    '''
    status_id = input('Enter status ID to search: ')
    result = main.search_status(status_id, table=status_table)
    if not result:
        print("ERROR: Status does not exist")
    else:
        print(f"User ID: {result['user_id']}")
        print(f"Status ID: {result['status_id']}")
        print(f"Status text: {result['status_text']}")


def delete_status():
    '''
    Deletes status from the database
    '''
    status_id = input('Status ID: ')
    if main.delete_status(status_id, table=status_table):
        print("Status was successfully deleted")
    else:
        print("An error occurred while trying to delete status")

def add_picture():
    """
    Adds a picture to the database
    """
    user_id = input("User ID: ")
    tags = get_tags()
    if main.add_picture(user_id, tags, user_table, picture_table):
        print("Picture added successfully")
    else:
        print("An error occurred when adding the picture")

def update_picture():
    """
    Updates a picture in the database
    """
    picture_id = input("Picture ID: ")
    user_id = input("User ID: ")
    tags = get_tags()
    if main.update_picture(picture_id, user_id, tags, user_table, picture_table):
        print("Picture updated successfully")
    else:
        print("An error occurred when updating the picture")

def search_picture():
    """
    Searches a picture in the database
    """
    picture_id = input("Picture ID: ")
    result = main.search_picture(picture_id, picture_table)
    if result:
        print(f"Picture ID: {result['picture_id']}")
        print(f"User ID: {result['user_id']}")
        print(f"Tags: {result['tags']}")
    else:
        print("ERROR: Picture was not found")

def delete_picture():
    """
    Deletes a picture in the database
    """
    picture_id = input("Picture ID: ")
    if main.delete_picture(picture_id, picture_table):
        print("Picture updated successfully")
    else:
        print("An error occurred when deleting the picture")

def get_tags():
    """
    Gets tags into the right format
    """
    tag_list = []
    tag_len = 0
    while True:
        tag_flag = input("Would you like to enter a tag? (Y/N): ").lower()
        if tag_len > 101:
            print("You have reached the tag character limit. Your last tag will be dropped off to fit the limit.")
            break
        # gets input for the tag and makes sure it is valid
        if tag_flag == "y":
            not_verified = True
            while not_verified:
                tag = input("Please enter your tag: ")
                if verify_tag(tag)[0]:
                    tag_list.append(tag)
                    tag_len += (len(tag) + 2)
                    not_verified = False
                else:
                    print(verify_tag(tag)[1])
        # leaves loop with given tags
        elif tag_flag == "n":
            break
        # catches answers that are not y/n
        else:
            print("Please enter a valid option")
    
    tags = " #".join(tag_list)
    tags = "#" + tags
    return tags

def save_pictures():
    """
    Saves all pictures in the db
    """
    main.save_all_pictures(picture_table)

def list_user_pictures():
    """
    Lists all pictures for a user
    """
    user_id = input("User ID: ")
    pictures = main.get_all_user_pictures(user_id)
    if pictures:
        for picture in pictures:
            print(picture)
    else:
        print("No pictures found for user")

def reconcile_pictures():
    """
    Print out db pictures that are missing from local files
    """
    missing_from_db, missing_from_local = main.reconcile_pictures(picture_table)
    if missing_from_db:
        print("*** MISSING FROM DB ***")
        for missing_db_pic in missing_from_db:
            print(f"Picture {missing_db_pic[1]} with path {missing_db_pic[0]} is missing from the database")
        print("*** MISSING FROM LOCAL ***")
        for missing_local_pic in missing_from_local:
            print(f"Picture {missing_local_pic[1]} with path {missing_local_pic[0]} is missing from local files")
    else:
        print("!!! ALL DATABASE FILES ARE MISSING FROM LOCAL !!!")
        for missing_local_pic in missing_from_local:
            print(f"Picture {missing_local_pic[1]} with path {missing_local_pic[0]} is missing from local files")

def quit_program():
    '''
    Quits program
    '''
    sys.exit()


if __name__ == '__main__':
    with Connection() as connection:
        user_table = connection.user_table
        status_table = connection.status_table
        picture_table = connection.picture_table
        menu_options = {
            'A': load_users,
            'B': load_status_updates,
            'C': add_user,
            'D': update_user,
            'E': search_user,
            'F': delete_user,
            'G': add_status,
            'H': update_status,
            'I': search_status,
            'J': delete_status,
            "K": add_picture,
            "L": update_picture,
            "M": search_picture,
            "N": delete_picture,
            "O": save_pictures,
            "P": list_user_pictures,
            "R": reconcile_pictures,
            'Q': quit_program
        }
        while True:
            user_selection = input("""
                                A: Load user database
                                B: Load status database
                                C: Add user
                                D: Update user
                                E: Search user
                                F: Delete user
                                G: Add status
                                H: Update status
                                I: Search status
                                J: Delete status
                                K: Add picture
                                L: Update picture
                                M: Search picture
                                N: Delete picture
                                O: Save pictures
                                P: List all pictures for a user
                                R: Reconcilie pictures
                                Q: Quit

                                Please enter your choice: """)
            if user_selection.upper() in menu_options:
                menu_options[user_selection.strip().upper()]()
            else:
                print("Invalid option")