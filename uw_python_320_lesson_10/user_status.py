'''
classes to manage the user status messages
'''
# pylint: disable=R0903
import sys
from sqlite3 import IntegrityError as IntegrityError2
from loguru import logger
from peewee import IntegrityError

logger.remove()
logger.add('logs_{time:YYYY-MM-DD}.log', level="DEBUG")
logger.add(sys.stderr, level="DEBUG")

def add_status(db):
    '''
    add a new status message to the collection
    '''
    def new_status(**kwargs):
        try:
            return db.insert(**kwargs)
        except (IntegrityError, IntegrityError2):
            logger.error(f"Status ID {kwargs.get('status_id')} already exists")
            print(f"Status ID {kwargs.get('status_id')} already exists")
            return False
    return new_status


def modify_status(db):
    '''
    Modifies a status message

    The new user_id and status_text are assigned to the existing message
    '''
    def change_status(**kwargs):
        try:
            return db.update(**kwargs)
        except KeyError:
            return False
    return change_status

def delete_status(db):
    '''
    deletes the status message with id, status_id
    '''
    def remove_status(**kwargs):
        try:
            return db.delete(**kwargs)
        except KeyError:
            return False
    return remove_status


def search_status(db):
    '''
    Find and return a status message by its status_id

    Returns an empty UserStatus object if status_id does not exist
    '''
    def search(**kwargs):
        try:
            return db.find_one(**kwargs)
        except KeyError:
            return None
    return search
