"""
Connection context manager
"""

from playhouse.dataset import DataSet
import socialnetwork_model

class Connection():
    """
    Creates a sqlite connection as a context manager
    """
    def __init__(self):
        """
        Creates the database
        """
        self.ds = DataSet('sqlite:///socialnetwork.db')
        self.user_table = self.ds['users']
        self.status_table = self.ds['status']
        self.picture_table = self.ds["pictures"]

    def __enter__(self):
        """
        Establishes initial connections
        """
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """
        Removes the connection to the database
        """
        self.ds.close()
