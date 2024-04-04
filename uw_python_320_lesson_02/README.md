# Introduction #

To be able to quickly test the code from lesson 1 manually, a new file was created, ``menu.py``, which allows exercising all basic functionality in ``main.py``. However, it was coded in such a rush that there are several bugs that have to be fixed before it can be used. Once that is done, we need to implement logging functionality on two of the files in the project.

# What you need to do #

1. Make sure you can complete all the steps outlined in "Testing ``menu.py``" below.
This will not be as easy as it sounds.
The code **HAS** errors that you will need to debug and fix.
You can use *PDB*, *Pysnooper* or any other debugging techniques you like.
**Make sure you capture your findings** in a file called
``debugging_notes.md`` (same markup format used for this README file). This file **must** be submitted with the rest of your work.

1. Implement logging capabilities on ``users.py`` and ``user_status.py``:
    1. You can use the standard Python logger or Loguru.
    1. Both ``users.py`` and ``user_status.py`` will share a **single log file** per session.
    1. **Each class method** should have **at least one** log info message. For example, "New status collection instance created".
    1. Within each method, you should have **one log error message** before the method returns ``False``.
    1. You can also add logging to ``main.py`` and ``menu.py``, but it is not a requirement.

## Testing ``menu.py`` ##

1. Load the users database.
1. Add a new user and confirm you get a success message.
1. Try to add the same user ID again and confirm you get an error message.
1. Update the name of an existing user.
1. Try to update the name of a non-existing user and confirm you get an error message.
1. Search for an existing user and return that user's email, name and last name.
1. Search for a non-existing user and return a message indicating that the user does not exist.
1. Delete an existing user.
1. Try to delete a non-existing user and confirm you get an error message.
1. Save the users database.
1. Load the status database.
1. Add a new status and confirm you get a success message.
1. Try to add the same status ID again and confirm you get an error message.
1. Update the text of an existing status ID.
1. Try to update the text of a non-existing status ID and confirm you get an error message.
1. Search for an existing status ID and return the ID of the user that created the status and the status text.
1. Search for a non-existing status ID and return a message indicating that the status ID does not exist.
1. Delete an existing status.
1. Try to delete a non-existing status and confirm you get an error message.
1. Save the status database.
1. Make sure menu options are case-insensitive (i.e., typing "a" or "A" works in the same way).

# Other requirements #

* Log filename: Each time you launch ``menu.py``, it will create a file called ``log_mm_dd_yyyy.log`` which will reflect the date on which the server is being launched, for example: ``log_10_22_2020.log``. If there is already a file with that name, your log messages will be appended to it (i.e., the existing log file will not be overwritten). Your log name can include additional information (for example, time at which it was launched).
* PEP8 compliance: Your code will need to pass Pylint with 10 out of 10. As before, a custom .pylintrc file or Pylint disable comments directly on main.py can be used.
	
# Tips #

* If you use loguru for logging, enter all your ``logger.add()`` statements for logfile creation in ``menu.py``. That will make it possible for all other files to share the same logfile.

# Submission #

The following files need to be submitted:

* ``menu.py``
* ``main.py`` (Your starting code should be the file you modified for assignment 1).
* ``users.py`` (Your starting code should be the file you used for assignment 1).
* ``user_status.py`` (Your starting code should be the file you used for assignment 1).
* ``debugging_notes.md``.
* ``.pylintrc`` (if using custom rules).

# How will your code be evaluated? #

The instructor will do the following:

1. Check that all errors in ``menu.py`` were corrected.
1. Check that a single log file is created with each run and that logging messages are being generated from both ``users.py`` and ``user_status.py``.
1. Run Pylint to verify PEP8 compliance.
