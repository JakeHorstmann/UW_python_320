"""
Test class to test users.py
"""

import unittest
from unittest.mock import Mock
import users

# pylint: disable=C0103


class TestUsers(unittest.TestCase):
    """
    Testing class for users.py
    """

    def setUp(self):
        """
        Method to create dummy user data used in testing
        """
        # set up dummy data used in tests below
        test_users = [users.Users("jakeh", "jakeh@uw.edu", "Jake", "H"),
                      users.Users("elizabethc", "elizabethc@uw.edu",
                                  "Elizabeth", "C"),
                      users.Users("matthewm", "matthewm@uw.edu", "Matthew", "M")]
        test_user_data = {}
        # format dictionary for the user collection tool
        for test_user in test_users:
            test_user_data[test_user.user_id] = test_user
        # create dummy user collection data
        test_data = users.UserCollection()
        test_data.database = test_user_data
        # override user collection tool to return fake data
        users.UserCollection = Mock(return_value=test_data)

    def test_UserCollect_add_valid_user(self):
        """
        Test for UserCollection's add_user method with valid user
        """
        # create test user to add to user collection
        test_id = "testuser"
        test_email = "testuser@uw.edu"
        test_name = "Test"
        test_last_name = "User"
        # create user_collection with dummy data
        user_collection = users.UserCollection()
        # add in test data
        response = user_collection.add_user(
            test_id, test_email, test_name, test_last_name)
        # assure user was added correctly
        self.assertEqual(response, True)

    def test_UserCollect_add_invalid_user(self):
        """
        Test for UserCollection's add_user method with duplicate user
        """
        # create test user to add to user collection
        test_id = "jakeh"
        test_email = "jakeh@uw.edu"
        test_name = "Jake"
        test_last_name = "H"
        # create user_collection with dummy data
        user_collection = users.UserCollection()
        # add in test data
        response = user_collection.add_user(
            test_id, test_email, test_name, test_last_name)
        # assure user was not added
        self.assertEqual(response, False)

    def test_UserCollect_modify_valid_user(self):
        """
        Test for UserCollection's modify_user method with valid user
        """
        # update jakeh id with new email and last name
        modify_id = "jakeh"
        modified_email = "jakehorstmann@uw.edu"
        modified_name = "Jake"
        modified_last_name = "Horstmann"
        # create user_collection with dummy data
        user_collection = users.UserCollection()
        # modify jakeh id
        response = user_collection.modify_user(modify_id, modified_email,
                                               modified_name, modified_last_name)
        # assure user was modified
        self.assertEqual(response, True)

    def test_UserCollect_modify_invalid_user(self):
        """
        Test for UserCollection's modify_user method with invalid user
        """
        # create bad id with data
        modify_id = "jakehorstmann"
        modified_email = "jakehorstmann@uw.edu"
        modified_name = "Jake"
        modified_last_name = "Horstmann"
        # create user_collection with dummy data
        user_collection = users.UserCollection()
        # try to modify invalid id
        response = user_collection.modify_user(modify_id, modified_email,
                                               modified_name, modified_last_name)
        # assure nothing was modified
        self.assertEqual(response, False)

    def test_UserCollect_delete_valid_user(self):
        """
        Test for UserCollection's delete_user method with valid user
        """
        # id to delete
        delete_id = "jakeh"
        # create user_collection with dummy data
        user_collection = users.UserCollection()
        # delete jakeh id
        response = user_collection.delete_user(delete_id)
        # assure user was deleted
        self.assertEqual(response, True)

    def test_UserCollect_delete_invalid_user(self):
        """
        Test for UserCollection's delete_user method with invalid user
        """
        # fake id to delete
        delete_id = "jakehorstmann"
        # create user_collection with dummy data
        user_collection = users.UserCollection()
        # try to delete id
        response = user_collection.delete_user(delete_id)
        # assure nothing was deleted
        self.assertEqual(response, False)

    def test_UserCollect_search_valid_user(self):
        """
        Test for UserCollection's search_user method with a valid user
        """
        # search for this id
        search_id = "jakeh"
        # create user_collection with fake user to search for
        user_collection = users.UserCollection()
        # search for user with search_id
        response = user_collection.search_user(search_id)
        # assure user was found
        self.assertEqual(response.user_id, search_id)

    def test_UserCollect_search_invalid_user(self):
        """
        Test for UserCollection's search_user method with an invalid user
        """
        # try to search for this id
        search_id = "jakehorstmann"
        # create user_collection with fake user to search for
        user_collection = users.UserCollection()
        # search for user with search_id
        response = user_collection.search_user(search_id)
        # assure user was not found
        self.assertEqual(response.user_id, None)
