"""
Test class to test main.py
"""

import unittest
from unittest.mock import Mock, patch, MagicMock, mock_open
import main
import user_status
import users
from io import StringIO

# pylint: disable=C0103
class TestMainUserData(unittest.TestCase):
    """
    Testing class for main.py's functions that use User data
    """
    def setUp(self):
        """
        Set up test functions with some dummy user data for testing
        """
        # pylint: disable=C0301
        # get backup
        self.backup_user_collection = users.UserCollection
        # set up dummy csv data used in tests below
        self.test_user_csv_data = ({"USER_ID": "jakeh", "EMAIL": "jakeh@uw.edu", "NAME": "Jake", "LASTNAME": "H"},
                                {"USER_ID": "elizabethc", "EMAIL": "elizabethc@uw.edu",
                                    "NAME": "Elizabeth", "LASTNAME": "C"},
                                {"USER_ID": "matthewm", "EMAIL": "matthewm@uw.edu", "NAME": "Matthew", "LASTNAME": "M"})
        # set up dummy data used in tests below
        # create mock users for the user database
        mock_user_1 = Mock(user_id = "jakeh", email = "jakeh@uw.edu", user_name = "Jake", user_last_name = "H")
        mock_user_2 = Mock(user_id = "elizabethc", email = "elizabethc@uw.edu", user_name = "Elizabeth", user_last_name = "C")
        mock_user_3 = Mock(user_id = "matthewm", email = "matthewm@uw.edu", user_name = "Matthew", user_last_name = "M")
        mock_users = [mock_user_1, mock_user_2, mock_user_3]
        mock_user_data = {}
        # format dictionary like the user collection tool
        for mock_user in mock_users:
            mock_user_data[mock_user.user_id] = mock_user
        # create good dummy user available to test class
        self.mock_user_data = mock_user_data
        
    def test_init_user_collection(self):
        """
        Test for main's init_user_collection function
        """
        # replace the user collection with a test value
        with patch("users.UserCollection") as mock:
            # call init_user_collection
            main.init_user_collection()
            # verify user collection object is created
            mock.assert_called_once()

    def test_load_users_good_data(self):
        """
        Test for main's load_users function with good data
        """
        # replace dict reader with good fake data
        mock_dictreader = MagicMock(fieldnames = ["USER_ID", "EMAIL", "NAME", "LASTNAME"])
        mock_dictreader.__iter__.return_value = self.test_user_csv_data
        main.csv.DictReader = Mock(return_value = mock_dictreader)
        # create mock user collection
        mock_user_collection = Mock(database = self.mock_user_data)
        mock_user_collection.add_user.return_value = True
        # replace open so that it does not error out when called with fake file
        with patch("builtins.open", create = True):
            # use mock user collection tool
            response = main.load_users("foo", mock_user_collection)
            self.assertEqual(True, response)

    def test_load_users_bad_csv_data(self):
        """
        Test for main's load_users function with bad csv data
        """
        # replace dict reader with bad fake data that is missing column
        mock_dictreader = Mock(fieldnames = ["USER_ID", "EMAIL", "LASTNAME"])
        main.csv.DictReader = Mock(return_value = mock_dictreader)
        # create mock user collection
        mock_user_collection = Mock(database = self.mock_user_data)
        # replace open so that it does not error out when called with fake file
        with patch("builtins.open", create = True):
            # use mock user collection tool
            response = main.load_users("foo", mock_user_collection)
            self.assertEqual(False, response)

    def test_load_users_bad_path(self):
        """
        Test for main's load_users function with bad file paths
        """
        # create mock user collection
        mock_user_collection = Mock(database = self.mock_user_data)
        # set up fake file paths
        test_path_1 = "fake_path.txt"
        test_path_2 = "fake/path.csv"
        # try to load users with fake paths
        test_1_response = main.load_users(test_path_1, mock_user_collection)
        test_2_response = main.load_users(test_path_2, mock_user_collection)
        # ensure both return False (hit file not found exception)
        self.assertEqual(False, test_1_response)
        self.assertEqual(False, test_2_response)

    def test_save_users_good_data(self):
        """
        Test for main's save_users function with good data
        """
        # create mock user collection
        mock_user_collection = Mock(database = self.mock_user_data)
        # create mock writer
        mock_writer = Mock()
        # set its writerow to a mock to track how many times it's called
        mock_writer.writerow = Mock()
        # ensure open is called correctly with fake file
        with patch("builtins.open", mock_open()):
            with patch("csv.writer", return_value = mock_writer):
                response = main.save_users("foo.csv", mock_user_collection)
                # make sure writerow was called 4 times (3 users + 1 column header)
                self.assertEqual(4, mock_writer.writerow.call_count)
                # assure everything was successful
                self.assertEqual(True, response)

    def test_save_users_bad_extension(self):
        """
        Test for main's save_users function with a bad extension
        """
        # create mock user collection
        mock_user_collection = Mock(database = self.mock_user_data)
        # call test function
        response = main.save_users("bad_path.docx", mock_user_collection)
        # assure it did not get through
        self.assertEqual(False, response)

    def test_add_user_new(self):
        """
        Test for main's add_users function with a new user
        """
        # create mock user collection
        mock_user_collection = Mock(database = self.mock_user_data)
        mock_user_collection.add_user = Mock(return_value = True)
        # call the add_user from main and get response
        response = main.add_user("testuser", "testuser@fake.com",
                                "Test", "User", mock_user_collection)
        # make sure add user is called once
        mock_user_collection.add_user.assert_called_once_with(
            "testuser", "testuser@fake.com", "Test", "User"
        )
        # ensure user was added correctly
        self.assertEqual(True, response)
    
    def test_add_user_bad_id(self):
        """
        Test for main's add_users function with a bad (blank) ID
        """
        # create mock user collection
        mock_user_collection = Mock(database = self.mock_user_data)
        # call the add_user from main and get response
        response = main.add_user("", "testuser@fake.com",
                                "Test", "User", mock_user_collection)
        # ensure user was not added
        self.assertEqual(False, response)

    def test_update_user_valid_id(self):
        """
        Test for main's update_users function with a valid ID
        """
        # create mock user collection
        mock_user = Mock(user_id = "testuser", user_email = "testuser@fake.com",
                            user_name = "Test", user_last_name =  "User")
        mock_user_collection = Mock(database = {"testuser": mock_user})
        mock_user_collection.modify_user = Mock(return_value = True)
        # call update_user to update ID
        response = main.update_user("testuser", "fakeuser@fake.com",
                                "Fake", "User", mock_user_collection)
        # make sure modify user is called once
        mock_user_collection.modify_user.assert_called_once_with(
            "testuser", "fakeuser@fake.com", "Fake", "User"
        )
        # ensure user was modified correctly
        self.assertEqual(True, response)

    def test_update_user_bad_id(self):
        """
        Test for main's update_users function with a bad (blank) ID
        """
        # create mock user collection
        mock_user_collection = Mock(database = self.mock_user_data)
        # call update_user to update ID
        response = main.update_user("", "fakeuser@fake.com",
                                "Fake", "User", mock_user_collection)
        # ensure user was not modified
        self.assertEqual(False, response)

    def test_delete_user_valid(self):
        """
        Test for main's delete_users function with a valid ID
        """
        # create mock user collection
        mock_user = Mock(user_id = "testuser", user_email = "testuser@fake.com",
                            user_name = "Test", user_last_name =  "User")
        mock_user_collection = Mock(database = {"testuser": mock_user})
        mock_user_collection.delete_user = Mock(return_value = True)
        # delete user from database
        response = main.delete_user("testuser", mock_user_collection)
        # make sure delete user is called once
        mock_user_collection.delete_user.assert_called_once_with("testuser")
        # make sure it was deleted
        self.assertEqual(True, response)

    def test_delete_user_invalid(self):
        """
        Test for main's delete_users function with invalid ID
        """
        # create mock user collection
        mock_user_collection = Mock(database = self.mock_user_data)
        # delete user from database
        response = main.delete_user("", mock_user_collection)
        # make sure nothing was deleted
        self.assertEqual(False, response)

    def test_search_user_valid(self):
        """
        Test for main's search_users function with a valid ID
        """
        # create mock user collection
        mock_user = Mock(user_id = "testuser", user_email = "testuser@fake.com",
                            user_name = "Test", user_last_name =  "User")
        mock_user_collection = Mock(database = {"testuser": mock_user})
        mock_user_collection.search_user = Mock(return_value = mock_user)
        # call search_user and get response
        response = main.search_user("testuser", mock_user_collection)
        # make sure delete user is called once
        mock_user_collection.search_user.assert_called_once_with("testuser")
        # make sure it matches test response
        self.assertEqual("testuser", response.user_id)

    def test_search_user_blank_id(self):
        """
        Test for main's search_users function with a blank ID
        """
        # create mock user collection
        mock_user_collection = Mock(database = self.mock_user_data)
        # call search_user and get response
        response = main.search_user("", mock_user_collection)
        # make sure it matches test response
        self.assertEqual(None, response.user_id)


class TestMainStatusData(unittest.TestCase):
    pass


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
                                   {"USER_ID": "elizabethc", "EMAIL": "elizabethc@uw.edu",
                                       "NAME": "Elizabeth", "LASTNAME": "C"},
                                   {"USER_ID": "matthewm", "EMAIL": "matthewm@uw.edu", "NAME": "Matthew", "LASTNAME": "M"})
        self.test_status_csv_data = ({"STATUS_ID": "jakeh_00001", "USER_ID": "jakeh", "STATUS_TEXT": "Working through Python 320 tests"},
                                     {"STATUS_ID": "elizabethc_00001", "USER_ID": "elizabethc",
                                         "STATUS_TEXT": "Just got Jake some donuts!"},
                                     {"STATUS_ID": "matthewm_00001", "USER_ID": "matthewm", "STATUS_TEXT": "I'm making the best movie called Interstellar"})
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
        self.user_collection = users.UserCollection

        # set up dummy status data used in tests below
        test_user_status = [user_status.UserStatus("jakeh_00001", "jakeh", "Working through Python 320 tests"),
                            user_status.UserStatus(
                                "elizabethc_00001", "elizabethc", "Just got Jake some donuts!"),
                            user_status.UserStatus(
                                "matthewm_00001", "matthewm_00001", "I'm making the best movie called Interstellar"),
                            user_status.UserStatus(
                                "jakeh_00002", "jakeh", "Struggling through Python 320 tests..."),
                            user_status.UserStatus("jakeh_00003", "jakeh", "Made it through Python 320 tests!")]
        test_user_status_data = {}
        # format dictionary for the user status tool
        for test_status in test_user_status:
            test_user_status_data[test_status.status_id] = test_status
        # create dummy user status data
        test_data = user_status.UserStatusCollection()
        test_data.database = test_user_status_data
        # override user status collection tool to return fake data
        user_status.UserStatusCollection = Mock(return_value=test_data)
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
        with patch("users.UserCollection", return_value="test"):
            # call init_user_collection to return fake data
            response = main.init_user_collection()
            # make sure it matches test response
            self.assertEqual("test", response)

    def test_init_status_collection(self):
        """
        Test for main's init_status_collection function
        """
        # replace the status collection with a test value
        with patch("user_status.UserStatusCollection", return_value="test"):
            # call init_user_collection to return fake data
            response = main.init_status_collection()
            # make sure it matches test response
            self.assertEqual("test", response)

    def test_load_status_updates(self):
        """
        Test for main's load_status_updates function
        """
        # replace dict reader with fake data
        mock_dictreader = MagicMock(fieldnames = ["STATUS_ID", "USER_ID", "STATUS_TEXT"])
        mock_dictreader.__iter__.return_value = self.test_status_csv_data
        main.csv.DictReader = Mock(return_value = mock_dictreader)
        # replace open so that it does not error out when called with fake file
        with patch("builtins.open", create=True):
            response = main.load_status_updates(
                "foo", user_status.UserStatusCollection())
            self.assertEqual(True, response)

    def test_save_status_updates(self):
        """
        Test for main's save_status_updates function
        """
        # replace open so that it does not error out when called with fake file
        with patch("builtins.open", create=True):
            response = main.save_status_updates(
                "foo.csv", user_status.UserStatusCollection())
            self.assertEqual(True, response)

    def test_add_status(self):
        """
        Test for main's add_status function
        """
        # replace the user_status.add_status call with test value
        test_object = user_status.UserStatusCollection()
        test_object.add_status = Mock(return_value="test")
        # add test_status to database
        test_object.database = {"test_status": "test"}
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
        test_object.database = {"test_status": "test"}
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
        test_object.database = {"test_status": "test"}
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
        test_object.database = {"test_status": "test"}
        # call the add_status from main and see if returns test response
        response = main.search_status("test_status", test_object)
        # make sure it matches test response
        self.assertEqual("test", response)
