# Introduction

For this assignment, your starting point will be your completed code from the end of lesson 2:

* main.py
* menu.py
* user_status.py
* users.py

You are also given a version of ``accounts.csv`` and ``status_updates.csv`` with 1,000 and 100,000 records, respectively.

The goal is easier to state than to implement: Once again, you need to migrate from using CSV files to storing your data into a database, this time, into MongoDB (non-relational).

If you want to try generating your own source data, you can use the following Github repository as a reference: https://github.com/ldconejo/social_network_generator

# What you need to do

1. Implement a MongoDB database that will contain both user account and well as user status data:
    * Create one collection called ``UserAccounts``.
    * Create another collection called ``StatusUpdates``.

1. Your code should make sure that some basic rules are followed:
    * No duplicated ``UserID`` or ``StatusID``.
    * Every status update should be associated to a particular user that **exists**.
    * If a user is deleted, all associated status updates should be deleted as well.

1. Modify ``UserStatusCollection`` to work with MongoDB. This means that **every operation** (add, modify, delete, search) needs to interact with the database.

1. Update the feature to load the CSV files for users and user status to populate your MongoDB database. Remove the features to save to CSV files, as the data will be stored in your database.

# Submission #

At least the following files need to be submitted:

* ``main.py``
* ``menu.py``
* ``user_status.py``
* ``users.py``
* ``test_main.py``

Any other files required by your implementation of this assignment (including data and test files!).

# How will your code be evaluated?

* The instructor will run ``menu.py`` and load the sample CSV files into your database.
* The instructor will interact with your database using the user interface in ``menu.py`` and try to add, modify, search and delete data.
* The instructor would also try common error conditions: Adding a duplicated user_id, deleting a non-existing user, etc. Your code should not crash due to these errors and please, no bare exceptions.
* The instructor will look at your code and verify that all operations are being performed directly on the database.

As usual, your code will need to be linted and score 10/10 on Pylint.

## notes on testing / CI

In order for your tests to run, you need to have mongodb running.

The CI (gitHub Actions) is set up to use this command to start mongo:

`mongod -f mongo_config_dev.yml`

That will configure mongo to use the configuration in the `mongo_config_dev.yml`.

Take a look at the `.yml` file, it's pretty self explanatory, but the key bits are:

The files Mongo creates will go in the ``mongo_files`` dir.

The server will be listening on localhost, and port number
27017 (which is the default for mongo)

To be consistent, you should use the same config (same command), and this command to start the pymongo client:

`client = MongoClient(host='localhost', port=27017)`

MongoDB allows more than one database at a time -- so you can use one a different one for testing than for operational use. That way your tests won't mess up your real data.

If you have any other requirements than loguru and pymongo, they should be added to the ``requirements.txt`` file.


# Tips

* To get MongoDB to use ``user_id`` and ``status_id`` as primary keys for your users and user status collections, use those values as the ``_id`` field for the entries into your collections.

* ``pymongo`` has several exceptions that could be useful for your error handling. One example is ``pymongo.errors.DuplicateKeyError``. You should probably import that into both ``users.py`` and ``user_status.py``.

* The ``update_one`` and ``delete_one`` methods return ``True`` even if the associated record does not exist. You will need to verify first and return the corresponding error message if an update or deletion is attempted on a non-existing record.

* Enable all operations (add, modify, search and delete) for users first, the process to do the same for the status collections will be very similar.

* Before adding a new status ID, remember to check that the corresponding user ID exists.

* It is always a good idea to write tests for your code. Try to use TDD, and attempt to reach 100% coverage.



