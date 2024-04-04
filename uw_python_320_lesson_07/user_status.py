'''
classes to manage the user status messages
'''
# pylint: disable=R0903, E0401
from datetime import datetime
from pymongo import MongoClient

class UserStatusCollection():
    '''
    Collection of UserStatus messages
    '''

    def __init__(self, host, port, database_name, table_name):
        client = MongoClient(host = host, port = port)
        database = client[database_name][table_name]
        self.database = database

    def add_status(self, status_id, user_id, status_text):
        '''
        add a new status message to the collection
        '''
        if self.search_status(status_id):
            # Rejects new status if status id already exists
            return False
        data = {"_id": status_id,
                "user_id": user_id,
                "status_text": status_text}
        self.database.insert_one(data)
        return True

    def batch_load_statuses(self, data):
        """
        Adds new statuses to the collection with a batch load
        """
        for row in data:
            if self.search_status(row["_id"]):
                # Rejects new status batch if it contains a duplicate
                return False
        self.database.insert_many(data)
        return True

    def modify_status(self, status_id, user_id, status_text):
        '''
        Modifies a status message

        The new user_id and status_text are assigned to the existing message
        '''
        results = self.search_status(status_id)
        if not results:
            # rejects a status that DNE
            return False
        data = {"_id": status_id,
                "user_id": user_id,
                "status_text": status_text}
        self.database.update_one(results, {"$set": data})
        return True


    def delete_status(self, status_id):
        '''
        deletes the status message with id, status_id
        '''
        if not self.search_status(status_id):
            # Rejects new status if status id already exists
            return False
        self.database.delete_one({"_id": status_id})
        return True

    def search_status(self, status_id):
        '''
        Find and return a status message by its status_id

        Returns an empty UserStatus object if status_id does not exist
        '''
        query = {"_id": status_id}
        results = self.database.find_one(query)
        if not results:
            return False
        return results

    def search_all_status_updates(self, user_id):
        """
        Returns all status updates for a user
        """
        query = {"user_id": user_id}
        len_of_results = self.database.count_documents(query)
        results = self.database.find(query)
        return len_of_results, results

    def filter_status_by_string(self, phrase):
        """
        Returns all status that contain the phrase
        """
        # regex = f"{phrase}/"
        # print(type(regex))
        query = {"status_text": {"$regex": phrase}}
        results = self.database.find(query)
        return results
