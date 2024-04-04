"""
Test class to test main.py
"""

import unittest
from unittest.mock import Mock, patch
import main
import user_status
import users

# pylint: disable=C0103

class TestMain(unittest.TestCase):
    """
    Testing class for main.py
    """
    def setUp(self):
        """
        Set up functions with some dummy user and user_status data for testing
        """
        # pylint: disable=C0301
        # get backups
        self.backup_user_collection = users.UserCollection
        self.backup_user_status_collection = user_status.UserStatusCollection
        # set up dummy csv data used in tests below
        self.test_user_csv_data = ({"USER_ID": "jakeh", "EMAIL": "jakeh@uw.edu", "NAME": "Jake", "LASTNAME": "H"},
                     {"USER_ID": "elizabethc", "EMAIL": "elizabethc@uw.edu", "NAME": "Elizabeth", "LASTNAME": "C"},
                     {"USER_ID": "matthewm", "EMAIL": "matthewm@uw.edu", "NAME": "Matthew", "LASTNAME": "M"})
        self.test_status_csv_data = ({"STATUS_ID":"jakeh_00001", "USER_ID": "jakeh", "STATUS_TEXT": "Working through Python 320 tests"},
                     {"STATUS_ID":"elizabethc_00001", "USER_ID": "elizabethc", "STATUS_TEXT": "Just got Jake some donuts!"},
                     {"STATUS_ID":"matthewm_00001", "USER_ID": "matthewm", "STATUS_TEXT": "I'm making the best movie called Interstellar"})
        # set up dummy data used in tests below
        test_users = [users.Users("jakeh", "jakeh@uw.edu", "Jake", "H"),
            users.Users("elizabethc", "elizabethc@uw.edu", "Elizabeth", "C"),
            users.Users("matthewm", "matthewm@uw.edu", "Matthew", "M")]
        test_user_data = {}
        # format dictionary for the user collection tool
        for test_user in test_users:
            test_user_data[test_user.user_id] = test_user
        # create dummy user collection data
        test_data = users.UserCollection()
        test_data.database = test_user_data
        # override user collection tool to return fake data
        users.UserCollection = Mock(return_value = test_data)
        self.user_collection = users.UserCollection

        # set up dummy status data used in tests below
        test_user_status = [user_status.UserStatus("jakeh_00001", "jakeh", "Working through Python 320 tests"),
            user_status.UserStatus("elizabethc_00001", "elizabethc", "Just got Jake some donuts!"),
            user_status.UserStatus("matthewm_00001", "matthewm_00001", "I'm making the best movie called Interstellar"),
            user_status.UserStatus("jakeh_00002", "jakeh", "Struggling through Python 320 tests..."),
            user_status.UserStatus("jakeh_00003", "jakeh", "Made it through Python 320 tests!")]
        test_user_status_data = {}
        # format dictionary for the user status tool
        for test_status in test_user_status:
            test_user_status_data[test_status.status_id] = test_status
        # create dummy user status data
        test_data = user_status.UserStatusCollection()
        test_data.database = test_user_status_data
        # override user status collection tool to return fake data
        user_status.UserStatusCollection = Mock(return_value = test_data)
        self.user_status_collection = user_status.UserStatusCollection

    def tearDown(self):
        # set backups back to original
        users.UserCollection = self.backup_user_collection
        user_status.UserStatusCollection = self.backup_user_status_collection

    def test_init_user_collection(self):
        """
        Test for main's init_user_collection function
        """
        # replace the user collection with a test value
        with patch("users.UserCollection", return_value = "test"):
            # call init_user_collection to return fake data
            response = main.init_user_collection()
            # make sure it matches test response
            self.assertEqual("test", response)

    def test_init_status_collection(self):
        """
        Test for main's init_status_collection function
        """
        # replace the status collection with a test value
        with patch("user_status.UserStatusCollection", return_value = "test"):
            # call init_user_collection to return fake data
            response = main.init_status_collection()
            # make sure it matches test response
            self.assertEqual("test", response)

    def test_load_users(self):
        """
        Test for main's load_users function
        """
        # replace dict reader with fake data
        main.csv.DictReader = Mock(return_value = self.test_user_csv_data)
        # replace open so that it does not error out when called with fake file
        with patch("builtins.open", create=True):
            response = main.load_users("foo", users.UserCollection())
            self.assertEqual(True, response)


    def test_save_users(self):
        """
        Test for main's save_users function
        """
        # replace open so that it does not error out when called with fake file
        with patch("builtins.open", create=True):
            response = main.save_users("foo.csv", users.UserCollection())
            self.assertEqual(True, response)

    def test_load_status_updates(self):
        """
        Test for main's load_status_updates function
        """
        # replace dict reader with fake data
        main.csv.DictReader = Mock(return_value = self.test_status_csv_data)
        # replace open so that it does not error out when called with fake file
        with patch("builtins.open", create=True):
            response = main.load_status_updates("foo", user_status.UserStatusCollection())
            self.assertEqual(True, response)

    def test_save_status_updates(self):
        """
        Test for main's save_status_updates function
        """
        # replace open so that it does not error out when called with fake file
        with patch("builtins.open", create=True):
            response = main.save_status_updates("foo.csv", user_status.UserStatusCollection())
            self.assertEqual(True, response)

    def test_add_user(self):
        """
        Test for main's add_users function
        """
        # replace the users.add_user call with test value
        test_object = users.UserCollection()
        test_object.add_user = Mock(return_value="test")
        # call the add_user from main and see if returns test response
        response = main.add_user("1", "2", "3", "4", test_object)
        # make sure it matches test response
        self.assertEqual("test", response)

    def test_update_user(self):
        """
        Test for main's update_users function
        """
        # replace the users.modify_user call with test value
        test_object = users.UserCollection()
        test_object.modify_user = Mock(return_value="test")
        # add test_id to database
        test_object.database = {"test_id":"test"}
        # call the update_user from main and see if returns test response
        response = main.update_user("test_id", "2", "3", "4", test_object)
        # make sure it matches test response
        self.assertEqual("test", response)

    def test_delete_user(self):
        """
        Test for main's delete_users function
        """
        # replace the users.delete_user call with test value
        test_object = users.UserCollection()
        test_object.delete_user = Mock(return_value="test")
        # add test_id to database
        test_object.database = {"test_id":"test"}
        # call the add_user from main and see if returns test response
        response = main.delete_user("test_id", test_object)
        # make sure it matches test response
        self.assertEqual("test", response)

    def test_search_user(self):
        """
        Test for main's search_users function
        """
        # replace the users.delete_user call with test value
        test_object = users.UserCollection()
        test_object.search_user = Mock(return_value="test")
        # add test_id to database
        test_object.database = {"test_id":"test"}
        # call the add_user from main and see if returns test response
        response = main.search_user("test_id", test_object)
        # make sure it matches test response
        self.assertEqual("test", response)

    def test_add_status(self):
        """
        Test for main's add_status function
        """
        # replace the user_status.add_status call with test value
        test_object = user_status.UserStatusCollection()
        test_object.add_status = Mock(return_value="test")
        # add test_status to database
        test_object.database = {"test_status":"test"}
        # call the add_status from main and see if returns test response
        response = main.add_status("test_status", "2", "3", test_object)
        # make sure it matches test response
        self.assertEqual("test", response)

    def test_delete_status(self):
        """
        Test for main's delete_status function
        """
        # replace the user_status.add_status call with test value
        test_object = user_status.UserStatusCollection()
        test_object.delete_status = Mock(return_value="test")
        # add test_status to database
        test_object.database = {"test_status":"test"}
        # call the add_status from main and see if returns test response
        response = main.delete_status("test_status", test_object)
        # make sure it matches test response
        self.assertEqual("test", response)

    def test_update_status(self):
        """
        Test for main's update_status function
        """
        # replace the user_status.update_status call with test value
        test_object = user_status.UserStatusCollection()
        test_object.modify_status = Mock(return_value="test")
        # add test_status to database
        test_object.database = {"test_status":"test"}
        # call the add_status from main and see if returns test response
        response = main.update_status("test_status", "2", "3", test_object)
        # make sure it matches test response
        self.assertEqual("test", response)

    def test_search_status(self):
        """
        Test for main's search_status function
        """
        # replace the user_status.add_status call with test value
        test_object = user_status.UserStatusCollection()
        test_object.search_status = Mock(return_value="test")
        # add test_status to database
        test_object.database = {"test_status":"test"}
        # call the add_status from main and see if returns test response
        response = main.search_status("test_status", test_object)
        # make sure it matches test response
        self.assertEqual("test", response)
