'''
Classes for user information for the social network project
'''
# pylint: disable=R0903, E0401
import logging
from datetime import datetime
from peewee import IntegrityError, DoesNotExist
from socialnetwork_model import UserModel

# set up logging for users.py file
log_file_name = "log_" + datetime.now().strftime("%m_%d_%Y")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
# logger.setLevel(logging.DEBUG)
log_file = logging.FileHandler(filename = log_file_name)
formatter = logging.Formatter("""%(asctime)s ~ %(filename)s ~ %(message)s""")
log_file.setFormatter(formatter)
logger.addHandler(log_file)

class UserCollection():
    '''
    Contains a collection of Users objects
    '''

    def __init__(self, database):
        self.database = database
        logger.debug("User database successfully linked")

    def add_user(self, user_id, email, user_name, user_last_name):
        '''
        Adds a new user to the collection
        '''
        try:
            with self.database.transaction():
                # create a row for the user ID in the database
                result = UserModel.create(
                    user_id = user_id,
                    user_email = email,
                    user_name = user_name,
                    user_last_name = user_last_name
                )
                # save new row
                result.save()
                logger.debug("User ID %s successfully added", user_id)
                return True
        # IntegrityError catches duplicate user_ids
        except IntegrityError:
            logger.debug("User ID %s tried to be added as a duplicate", user_id)
            return False

    def batch_load_users(self, data):
        """
        Adds new users to the collection with a batch load
        """
        try:
            with self.database.transaction():
                # create rows for the users in the database
                UserModel.insert_many(data).execute()
                logger.debug("User batch successfully added")
                return True
        except IntegrityError:
            logger.debug("User batch load did not contain unique IDs")
            return False

    def modify_user(self, user_id, email, user_name, user_last_name):
        '''
        Modifies an existing user
        '''
        with self.database.transaction():
            # get user ID to modify
            result = self.search_user(user_id)
            if result:
                # modify ID that was fetched
                result.user_email = email
                result.user_name = user_name
                result.user_last_name = user_last_name
                # save updated row
                result.save()
                logger.debug("User ID %s successfully modified", user_id)
                return True
            # return False if result is not found
            logger.debug("User ID %s cannot be modified as it does not exist", user_id)
            return False

    def delete_user(self, user_id):
        '''
        Deletes an existing user
        '''
        with self.database.transaction():
            # get user ID to delete
            result = self.search_user(user_id)
            if result:
                # delete ID that was fetched
                result.delete_instance()
                logger.debug("User ID %s successfully deleted", user_id)
                return True
            # return False if result is not found
            logger.debug("User ID %s cannot be deleted as it does not exist", user_id)
            return False

    def search_user(self, user_id):
        '''
        Searches for user data
        '''
        try:
            with self.database.transaction():
                # get user with user_id
                result = UserModel.get(UserModel.user_id == user_id)
                # return row that was feteched
                logger.debug("User ID %s sucessfully found", user_id)
                return result
        # DoesNotExist catches if the user_id does not exist
        except DoesNotExist:
            logger.debug("User ID %s cannot be found", user_id)
            return False
