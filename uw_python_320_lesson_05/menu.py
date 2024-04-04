'''
Provides a basic frontend
'''
import sys
from pymongo import MongoClient
import main
from verify_input import verify_yes_or_no

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
    main.load_status_updates(filename, status_collection, user_collection)


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
    if result:
        print(f"User ID: {result['_id']}")
        print(f"Email: {result['user_email']}")
        print(f"Name: {result['user_name']}")
        print(f"Last name: {result['user_last_name']}")
    else:
        print("ERROR: User does not exist")



def delete_user():
    '''
    Deletes user from the database
    '''
    user_id = input('User ID: ')
    if main.delete_user(user_id, user_collection, status_collection):
        print("User was successfully deleted")
    else:
        print("An error occurred while trying to delete user")


def add_status():
    '''
    Adds a new status into the database
    '''
    user_id = input('User ID: ')
    status_id = input('Status ID: ')
    status_text = input('Status text: ')
    if main.add_status(user_id, status_id, status_text, status_collection, user_collection):
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
    if main.update_status(status_id, user_id, status_text, status_collection, user_collection):
        print("Status was successfully updated")
    else:
        print("An error occurred while trying to update status")


def search_status():
    '''
    Searches a status in the database
    '''
    status_id = input('Enter status ID to search: ')
    result = main.search_status(status_id, status_collection)
    if result:
        print(f"User ID: {result['user_id']}")
        print(f"Status ID: {result['_id']}")
        print(f"Status text: {result['status_text']}")
    else:
        print("ERROR: Status does not exist")

def search_all_status_updates():
    """
    Finds all statuses for a given user
    """
    user_id = input("User ID: ")
    result_len, results = main.search_all_status_updates(user_id, status_collection)
    if results:
        # determine is the sentence needs plural forms or not
        plural_status = "" if result_len == 1 else "es"
        was_or_were = "was" if result_len == 1 else "were"
        # print how many results were found for the user
        print(f"A total of {result_len} status{plural_status} {was_or_were} found for {user_id}")
        user_response = input("Would you like to see the next status update? (Y/N): ").lower()
        # loop while user is not entering the right response
        while not verify_yes_or_no(user_response):
            user_response = input("Please enter a valid choice (Y/N): ").lower()
        # loop while the user wants to see more statuses
        while user_response == "y":
            try:
                # print next status and ask if they want to see the next
                print(next(results)["status_text"])
                user_response = input("Would you like to see the next status update? (Y/N): "
                                      ).lower()
                # loop while user is not entering thne right response
                while not verify_yes_or_no(user_response):
                    user_response = input("Please enter a valid choice (Y/N): ").lower()
            # this error means we have reached the final status
            except StopIteration:
                print("INFO: You have reached the last status update")
                user_response = "n"
    else:
        print("An error occurred while searching for that user")

def filter_status_by_string():
    """
    Find all statuses with a certain phrase
    """
    # string to search for in statuses
    search_string = input("Enter the string to search: ")
    # get statuses with the search_string in their status text
    results = main.filter_status_by_string(search_string, status_collection)
    if results:
        # determine if user wants to see next status
        user_response = input("Review the next status? (Y/N): ").lower()
        # loop while user does not enter Y/N
        while not verify_yes_or_no(user_response):
            user_response = input("Please enter a valid choice (Y/N): ").lower()
        while user_response == "y":
            try:
                # get the next status
                result = next(results)
                print(result['status_text'])
                # ask user if they want to delete status
                ask_to_delete_status(result)
                user_response = input("Review the next status? (Y/N): ").lower()
                while not verify_yes_or_no(user_response):
                    user_response = input("Please enter a valid choice (Y/N): ").lower()
            # catch when user reaches the end of the statuses
            except StopIteration:
                print("INFO: You have reached the last status update")
                user_response = "n"

def ask_to_delete_status(status):
    """
    Ask the user if they would like to delete the status
    """
    # get y/n response from user
    response = input("Would you like to delete this status? (Y/N): ").lower()
    while not verify_yes_or_no(response):
        response = input("Please enter a valid choice (Y/N): ").lower()
    # delete status if they approve
    if response == "y":
        main.delete_status(status['_id'], status_collection)

def delete_status():
    '''
    Deletes status from the database
    '''
    status_id = input('Status ID: ')
    if main.delete_status(status_id, status_collection):
        print("Status was successfully deleted")
    else:
        print("An error occurred while trying to delete status")

def flagged_status_updates():
    """
    Prints all statuses returned by filter_status_by_string
    """
    # string to search for in statuses
    search_string = input("Enter the string to search: ")
    # get statuses with the search_string in their status text
    results = main.filter_status_by_string(search_string, status_collection)
    # print out (status_id, status_text) for each row returned
    for status_tuple in [(result['_id'], result['status_text']) for result in results]:
        print(status_tuple)

def quit_program():
    '''
    Quits program
    '''
    sys.exit()


if __name__ == '__main__':
    client = MongoClient(host="localhost", port = 27017)
    user_collection = main.init_user_collection(client)
    status_collection = main.init_status_collection(client)
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
        'J': search_all_status_updates,
        'K': filter_status_by_string,
        'L': flagged_status_updates,
        'M': delete_status,
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
                            J: Search all statuses for a user
                            K: Search all status updates matching a string
                            L: Show all flagged status updates
                            M: Delete status
                            Q: Quit

                            Please enter your choice: """).upper()
        if user_selection in menu_options:
            menu_options[user_selection]()
        else:
            print("Invalid option")
