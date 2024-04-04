# docker run --name mongodb -p 27017:27017 -p 27018:27017 -d mongo:latest
from unittest.mock import patch
import main
import menu
import time
import csv

def test_user_multiprocess_load():
    file = "accounts.csv"
    with patch("builtins.input", return_value = file):
        menu.load_users_multiprocess()

def test_status_multiprocess_load():
    mock_file = "status_updates.csv"
    with patch("builtins.input", return_value = mock_file):
        menu.load_status_updates_multiprocess()

def test_user_load():
    file = "accounts.csv"
    user_collection = main.init_user_collection("localhost", 27017, "database")
    main.load_users(file, user_collection, batch_size = 128)

def test_status_load():
    file = "status_updates.csv"
    user_collection = main.init_user_collection("localhost", 27017, "database")
    status_collection = main.init_status_collection("localhost", 27017, "database")
    main.load_status_updates(file, status_collection, user_collection, batch_size = 128)

if __name__ == "__main__":
    db = "database"
    tables = ["UserAccounts", "StatusUpdates"]
    iterations = 10
    # wipe initial databases
    main.nuke_databases(db, tables)
    # set up functions to test
    test_functions = {"mp":{"user": test_user_multiprocess_load,
                      "status": test_status_multiprocess_load},
                      "regular": {"user": test_user_load,
                      "status": test_status_load}}
    # test functions
    for iteration in range(iterations):
        for key, functions in test_functions.items():
            # tests the user function
            user_fun = functions["user"]
            status_fun = functions["status"]
            start_time = time.time()
            user_fun()
            end_time = time.time()
            delta_user = end_time - start_time
            # tests the status function
            start_time = time.time()
            status_fun()
            end_time = time.time()
            delta_status = end_time - start_time
            # clears databases for the next test
            main.nuke_databases(db, tables)
            # write data to a csv file with times
            with open("results.csv", "a", newline = "") as csvfile:
                field_names = ["function", "iteration", "time"]
                writer = csv.DictWriter(csvfile, fieldnames = field_names, delimiter = ",")
                writer.writerow({"function": f"{key}_user",
                                "iteration": iteration,
                                "time": delta_user})
                writer.writerow({"function": f"{key}_status",
                                "iteration": iteration,
                                "time": delta_status})