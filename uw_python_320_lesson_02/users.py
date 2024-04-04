'''
Classes for user information for the social network project
'''
import logging
from datetime import datetime
# pylint: disable=R0903

# set up logging for users.py file
log_file_name = "log_" + datetime.now().strftime("%m_%d_%Y")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
log_file = logging.FileHandler(filename = log_file_name)
formatter = logging.Formatter("""%(asctime)s ~ %(filename)s ~ %(message)s""")
log_file.setFormatter(formatter)
logger.addHandler(log_file)

class Users():
    '''
    Contains user information
    '''

    def __init__(self, user_id, email, user_name, user_last_name):
        self.user_id = user_id
        self.email = email
        self.user_name = user_name
        self.user_last_name = user_last_name
        logger.debug(f"User ID {user_id} successfully created")


class UserCollection():
    '''
    Contains a collection of Users objects
    '''

    def __init__(self):
        self.database = {}
        logger.debug(f"User database successfully instantiated")

    def add_user(self, user_id, email, user_name, user_last_name):
        '''
        Adds a new user to the collection
        '''
        if user_id in self.database:
            # Rejects new status if status_id already exists
            logger.debug(f"User ID {user_id} already exists in the database")
            return False
        new_user = Users(user_id, email, user_name, user_last_name)
        self.database[user_id] = new_user
        logger.debug(f"User ID {user_id} successfully added to database")
        return True

    def modify_user(self, user_id, email, user_name, user_last_name):
        '''
        Modifies an existing user
        '''
        if user_id not in self.database:
            logger.debug(f"User ID {user_id} does not exist in the database")
            return False
        self.database[user_id].email = email
        self.database[user_id].user_name = user_name
        self.database[user_id].user_last_name = user_last_name
        logger.debug(f"User ID {user_id} successfully modified in the database")
        return True

    def delete_user(self, user_id):
        '''
        Deletes an existing user
        '''
        if user_id not in self.database:
            logger.debug(f"User ID {user_id} does not exist in the database")
            return False
        del self.database[user_id]
        logger.debug(f"User ID {user_id} successfully deleted from the database")
        return True

    def search_user(self, user_id):
        '''
        Searches for user data
        '''
        if user_id not in self.database:
            logger.debug(f"User ID {user_id} was not found in the database")
            return Users(None, None, None, None)
        logger.debug(f"User ID {user_id} was found in the database")
        return self.database[user_id]
