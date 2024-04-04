# Introduction

Now that our social networking project is up and running and setup with a SQL database, we will try to add some functionality to it, using what we have learned about list comprehension, generators and iterators.

# Part 1: Status update generator/iterator

1. Within ``UserStatusCollection`` in ``user_status.py``, you will create a new method called ``search_all_status_updates`` that will take a user ID and return all status updates for that user.
1. Within ``main.py``, you will create a new function, also called ``search_all_status_updates`` which will take a user ID and the corresponding pointer to ``status_collection``. This function will serve as a proxy for ``menu.py`` to access this new functionality.
1. Create a new function in ``menu.py``, called ``search_all_status_updates``. This function will ask for a user ID and call the corresponding function in ``main.py``. The results from the query will be turned into a generator (you can create a new function in ``menu.py`` for that, called ``status_generator``). Then, it will report how many status updates were found for that user and will repeatedly offer to show the next status update (hence the need for a generator), print it out if the answer is yes and return to the main menu if the answer is no. The generator will raise a ``StopIteration`` exception if it reaches the end of the query, you will need to handle that exception (as usual, no bare exceptions!), print a message on screen that this was the last update and go back to the main menu. ``search_status_updates`` will produce an output similar to this:

```
Enter user ID: ldconejo79
A total 2 status updates found for ldconejo79 
Would you like to see the next update? (Y/N): y
Great game today!
Would you like to see the next update? (Y/N): y
My team was eliminated. Again :-(
Would you like to see the next update? (Y/N): y
INFO: You have reached the last update
```
You can also choose to simply turn the query results directly into an iterator (using ``iter()``), in which case you would not need ``status_generator``.

In general, remember that ``menu.py`` is more like a placeholder for a web-based user interface, which is one of the reasons why it only interacts with ``main.py``. In this way, once you are ready to work on a web interface, you can have the new interface interact with ``main.py`` with minimal to no changes to ``main.py``, ``users.py`` and ``user_status.py``.

# Part 2: Using Iterator in SQL Query / List comprehension for searching status by search string

We want to implement the capability to identify status updates matching a search string, list, and potentially delete them.  Here is what you need to do:

1. Create a new method in ``UserStatusCollection``, called ``filter_status_by_string``.
    * The method will take a single input parameter, a string containing either a word or phrase to be searched within **all status updates from all users** in the database. 
    * The method will query your database for any status updates matching the string. 
    * For example, if the search string is "beautiful day", a status update where *status_text* is "It's a beautiful day today" will become a match.
    * To avoid the risk of the query resulting in too many results in a large database and therefore compromising system memory, you need to make sure that your query returns an iterator, so that it only holds one result at a time. Here is an example that you can use as a reference:

    ```
    query = UsersTable.select().where(UsersTable.user_location.contains('Seattle')).iterator()
    next_result = next(query)
    print(f"User: {next_result.user_name}")
    ```
    * You will need to adjust your query to search the Status table for status updates with status text that *contains* the search string.
    * Return *query*, letting ``main.py`` and ``menu.py`` work the iterator.

1. Create a function in ``main.py`` to access ``filter_status_by_string`` and return the query to ``menu.py``
1. In ``menu.py``, create a function also called ``filter_status_by_string``.
    * This function will ask the user for the string to search and call the corresponding function in ``main.py``.
    * It will iterate through each status update returned by the query, asking the user if they want to see the next result and asking if they want to delete the current result. The output will be something like this:

    ```
    Enter the string to search: existence
    Review the next status? (Y/N): y
    thinkable existence hug aback sky
    Delete this status? (Y/N): n
    Review the next status? (Y/N): y
    stormy existence remind encouraging cough
    Delete this status? (Y/N): 
    ```
    * Make sure you also add the corresponding menu option, called *Search all status updates matching a string*.
1. Also in ``menu.py``, create a function called ``flagged_status_updates``.
    * This function will also ask the user for a string to search.
    * It will then call ``filter_status_by_string`` in ``main.py``.
    * Finally, it will take the returning query and **using list comprehension** return and print a list of tuples showing all results. The output should be something like this:

    ```
    Enter the string to search: existence
    ('Isabel.Avivah34_27', 'thinkable existence hug aback sky')
    ('Brigitta.Balsam57_143', 'stormy existence remind encouraging cough')
    ('Adelaida.Pearman53_377', 'troubled existence deal parsimonious blade')
    ('Cora.Zarger49_922', 'rich wilderness leave foolish existence')
    ("Binny.O'Connell43_537", 'crowded existence carry obtainable spade')
    ('Lonnie.Fielding48_697', 'wee step conceptualize beautiful existence')
    ('Talya.Demb61_9', 'rustic existence cough entertaining rest')
    ('Joanna.Hughett86_387', 'naughty basketball carve hurt existence')
    ('Audrie.Morris67_110', 'afraid eye weep icky existence')
    ```

    * As before, make sure you add the corresponding menu option, *Show all flagged status updates*.

# How will your code be evaluated?

1. Any .db files included in your submission will be deleted to ensure your code can initialize the database from scratch. (again, they should not be commited to git anyway)
1. A sample set of 1,000 user accounts and 100,000 status updates will be loaded into your database from CSV files, using the capability developed in lesson 3.
1. The instructor will verify both new menu options, including verifying that search results marked for deletion are indeed deleted.
1. The instructor will look at the code to verify the use of the corresponding constructs (generator, iterator and list comprehension).
1. PEP8 compliance will be checked as usual, using Pylint; the expectation is for your code to score 10 out of 10 (using a custom ``.pylintrc`` or Pylint disable statements is acceptable within reason).
1. You do not need to develop unit testing for this assignment.

# Tips

* For part 1, you will need to query *StatusTable* (or the SQL table name you used for status updates), filtering by user ID. Your query should look similar to this

```
query = StatusTable.select().where(StatusTable.user_id == target_user_id)
```
* For Part 1, the long route to delete a status update would be to use the status ID and call ``delete_status()`` in ``main.py``. The short route would be to call the ``delete_instance()`` method directly on the corresponding query result.
* Remember, **DO NOT** use bare exceptions. When working with iterators and generators, you will run into a ``StopIteration`` exception at the end, it should be easy to add exception handling for it.
