'''
Classes for user information for the social network project
'''
# pylint: disable=R0903
import sys
from loguru import logger
from peewee import IntegrityError
from sqlite3 import IntegrityError as IntegrityError2

logger.remove()
logger.add('logs_{time:YYYY-MM-DD}.log', level="DEBUG")
logger.add(sys.stderr, level="DEBUG")


def add_user(db):
    '''
    Adds a new user to the collection
    '''
    def insert_user(**kwargs):
        try:
            return db.insert(**kwargs)
        except (IntegrityError, IntegrityError2) as e:
            logger.error(f"The user id {kwargs.get('user_id')} already exists")
            print(f"ERROR: User {kwargs.get('user_id')} already exists")
            return False
    return insert_user


def search_user(db):
    def search(**kwargs):
        try:
            return db.find_one(**kwargs)
        except KeyError:
            return None
    return search


def modify_user(db):
    '''
    Modifies an existing user
    '''
    def update_user(**kwargs):
        try:
            return db.update(**kwargs)
        except (IntegrityError, IntegrityError2, KeyError):
            logger.error(f"User {kwargs.get('user_id')} was not found")
            print(f"User {kwargs.get('user_id')} was not found")
            return False
    return update_user


def delete_user(db):
    '''
    Deletes an existing user
    '''
    def remove_user(**kwargs):
        try:
            return db.delete(**kwargs)
        except KeyError:
            return False
    return remove_user


