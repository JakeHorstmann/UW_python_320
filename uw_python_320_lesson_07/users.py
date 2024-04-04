'''
Classes for user information for the social network project
'''
# pylint: disable=R0903, E0401
from pymongo import MongoClient

class UserCollection():
    '''
    Contains a collection of Users objects
    '''

    def __init__(self, host, port, database_name, table_name):
        client = MongoClient(host = host, port = port)
        database = client[database_name][table_name]
        self.database = database

    def add_user(self, user_id, email, user_name, user_last_name):
        '''
        Adds a new user to the collection
        '''
        if self.search_user(user_id):
            # Rejects new user if user id already exists
            return False
        data = {"_id": user_id,
                "user_email": email,
                "user_name": user_name,
                "user_last_name": user_last_name}
        self.database.insert_one(data)
        return True

    def batch_load_users(self, data):
        """
        Adds new users to the collection with a batch load
        """
        for row in data:
            if self.search_user(row["_id"]):
                # Rejects new user batch if it contains a duplicate
                return False
        self.database.insert_many(data)
        return True

    def modify_user(self, user_id, email, user_name, user_last_name):
        '''
        Modifies an existing user
        '''
        results = self.search_user(user_id)
        if not results:
            return False
        data = {"_id": user_id,
                "user_email": email,
                "user_name": user_name,
                "user_last_name": user_last_name}
        self.database.update_one(results, {"$set": data})
        return True

    def delete_user(self, user_id):
        '''
        Deletes an existing user
        '''
        if not self.search_user(user_id):
            return False
        self.database.delete_one({"_id": user_id})
        return True

    def search_user(self, user_id):
        '''
        Searches for user data
        '''
        results = self.database.find_one({"_id": user_id})
        if not results:
            return False
        return results
    
    def count_users_with_id(self, user_ids):
        """
        Searches multiple users
        """
        query = {"_id": {"$in": user_ids}}
        results = self.database.count_documents(query)
        if not results:
            return 0
        return results
