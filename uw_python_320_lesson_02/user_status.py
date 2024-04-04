'''
classes to manage the user status messages
'''
import logging
from datetime import datetime
# pylint: disable=R0903

# set up logging for user_status file
log_file_name = "log_" + datetime.now().strftime("%m_%d_%Y")
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
log_file = logging.FileHandler(filename = log_file_name)
formatter = logging.Formatter("""\
%(asctime)s ~ %(filename)s ~ %(funcName)s ~ %(message)s\
""")
log_file.setFormatter(formatter)
logger.addHandler(log_file)

class UserStatus():
    '''
    class to hold status message data
    '''

    def __init__(self, status_id, user_id, status_text):
        self.status_id = status_id
        self.user_id = user_id
        self.status_text = status_text
        logger.debug(f"Status {status_id} successfully created")


class UserStatusCollection():
    '''
    Collection of UserStatus messages
    '''

    def __init__(self):
        self.database = {}
        logger.debug(f"Status database successfully instantiated")

    def add_status(self, status_id, user_id, status_text):
        '''
        add a new status message to the collection
        '''
        if status_id in self.database:
            # Rejects new status if status_id already exists
            logger.debug(f"Status ID {status_id} already exists in the database")
            return False
        new_status = UserStatus(status_id, user_id, status_text)
        self.database[status_id] = new_status
        logger.debug(f"Status ID {status_id} successfully added to the database")
        return True

    def modify_status(self, status_id, user_id, status_text):
        '''
        Modifies a status message

        The new user_id and status_text are assigned to the existing message
        '''
        if status_id not in self.database:
            # Rejects update is the status_id does not exist
            logger.debug(f"Status ID {status_id} does not exist in the database")
            return False
        self.database[status_id].user_id = user_id
        self.database[status_id].status_text = status_text
        logger.debug(f"Status ID {status_id} successfully modified in the database")
        return True

    def delete_status(self, status_id):
        '''
        deletes the status message with id, status_id
        '''
        if status_id not in self.database:
            # Fails if status does not exist
            logger.debug(f"Status ID {status_id} does not exist in the database")
            return False
        del self.database[status_id]
        logger.debug(f"Status ID {status_id} successfully deleted from the database")
        return True

    def search_status(self, status_id):
        '''
        Find and return a status message by its status_id

        Returns an empty UserStatus object if status_id does not exist
        '''
        if status_id not in self.database:
            # Fails if the status does not exist
            logger.debug(f"Status ID {status_id} was not found in the database")
            return UserStatus(None, None, None)
        logger.debug(f"Status ID {status_id} was found in the database")
        return self.database[status_id]
