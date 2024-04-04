import time
import main, users, user_status
from peewee import SqliteDatabase
from socialnetwork_model import UserModel, StatusModel


class TimeCode:
    def __init__(self, sqlite_db_name):
        # set up sqlite database
        sqlite_db = SqliteDatabase(sqlite_db_name)
        self.sqlite_db = sqlite_db
        self.user_collection = users.UserCollection(sqlite_db)
        self.status_collection = user_status.UserStatusCollection(sqlite_db)

    def timeit(method):
        def timed(*args, **kwargs):
            start = time.time()
            result = method(*args, **kwargs)
            end = time.time()
            total_time = round((end - start) * 1000000, 2)
            print(f"Total time for {method.__name__} was {total_time} microseconds")
            return result
        return timed


    def reset_tables(self):
        self.sqlite_db.drop_tables([UserModel, StatusModel])
    @timeit
    def add_user(self, user_id, user_email, user_name, user_last_name):
        main.add_user(user_id, user_email, user_name, user_last_name, self.user_collection)
    @timeit
    def update_user(self, user_id, user_email, user_name, user_last_name):
        main.update_user(user_id, user_email, user_name, user_last_name, self.user_collection)
    @timeit
    def delete_user(self, user_id):
        main.delete_user(user_id, self.user_collection)
    @timeit
    def search_user(self, user_id):
        main.search_user(user_id, self.user_collection)

    @timeit
    def load_user_csv(self, path):
        main.load_users(path, self.user_collection)

    @timeit
    def load_status_csv(self, path):
        main.load_status_updates(path, self.status_collection)
    @timeit
    def add_status(self, status_id, user_id, status_text):
        main.add_status(status_id, user_id, status_text, self.status_collection)
    @timeit
    def update_status(self, status_id, user_id, status_text):
        main.update_status(status_id, user_id, status_text, self.status_collection)
    @timeit
    def delete_status(self, status_id):
        main.delete_status(status_id, self.status_collection)

    @timeit
    def search_status(self, status_id):
        main.search_status(status_id, self.status_collection)


if __name__ == "__main__":
    time_code = TimeCode("database.db")
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

    # time_code.load_user_csv("./accounts.csv")
    # time_code.load_status_csv("./status_updates.csv")

    time_code.reset_tables()
    
    # ## used to try and average out the results
    # iterations = 10000
    # i = 0
    # add_user_time = 0
    # update_user_time = 0
    # search_user_time = 0
    # delete_user_time = 0
    # add_status_time = 0
    # update_status_time = 0
    # search_status_time = 0
    # delete_status_time = 0

    # while i < iterations:
    #     add_user_time += time_code.add_user(user_id, user_email, user_name, user_last_name)
    #     update_user_time += time_code.update_user(user_id, "TestUser@gmail.com", "Test", "User")
    #     search_user_time += time_code.search_user(user_id)
    #     delete_user_time += time_code.delete_user(user_id)

    #     time_code.user_collection.add_user(user_id, user_email, user_name, user_last_name)
    #     status_id = "testuser_001"
    #     status_text = "this is a test status"
    #     add_status_time += time_code.add_status(status_id, user_id, status_text)
    #     update_status_time += time_code.update_status(status_id, user_id, "this is a modified status")
    #     search_status_time += time_code.search_status(status_id)
    #     delete_status_time += time_code.delete_status(status_id)



