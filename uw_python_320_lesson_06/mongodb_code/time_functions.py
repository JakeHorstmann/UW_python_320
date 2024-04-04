import time
import main, users, user_status
from pymongo import MongoClient

class TimeCode():
    def __init__(self, user_db_name, status_db_name):
        # set up mongodb database
        client = MongoClient(host = "localhost", port = 27017)
        self.db = client.database
        self.user_collection = users.UserCollection(self.db[user_db_name])
        self.status_collection = user_status.UserStatusCollection(self.db[status_db_name])


    def timeit(method):
        def timed(*args, **kwargs):
            start = time.time()
            result = method(*args, **kwargs)
            end = time.time()
            total_time = round((end-start) * 1000, 2)
            print(f"Total time for {method.__name__} was {total_time}ms")
            return result

        return timed

    def reset_tables(self, user_db_name, status_db_name):
        self.db[user_db_name].drop()
        self.db[status_db_name].drop()

    @timeit
    def add_user(self, user_id, user_email, user_name, user_last_name):
        main.add_user(user_id, user_email, user_name, user_last_name, self.user_collection)
    @timeit
    def update_user(self, user_id, user_email, user_name, user_last_name):
        main.update_user(user_id, user_email, user_name, user_last_name, self.user_collection)
    @timeit
    def delete_user(self, user_id):
        main.delete_user(user_id, self.user_collection, self.status_collection)
    @timeit
    def search_user(self, user_id):
        main.search_user(user_id, self.user_collection)
    @timeit
    def load_user_csv(self, path):
        main.load_users(path, self.user_collection)
    @timeit
    def load_status_csv(self, path):
        main.load_status_updates(path, self.status_collection, self.user_collection)
    @timeit
    def add_status(self, status_id, user_id, status_text):
        main.add_status(status_id, user_id, status_text, self.status_collection, self.user_collection)
    @timeit
    def update_status(self, status_id, user_id, status_text):
        main.update_status(status_id, user_id, status_text, self.status_collection, self.user_collection)
    @timeit
    def delete_status(self, status_id):
        main.delete_status(status_id, self.status_collection)
    @timeit
    def search_status(self, status_id):
        main.search_status(status_id, self.status_collection)

if __name__ == "__main__":
    time_code = TimeCode("TimeUserAccounts", "TimeStatusUpdates")
    user_id = "testuser"
    user_email = "testuser@gmail.com"
    user_name = "test"
    user_last_name = "user"

    time_code.add_user(user_id, user_email, user_name, user_last_name)
    time_code.update_user(user_id, "TestUser@gmail.com", "Test", "User")
    time_code.search_user(user_id)
    time_code.delete_user(user_id)

    time_code.user_collection.add_user(user_id, user_email, user_name, user_last_name)
    status_id = "testuser_001"
    status_text = "this is a test status"
    time_code.add_status(status_id, user_id, status_text)
    time_code.update_status(status_id, user_id, "this is a modified status")
    time_code.search_status(status_id)
    time_code.delete_status(status_id)

    time_code.reset_tables("TimeUserAccounts", "TimeStatusUpdates")

    # time_code = TimeCode("TimeUserAccounts", "TimeStatusUpdates")

    # time_code.load_user_csv("./accounts.csv")
    # time_code.load_status_csv("./status_updates.csv")