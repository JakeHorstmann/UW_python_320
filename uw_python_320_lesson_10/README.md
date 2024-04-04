
# Lesson 10

# Introduction

The requirements for this assignment are fairly straightforward: we are going to build an API to the application from lesson 9. This API will do three things. Firstly, it will list all of the users details and their status information. Secondly, it will list all of the users with their image details. Finally, it will list any occurrences where the database record of the images is out of sync with the files on disk. This sync check is necessary in case anyone should copy images into the folders outside of the application. We can then report upon the differences.

We are going to build a web interface that uses an API to return a JSON data structure that contains all of the data in the user table, and all of the data in the image table. It will also return the results of calling the `list_user_images` function. The web interface will display the raw JSON data. It does not need to be formatted.


# What to do
1. You will be using Flask to build the web API.
1. The user details will be at a `users` url.
1. The image details will be at an `images` url.
1. The differences will be at a `differences` url.
1. If there is no data to show, be sure to include an empty json structure in your response. No error message is necessary.
2. You will build the web application that serves the data from your application at these urls.
3. You will use the provided database, your files from lesson 9, and the following Flask and sqlalchemy packages (that you will need to install):
   1. `pip install flask`
   2. `pip install flask-restful`
   3. `pip install sqlalchemy`

# Submission

The following files need to be submitted:

## New files
* `api.py`: Your flask API

## Files from lesson 9 (please resubmit)

All the files you need for your solution -- likely:

* `main.py`
* `menu.py`
* `user_status.py`
* `users.py`
* `test_main.py`
* `list_user_images.py`

Any other files required by your implementation of this assignment.


# Other requirements
1. Your code must run from a browser that accesses the default Flask IP address and port.

1. You will use the same data as used for assignment 9.

# How will your code be evaluated?

* The instructor will delete any .db files and image directories included in the submission. This is to make sure your code can create and initialize a database file from scratch.
* The instructor will run `menu.py` and load sample CSV files into your SQL database, as before.
* The instructor will run `api.py` and will access the specified urls to verify that the correct data is returned.
* The instructor will look at your code and verify that all operations are being performed directly in the SQL database.

As usual, your code will need to be linted and score 10/10 on pylint.

# Tips

1. To keep things as straightforward as possible, be sure to use the Flask defaults for ip address and ports.

2. Consider how you will test your web API. Implement a realistic set of tests. Flask comes with a test framework:

https://flask.palletsprojects.com/en/2.0.x/testing/


