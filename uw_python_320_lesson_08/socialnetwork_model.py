"""
File for establishing the database schema
"""
# pylint: disable=R0903, E0401
from playhouse.dataset import DataSet

DATABASE = "database.db"

def get_ds():
    """
    Gets and returns the database used in other files
    """
    ds = DataSet(f"sqlite:///{DATABASE}")
    return ds
