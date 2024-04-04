# Lesson 8
# Introduction

Object-oriented languages are excellent for handling "things" (also know as classes!). Adding new things is relatively easy. But as more and more new things are added testing can become very complex, and the speed of change slows.

If you have a system with few things, but need to potentially add a lot of logic over time (but not new things), functional programming can excel. And functional programs, when well written, are easy to test.

With our social media application, the things are really well defined and stable. We are probably only ever going to have users, messages, and maybe a couple of others, for a very long time. To help facilitate easier growth and expansion of the application, and to reduce testing time, it has been decided to rewrite the system to use a functional approach.

After some investigation, you have found that PeeWee now supports an extension that should allow a more functional approach to interfacing to a database for Python. Its is called DataSet, and its documentation is at docs.peewee-orm.com/en/latest/peewee/playhouse.html#dataset

With this in mind, you are going to embark on a project to rewrite your database code from assignment 3, now using a functional approach. All of the material in this lesson should help you to do this.

Your starting point will be the code you finished on Assignment 3. And you can use the same data you used in lesson 3 too (unless you prefer to generate some new data).


# What to do
1. Familiarize yourself with DataSet: docs.peewee-orm.com/en/latest/peewee/playhouse.html#dataset

1. Using the database you created in lesson 3, and your newly acquired knowledge of functional programming, identify the relevant functional concepts you will use to structure your code for this assignment:
   - consider which constructs you will use to replace classes.
   - determine how you will code the database access
   - identify how the code will be organized so that it is clear and easy to understand

1. Using your analysis form the preceding step, start to code your functional solution.

1. Decide how you will best be able to use unit tests. Can you use your unit tests from lesson 3? Will they need to be amended?

1. Your application should be robust: make sure you add all appropriate error handling and logging that is needed.

For reference, here are the steps from lesson 3 that you should use in this assignment as you rewrite the code:

1. Reuse the lesson 3 SQL database that contains both user account and well as user status data:

* Implement your database model in a separate file, ``socialnetwork_model.py``.
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

The fact that ``UserID`` will be a foreign key in the ``Status`` table means that you cannot add a status for a user that does not exist in the ``Users`` table.

1. ``UserStatusCollection`` will have **every operation** (add, modify, delete, search) needed to interact with the database. This means no dumping the entire database into a dictionary!

2. Reimplement the feature to load the CSV files for users and user status to populate your SQL database.

3. Your database needs to be setup so that erasing a user from the ``Users`` table will cause all status updates from that user in the ``Status`` table to be deleted. Naturally, a new status update cannot be created for a user that does not exist.

4. Ensure you can run unit tests for the code on ``users.py`` and ``user_status.py``. Test coverage should be at at 100% for each of the two files.

# Submission #

The following files need to be submitted:

* ``main.py``
* ``menu.py``
* ``user_status.py``
* ``users.py``
* ``test_main.py``.

Any other files required by your implementation of this assignment.

# Other requirements

* Your code needs to be able to create a new database file and the corresponding tables if one does not exist.
* For testing, if your test database does not run from memory, you will need to add code to delete the .db file that is created after every test run.


# How will your code be evaluated?

* The instructor will delete any .db files included in the submission. This is to make sure your code can create and initialize a database file from scratch.
* The instructor will run ``menu.py`` and load sample CSV files into your SQL database. A SQL database inspector will be use to look at the table structure of your database, verify that the correct fields have been set as primary keys in each table, as well as that ``UserID`` has been set as foreign key in the ``Status`` table.
* The instructor will interact with your database using the user interface in ``menu.py`` and try to add, modify, search and delete data, checking that this is also reflecting in the database file.
* The instructor would also try common error conditions: Adding a duplicated user_id, deleting a non-existing user, etc. Your code should not crash due to these errors and please, no bare exceptions (most database errors will be ``IntegrityError`` exceptions).
* The instructor will look at your code and verify that all operations are being performed directly in the SQL database.

As usual, your code will need to be linted and score 10/10 on Pylint.

# Tips

1. Study the API for DataSet carefully and understand how you can use it in a functional programming style.

1. Carefully consider which functional constructs you will use to replace classes. Will closures help? Will currying offer any benefits to this solution? What is the best way to organize your functions?

1. Consider starting this assignment using your completed lesson 3 assignment, and gradually reworking the code from an object oriented to a functional approach.

1. You will need to remove and replace all classes.

1. Rebuild your code incrementally. Start simple, with the most common case, and add corner cases as you go.

1. Use unit testing as early as possible in your development work.

1. Use Python code to enforce string length constraints for the different fields.

1. ``DataSet`` includes a ``create_index`` method within its ``Table`` class, which you can use to implement unique value constraints for ``user_id`` and ``status_id``. Read ``Using create_index()`` below for some additional steps required.

1. ``DataSet`` does not have specific functionality for implementing foreign key constraints. One option to consider when adding a new status update, is to try to add the associated ``user_id``  to the ``Users`` table, which should raise a ``peewee.IntegrityError`` exception. You can trap the exception and handle it by adding the status update (since you know the status is associated to a valid ``user_id``). For example:

```
try:
    Users.insert(user_id=#USER_ID FROM THE STATUS UPDATE)
# If an IntegrityError exception is raised, the foreign 
# constraint has been satisfied
except peewee.IntegrityError:
    Status.insert(#NEW STATUS UPDATE GOES HERE)
```
# Using create_index()

The ``peewee`` module has a bug that was reported and fixed here:

https://github.com/coleifer/peewee/issues/2319 

As of the time of this writing, the fix is not yet part of the ``peewee`` module that is installed using ``pip``. However, you can install it directly from Github (yes, you will hopefully be learning something new if you try this) by doing the following:

1. Uninstall ``peewee``:
```
python -m pip uninstall peewee
```

2. Install ``peewee`` directly from its master Github repository (do this in a separate folder, not within your assignment's folder):
```
git clone https://github.com/coleifer/peewee.git
cd peewee
python setup.py install
```
3. You can safely delete the ``peewee`` directory created in the previous step after installing. It is not needed anymore and it should not be part of the pull request for your assignment.

4. ``create_index()`` requires that the column you're trying to make unique already exists, so you will need to create a dummy record first, use ``create_index()`` to make the desired column(s) unique and then delete the dummy record. Here is an example:

```
from playhouse.dataset import DataSet

ds = DataSet('sqlite:///socialnetwork.db')

Users = ds["UsersTable"]

# Create a dummy record to have a 'user_id' column
# before making the column unique with 'create_index()'.
Users.insert(user_id='test')
Users.create_index(['user_id'], unique=True)
# Delete the dummy record afterwards.
Users.delete(user_id='test')

# Some sample add operations
Users.insert(user_id='atumble', user_name='Aldus', user_last_name='Tumbledoor', user_email='atumbled@uw.edu')
# The next insert will fail because of the UNIQUE constraint
Users.insert(user_id='atumble', user_name='Aldus', user_last_name='Tumbledoors', user_email='taldus2@uw.edu')
```
