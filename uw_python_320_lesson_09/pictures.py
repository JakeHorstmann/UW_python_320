'''
Functions for picture information for the social network project
'''
# pylint: disable=R0903
from loguru import logger
from peewee import IntegrityError
from sqlite3 import IntegrityError as IntegrityError2


def add_picture(db):
    '''
    add a new picture to the collection
    '''
    def add(**kwargs):
        try:
            return db.insert(**kwargs)
        except (IntegrityError, IntegrityError2):
            print(f"Picture ID {kwargs.get('picture_id')} already exists")
            return False
    return add

def modify_picture(db):
    '''
    modifies a picture message
    '''
    def modify(**kwargs):
        try:
            return db.update(**kwargs)
        except KeyError:
            return False
    return modify

def delete_picture(db):
    '''
    deletes the picture
    '''
    def delete(**kwargs):
        try:
            return db.delete(**kwargs)
        except KeyError:
            return False
    return delete

def search_picture(db):
    '''
    find and return a picture
    '''
    def search(**kwargs):
        try:
            return db.find_one(**kwargs)
        except KeyError:
            return None
    return search

def create_key(db):
    '''
    creates a unique PK for a picture
    '''
    num_of_pics = len(get_all_pictures(db))
    picture_id = f"{(num_of_pics+1):08}"
    while search_picture(db)(picture_id=picture_id):
        picture_id = f"{(num_of_pics+1):08}"
    return picture_id

def get_all_pictures(db):
    '''
    get all pictures in the db
    '''
    pics = db.find()
    return pics