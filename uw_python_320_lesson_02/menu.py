'''
Provides a basic frontend
'''
import sys
import main


def load_users():
    '''
    Loads user accounts from a file
    '''
    filename = input('Enter filename of user file: ')
    main.load_users(filename, user_collection)

def load_status_updates():
    '''
    Loads status updates from a file
    '''
    filename = input('Enter filename for status file: ')
    main.load_status_updates(filename, status_collection)


def add_user():
    '''
    Adds a new user into the database
    '''
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    if main.add_user(user_id,
                         email,
                         user_name,
                         user_last_name,
                         user_collection):
        print("User was successfully added")
    else:
        print("An error occurred while trying to add new user")



def update_user():
    '''
    Updates information for an existing user
    '''
    user_id = input('User ID: ')
    email = input('User email: ')
    user_name = input('User name: ')
    user_last_name = input('User last name: ')
    if main.update_user(user_id, email, user_name, user_last_name, user_collection):
        print("User was successfully updated")
    else:
        print("An error occurred while trying to update user")



def search_user():
    '''
    Searches a user in the database
    '''
    user_id = input('Enter user ID to search: ')
    result = main.search_user(user_id, user_collection)
    if result.user_id:
        print(f"User ID: {result.user_id}")
        print(f"Email: {result.email}")
        print(f"Name: {result.user_name}")
        print(f"Last name: {result.user_last_name}")
    else:
        print("ERROR: User does not exist")



def delete_user():
    '''
    Deletes user from the database
    '''
    user_id = input('User ID: ')
    if main.delete_user(user_id, user_collection):
        print("User was successfully deleted")
    else:
        print("An error occurred while trying to delete user")



def save_users():
    '''
    Saves user database into a file
    '''
    filename = input('Enter filename for users file: ')
    main.save_users(filename, user_collection)


def add_status():
    '''
    Adds a new status into the database
    '''
    user_id = input('User ID: ')
    status_id = input('Status ID: ')
    status_text = input('Status text: ')
    if main.add_status(user_id, status_id, status_text, status_collection):
        print("New status was successfully added")
    else:
        print("An error occurred while trying to add new status")


def update_status():
    '''
    Updates information for an existing status
    '''
    user_id = input('User ID: ')
    status_id = input('Status ID: ')
    status_text = input('Status text: ')
    if main.update_status(status_id, user_id, status_text, status_collection):
        print("Status was successfully updated")
    else:
        print("An error occurred while trying to update status")


def search_status():
    '''
    Searches a status in the database
    '''
    status_id = input('Enter status ID to search: ')
    result = main.search_status(status_id, status_collection)
    if result.user_id:
        print(f"User ID: {result.user_id}")
        print(f"Status ID: {result.status_id}")
        print(f"Status text: {result.status_text}")
    else:
        print("ERROR: Status does not exist")


def delete_status():
    '''
    Deletes status from the database
    '''
    status_id = input('Status ID: ')
    if main.delete_status(status_id, status_collection):
        print("Status was successfully deleted")
    else:
        print("An error occurred while trying to delete status")


def save_status():
    '''
    Saves status database into a file
    '''
    filename = input('Enter filename for status file: ')
    main.save_status_updates(filename, status_collection)


def quit_program():
    '''
    Quits program
    '''
    sys.exit()


if __name__ == '__main__':
    user_collection = main.init_user_collection()
    status_collection = main.init_status_collection()
    menu_options = {
        'A': load_users,
        'B': load_status_updates,
        'C': add_user,
        'D': update_user,
        'E': search_user,
        'F': delete_user,
        'G': save_users,
        'H': add_status,
        'I': update_status,
        'J': search_status,
        'K': delete_status,
        'L': save_status,
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
                            G: Save user database to file
                            H: Add status
                            I: Update status
                            J: Search status
                            K: Delete status
                            L: Save status database to file
                            Q: Quit

                            Please enter your choice: """).upper()
        if user_selection in menu_options:
            menu_options[user_selection]()
        else:
            print("Invalid option")