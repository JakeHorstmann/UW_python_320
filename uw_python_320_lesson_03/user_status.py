'''
classes to manage the user status messages
'''
# pylint: disable=R0903, E0401
import logging
from datetime import datetime
from peewee import IntegrityError, DoesNotExist
from socialnetwork_model import StatusModel

# set up logging for user_status file
log_file_name = "log_" + datetime.now().strftime("%m_%d_%Y")
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
log_file = logging.FileHandler(filename = log_file_name)
formatter = logging.Formatter("""\
%(asctime)s ~ %(filename)s ~ %(funcName)s ~ %(message)s\
""")
log_file.setFormatter(formatter)
logger.addHandler(log_file)

class UserStatusCollection():
    '''
    Collection of UserStatus messages
    '''

    def __init__(self, database):
        self.database = database
        logger.debug("Status database successfully linked")

    def add_status(self, status_id, user_id, status_text):
        '''
        add a new status message to the collection
        '''
        try:
            with self.database.transaction():
                # create a row for the status ID in the database
                result = StatusModel.create(
                    status_id = status_id,
                    user_id = user_id,
                    status_text = status_text
                )
                # save new row
                result.save()
                logger.debug("Status ID %s successfully added", status_id)
                return True
        # IntegrityError catches duplicate status_ids
        except IntegrityError:
            # not necessarily true. may be a foreign key error
            logger.debug("Status ID %s tried to be added as a duplicate", status_id)
            return False

    def modify_status(self, status_id, user_id, status_text):
        '''
        Modifies a status message

        The new user_id and status_text are assigned to the existing message
        '''
        try:
            with self.database.transaction():
                # get status ID to modify
                result = self.search_status(status_id)
                if result:
                    # modify ID that was fetched
                    result.user_id = user_id
                    result.status_text = status_text
                    # save updated row
                    result.save()
                    logger.debug("Status ID %s successfully modified", status_id)
                    return True
                # return False if result is not found
                logger.debug("Status ID %s cannot be deleted as it does not exist", status_id)
                return False
        # catches foreign keys that do not exist
        except IntegrityError:
            logger.debug("User ID %s does not exist as a foreign key", user_id)
            return False


    def delete_status(self, status_id):
        '''
        deletes the status message with id, status_id
        '''
        with self.database.transaction():
            # get status ID to delete
            result = self.search_status(status_id)
            if result:
                # delete ID that was fetched
                result.delete_instance()
                logger.debug("Status ID %s successfully deleted", status_id)
                return True
            # return False if result is not found
            logger.debug("Status ID %s cannot be deleted as it does not exist", status_id)
            return False

    def search_status(self, status_id):
        '''
        Find and return a status message by its status_id

        Returns an empty UserStatus object if status_id does not exist
        '''
        try:
            with self.database.transaction():
                # get row with status_id
                result = StatusModel.get(StatusModel.status_id == status_id)
                # return row that was fetched
                logger.debug("Status ID %s successfully found", status_id)
                return result
        # DoesNotExist catches if the status_id does not exist
        except DoesNotExist:
            logger.debug("Status ID %s cannot be found", status_id)
            return False
