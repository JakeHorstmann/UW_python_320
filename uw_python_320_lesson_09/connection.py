"""
Connection context manager
"""

import socialnetwork_model
from playhouse.dataset import DataSet

class Connection():
    """
    Creates a sqlite connection as a context manager
    """
    def __init__(self):
        """
        Creates the database
        """
        self.ds = DataSet('sqlite:///socialnetwork.db')

    def __enter__(self):
        """
        Establishes initial connections
        """
        self.user_table = self.ds['users']
        self.status_table = self.ds['status']
        self.picture_table = self.ds["pictures"]
        
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """
        Removes the connection to the database
        """
        self.ds.close()