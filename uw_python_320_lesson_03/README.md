# Introduction

It turns out storing all information from your social network in a CSV file is not very efficient. The goal of this assignment is to migrate to a SQL database without losing or changing any existing functionality (i.e., all user-accessible functions will still  take the same input parameters and return the same type of values).

Your starting point will be the code you finished in Assignment 2, including logging capabilities as well as the simplified user interface in ``menu.py``.

We are also providing you with a much larger set of data in both ``accounts.csv`` and ``status_updates.csv``. This data has been generated automatically, so do not expect the status updates to make much sense! It contains 1,000 user accounts and 100,000 status updates.

If you want to try generating your own source data, you can use the following Github repository as a reference:

https://github.com/ldconejo/social_network_generator

# What you need to do

1. Implement a SQL database using the PeeWee ORM that will contain both user account and well as user status data:

* Implement your database model in a separate file, ``socialnetwork_model.py``

* The database will have two tables: ``Users`` and ``Status``.
* The ``Users`` table will have the following fields:
    * user_id (Primary Key, limited to 30 characters).
    * user_name (Limited to 30 characters).
    * user_last_name (Limited to 100 characters).
    * user_email.
* The ``Status`` table will have these fields:
    * status_id (Primary Key).
    * user_id (Foreign Key from the ``Users`` table).
    * status_text.

The fact that *UserID* will be a foreign key in the *Status* table means that you cannot add a status for a user that does not exist in the ``Users`` table.

1. Modify ``UserCollection``  and ``UserStatusCollection`` to work with your new SQL database. This means that **every operation** (add, modify, delete, search) needs to interact with the database. This means no dumping the entire database into a dictionary!

1. Update the feature to load the CSV files for users and user status to populate your SQL database. Remove the feature to save to CSV files, as the data will from now on be stored in your SQL database.

1. Your database needs to be setup so that erasing a user from the ``Users`` table will cause all status updates from that user in the *Status* table to be deleted. Naturally, a new status update cannot be created for a user that does not exist.

1. Create unit testing for the code on ``users.py`` and ``user_status.py``. Test coverage should be at at 100% for each of the two files.

1. Update your ``main.py`` (and ``test_main.py``) files to work with your new ``UserCollection`` and ``UserStatusCollection`` classes.

**Note:** Any code in main.py that worked directly with the ``.database`` dictionaries will need to be updated. On the plus side, you no longer need the code that dumps the csv files.


# Submission #

The following files need to be submitted:

* ``main.py``
* ``test_main.py``
* ``menu.py``
* ``user_status.py``
* ``test_user_status.py``
* ``users.py``
* ``test_users.py``
* ``socialnetwork_model.py``

Any other files required by your implementation of this assignment.

# Other requirements

* Your code needs to be able to create a new database file and the corresponding tables if one does not exist.

* For testing, if your test database does not run from memory, you will need to add code to delete the ``.db`` file that is created after every test run.
NOTE: Fixtures can be relly helpful here!

* Do not commit any temporary ``.db`` files to git!

# How will your code be evaluated?

* The instructor will delete any .db files included in the submission. This is to make sure your code can create and initialize a database file from scratch. (they should not be in git in the first place)
* The instructor will run ``menu.py`` and load sample CSV files into your SQL database. A SQL database inspector will be use to look at the table structure of your database, verify that the correct fields have been set as primary keys in each table, as well as that *UserID* has been set as foreign key in the *Status* table.
* The instructor will interact with your database using the user interface in ``menu.py`` and try to add, modify, search and delete data, checking that this is also reflected in the database file.
* The instructor will also try common error conditions: Adding a duplicated user_id, deleting a non-existing user, etc. Your code should not crash due to these errors and please, no bare exceptions (most database errors will be ``IntegrityError`` exceptions).
* The instructor will look at your code and verify that all operations are being performed directly in the SQL database.

As usual, your code will need to be linted and score 10/10 on Pylint.

# Tips

* Note that although Peewee will let you use *max_length*, SQLite will not truncate or raise an exception if you exceed the limit. You will either need to use constraints while defining fields that have such limitations
(``constraints=[peewee.Check("LENGTH(user_id) < 30")]``) or check for those limits outside of Peewee (for example, by having your code check the size of the user ID that has been entered).
* The ``Users`` and ``UserStatus`` classes may not be required anymore. You might be able to delete that code.
* Remember tests run in alphabetical order, so ``test_new_user`` would run **after** ``test_delete_user``, which could cause some issues. Be sure to use fixtures and/or mocking, to keep your tests independent.
* Try to use unique names for your tables in the database, to avoid conflicts with your existing classes. For example, name them *UsersTable* and *StatusTable*.
* Try to get some basic functionality first. For example, get your code to create the database, initialize tables and enable the *Add user* menu function. Use a database inspector (several *freeware* options are available) to check that the new entry has been created. Once this is working try to optimize for the remaining features.
* Pass a reference to the database when you initialize *UserCollection* and ``UserStatusCollection``, that way all methods within your classes can refer to the database that was passed during init.
* Make use of appropriate exception types, such as ``DoesNotExist`` for records not found in the database. ``Peewee.IntegrityError`` will be triggered when trying to add a duplicated user or status update.
* Add additional logging messages to the code as required.
* Using ``on_delete='CASCADE'`` parameter when setting up the foreign key in the *Status* table will take care of any status updates from a user that is being deleted.
* For unit testing, load your database in memory (you might need to change ``socialnetwork_model.py`` to work in memory as well), so that you do not need to delete the database file after every test run. You can do that by instantiating your database with this command:

```
database = SqliteDatabase(':memory:')
```

* When implementing your database in memory for testing purposes, remember that the moment your close the connection, all your data and tables will be lost, so your tests will need to create those tables again. If using ``unittest``, you can use the ``setUp`` and ``tearDown`` for these purposes.
 If using ``pytest``, test fixtures work great as well.

# Configuring the CI (gitHub actions)

The CI is set up to lint, test, and check test coverage on your code.

It may work by default, but you may need to make some changes to customize it for your specific project.

### Adding requirements

The CI should be set up with known requirements (e.g. peewee), but if you need other third-party pacakges, you can add them to the ``requirements.py`` file.

### Configuring the coverage report

Exactly how coverage is run can be configured by editing the ``.coveragerc`` file. See the coverage docs for details:

https://coverage.readthedocs.io/en/6.3/config.html

The most likely thing you will need to do is exclude files. For instance, if you don't have tests for the menu.py file, you can put this in .coveragerc:

```
# .coveragerc to control how coverage is run.
[run]
omit = menu.py
```

If you have more files to omit, then they can go on the next lines:

```
# .coveragerc to control how coverage is run.
[run]
omit = menu.py
       users.py
```
 etc.

 **Do not disable coverage for files that you are supposed to be testing!**




