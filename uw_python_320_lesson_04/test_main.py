"""
Test class to test main.py
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import main

# pylint: disable=C0103
class TestMainUserData(unittest.TestCase):
    """
    Testing class for main.py's functions that use user data
    """
    def setUp(self):
        """
        Set up function to create dummy data
        """
        # set up dummy csv data used in tests below
        self.test_user_csv_data = ({"USER_ID": "jakeh", "EMAIL": "jakeh@uw.edu",
                                    "NAME": "Jake", "LASTNAME": "H"},
                                {"USER_ID": "elizabethc", "EMAIL": "elizabethc@uw.edu",
                                    "NAME": "Elizabeth", "LASTNAME": "C"},
                                {"USER_ID": "matthewm", "EMAIL": "matthewm@uw.edu",
                                 "NAME": "Matthew", "LASTNAME": "M"})

    def test_init_user_collection(self):
        # pylint: disable=R0201
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
        mock_user_collection = Mock()
        mock_user_collection.batch_load_users.return_value = True
        # replace open so that it does not error out when called with fake file
        with (patch("builtins.open", create = True),
              patch("verify_input.verify_csv_file", return_value = [True, ""])):
            # use mock user collection tool
            response = main.load_users("foo", mock_user_collection)
            self.assertEqual(response, True)

    def test_load_users_bad_csv_data(self):
        """
        Test for main's load_users function with bad csv data
        """
        # replace dict reader with bad fake data that is missing column
        mock_dictreader = Mock(fieldnames = ["USER_ID", "EMAIL", "LASTNAME"])
        main.csv.DictReader = Mock(return_value = mock_dictreader)
        # create mock user collection
        mock_user_collection = Mock()
        # replace open so that it does not error out when called with fake file
        with (patch("builtins.open", create = True),
            patch("verify_input.verify_csv_file", return_value = [False, ""])):
            # use mock user collection tool
            response = main.load_users("foo", mock_user_collection)
            self.assertEqual(response, False)

    def test_load_users_bad_path(self):
        """
        Test for main's load_users function with bad file paths
        """
        # create mock user collection
        mock_user_collection = Mock()
        # set up fake file paths
        test_path = "fake/path.csv"
        # try to load users with fake paths
        with patch("verify_input.verify_csv_file", return_value = [False, ""]):
            response = main.load_users(test_path, mock_user_collection)
            self.assertEqual(response, False)

    def test_add_user_new(self):
        """
        Test for main's add_users function with a new user
        """
        # create mock user collection
        mock_user_collection = Mock()
        mock_user_collection.add_user = Mock(return_value = True)
        # call the add_user from main and get response
        with (patch("verify_input.verify_user_id", return_value = [True, ""]),
              patch("verify_input.verify_email", return_value = [True, ""]),
              patch("verify_input.verify_user_name", return_value = [True, ""]),
              patch("verify_input.verify_user_last_name", return_value = [True, ""])):
            response = main.add_user("testuser", "testuser@fake.com",
                                    "Test", "User", mock_user_collection)
            # make sure add user is called once
            mock_user_collection.add_user.assert_called_once_with(
                "testuser", "testuser@fake.com", "Test", "User"
            )
            # ensure user was added correctly
            self.assertEqual(response, True)

    def test_add_user_bad_id(self):
        """
        Test for main's add_users function with a bad (blank) ID
        """
        # create mock user collection
        mock_user_collection = Mock()
        # call the add_user from main and get response
        response = main.add_user("", "testuser@fake.com",
                                "Test", "User", mock_user_collection)
        # ensure user was not added
        self.assertEqual(response, False)

    def test_update_user_valid_id(self):
        """
        Test for main's update_users function with a valid ID
        """
        # create mock user collection
        mock_user_collection = Mock()
        mock_user_collection.modify_user = Mock(return_value = True)
        # bypass verify input functions
        with (patch("verify_input.verify_user_id", return_value = [True, ""]),
              patch("verify_input.verify_email", return_value = [True, ""]),
              patch("verify_input.verify_user_name", return_value = [True, ""]),
              patch("verify_input.verify_user_last_name", return_value = [True, ""])):
            # call update_user to update ID
            response = main.update_user("testuser", "fakeuser@fake.com",
                                    "Fake", "User", mock_user_collection)
            # make sure modify user is called once
            mock_user_collection.modify_user.assert_called_once_with(
                "testuser", "fakeuser@fake.com", "Fake", "User"
            )
            # ensure user was modified correctly
            self.assertEqual(response, True)

    def test_update_user_bad_id(self):
        """
        Test for main's update_users function with a bad (blank) ID
        """
        # create mock user collection
        mock_user_collection = Mock()
        mock_user_collection.modify_user = Mock(return_value = False)
        # bypass verify input functions
        with (patch("verify_input.verify_user_id", return_value = [True, ""]),
              patch("verify_input.verify_email", return_value = [True, ""]),
              patch("verify_input.verify_user_name", return_value = [True, ""]),
              patch("verify_input.verify_user_last_name", return_value = [True, ""])):
            # call update_user to update ID
            response = main.update_user("", "fakeuser@fake.com",
                                    "Fake", "User", mock_user_collection)
            # ensure user was not modified
            self.assertEqual(response, False)

    def test_delete_user_valid(self):
        """
        Test for main's delete_users function with a valid ID
        """
        # create mock user collection
        mock_user_collection = Mock()
        mock_user_collection.delete_user = Mock(return_value = True)
        # bypass verify input functions
        with patch("verify_input.verify_user_id", return_value = [True, ""]):
            # delete user from database
            response = main.delete_user("testuser", mock_user_collection)
            # make sure delete user is called once
            mock_user_collection.delete_user.assert_called_once_with("testuser")
            # make sure it was deleted
            self.assertEqual(response, True)

    def test_delete_user_invalid(self):
        """
        Test for main's delete_users function with invalid ID
        """
        # create mock user collection
        mock_user_collection = Mock()
        mock_user_collection.delete_user = Mock(return_value = False)
        # bypass verify input functions
        with patch("verify_input.verify_user_id", return_value = [True, ""]):
            # delete user from database
            response = main.delete_user("testing", mock_user_collection)
            # make sure delete user is called once
            mock_user_collection.delete_user.assert_called_once_with("testing")
            # make sure it was deleted
            self.assertEqual(response, False)

    def test_search_user_valid(self):
        """
        Test for main's search_users function with a valid ID
        """
        # create mock user collection
        mock_user_collection = Mock()
        mock_user_collection.search_user = Mock(return_value = Mock(user_id = "testuser"))
        # bypass verify input functions
        with patch("verify_input.verify_user_id", return_value = [True, ""]):
            # call search_user and get response
            response = main.search_user("testuser", mock_user_collection)
            # make sure delete user is called once
            mock_user_collection.search_user.assert_called_once_with("testuser")
            # make sure it matches test response
            self.assertEqual(response.user_id, "testuser")

    def test_search_user_invalid(self):
        """
        Test for main's search_users function with an invalid ID
        """
        # create mock user collection
        mock_user_collection = Mock()
        mock_user_collection.search_user = Mock(return_value = False)
        # bypass verify input functions
        with patch("verify_input.verify_user_id", return_value = [True, ""]):
            # call search_user and get response
            response = main.search_user("test@user", mock_user_collection)
            # make sure delete user is called once
            mock_user_collection.search_user.assert_called_once_with("test@user")
            # make sure it matches test response
            self.assertEqual(response, False)


class TestMainStatusData(unittest.TestCase):
    """
    Testing class for main.py's functions that use status data
    """
    def setUp(self):
        """
        Set up function to create dummy data
        """
        # pylint: disable=C0301
        # set up dummy csv data used in tests below
        self.test_status_csv_data = ({"STATUS_ID": "jakeh_00001", "USER_ID": "jakeh",
                                      "STATUS_TEXT": "Working through Python 320 tests"},
                                     {"STATUS_ID": "elizabethc_00001", "USER_ID": "elizabethc",
                                         "STATUS_TEXT": "Just got Jake some donuts!"},
                                     {"STATUS_ID": "matthewm_00001", "USER_ID": "matthewm",
                                      "STATUS_TEXT": "I'm making the best movie called Interstellar"})

    def test_init_status_collection(self):
        # pylint: disable=R0201
        """
        Test for main's init_status_collection function
        """
        # replace the user collection with a test value
        with patch("user_status.UserStatusCollection") as mock:
            # call init_user_collection
            main.init_status_collection()
            # verify user collection object is created
            mock.assert_called_once()

    def test_load_status_updates_good_data(self):
        """
        Test for main's load_status_updates function with good data
        """
        # replace dict reader with good fake data
        mock_dictreader = MagicMock(fieldnames = ["STATUS_ID", "USER_ID", "STATUS_TEXT"])
        mock_dictreader.__iter__.return_value = self.test_status_csv_data
        main.csv.DictReader = Mock(return_value = mock_dictreader)
        # create mock user status collection
        mock_status_collection = Mock()
        mock_status_collection.batch_load_statuses.return_value = True
        # replace open so that it does not error out when called with fake file
        with (patch("builtins.open", create = True),
              patch("verify_input.verify_csv_file", return_value = [True, ""])):
            # use mock user status collection tool
            response = main.load_status_updates("foo", mock_status_collection)
            self.assertEqual(response, True)

    def test_load_users_bad_csv_data(self):
        """
        Test for main's load_status_updates function with bad csv data
        """
        # replace dict reader with good fake data
        mock_dictreader = MagicMock(fieldnames = ["STATUS_ID", "STATUS_TEXT"])
        mock_dictreader.__iter__.return_value = self.test_status_csv_data
        main.csv.DictReader = Mock(return_value = mock_dictreader)
        # create mock user status collection
        mock_status_collection = Mock()
        mock_status_collection.add_status.return_value = False
        # replace open so that it does not error out when called with fake file
        with (patch("builtins.open", create = True),
              patch("verify_input.verify_csv_file", return_value = [True, ""])):
            # use mock user status collection tool
            response = main.load_status_updates("foo", mock_status_collection)
            self.assertEqual(response, False)

    def test_load_users_bad_path(self):
        """
        Test for main's load_status_updates function with bad file path
        """
        # create mock user collection
        mock_status_collection = Mock()
        # set up fake file paths
        test_path = "fake/path.csv"
        # try to load users with fake paths
        with patch("verify_input.verify_csv_file", return_value = [False, ""]):
            response = main.load_status_updates(test_path, mock_status_collection)
            self.assertEqual(response, False)

    def test_add_status_new(self):
        """
        Test for main's add_status function with a new status
        """
        # create mock status collection
        mock_status_collection = Mock()
        mock_status_collection.add_status = Mock(return_value = True)
        # call the add_status from main and get response
        with (patch("verify_input.verify_status_id", return_value = [True, ""]),
              patch("verify_input.verify_user_id", return_value = [True, ""]),
              patch("verify_input.verify_status_text", return_value = [True, ""])):
            response = main.add_status("testuser", "testuser_00001",
                                    "test entry", mock_status_collection)
            # make sure add status is called once
            mock_status_collection.add_status.assert_called_once_with(
                "testuser_00001", "testuser", "test entry"
            )
            # ensure user was added correctly
            self.assertEqual(response, True)

    def test_add_status_bad_id(self):
        """
        Test for main's add_status function with a bad ID
        """
        # create mock status collection
        mock_status_collection = Mock()
        mock_status_collection.add_status = Mock(return_value = False)
        # call the add_status from main and get response
        with (patch("verify_input.verify_status_id", return_value = [True, ""]),
              patch("verify_input.verify_user_id", return_value = [True, ""]),
              patch("verify_input.verify_status_text", return_value = [True, ""])):
            response = main.add_status("", "testuser_00001",
                                    "test entry", mock_status_collection)
            # make sure add status is called once
            mock_status_collection.add_status.assert_called_once_with(
                "testuser_00001", "", "test entry"
            )
            # ensure user was not added
            self.assertEqual(response, False)

    def test_update_status_valid_id(self):
        """
        Test for main's update_status function with a valid ID
        """
        # create mock status collection
        mock_status_collection = Mock()
        mock_status_collection.modify_status = Mock(return_value = True)
        # call the update_status from main and get response
        with (patch("verify_input.verify_status_id", return_value = [True, ""]),
              patch("verify_input.verify_user_id", return_value = [True, ""]),
              patch("verify_input.verify_status_text", return_value = [True, ""])):
            response = main.update_status("testuser_00001", "testuser",
                                    "test entry", mock_status_collection)
            # make sure update status is called once
            mock_status_collection.modify_status.assert_called_once_with(
                "testuser_00001", "testuser", "test entry"
            )
            # ensure user was updated
            self.assertEqual(response, True)

    def test_update_status_bad_id(self):
        """
        Test for main's update_status function with a bad ID
        """
        # create mock status collection
        mock_status_collection = Mock()
        mock_status_collection.modify_status = Mock(return_value = False)
        # call the update_status from main and get response
        with (patch("verify_input.verify_status_id", return_value = [True, ""]),
              patch("verify_input.verify_user_id", return_value = [True, ""]),
              patch("verify_input.verify_status_text", return_value = [True, ""])):
            response = main.update_status("testuser_00001", "",
                                    "test entry", mock_status_collection)
            # make sure update status is called once
            mock_status_collection.modify_status.assert_called_once_with(
                "testuser_00001", "", "test entry"
            )
            # ensure user was not updated
            self.assertEqual(response, False)

    def test_delete_status_valid(self):
        """
        Test for main's delete_status function with a valid ID
        """
        # create mock status collection
        mock_status_collection = Mock()
        mock_status_collection.delete_status = Mock(return_value = True)
        # bypass verify input functions
        with patch("verify_input.verify_status_id", return_value = [True, ""]):
            # delete user from database
            response = main.delete_status("testuser_00001", mock_status_collection)
            # make sure delete status is called once
            mock_status_collection.delete_status.assert_called_once_with("testuser_00001")
            # make sure it was deleted
            self.assertEqual(response, True)

    def test_delete_status_invalid(self):
        """
        Test for main's delete_status function with an invalid ID
        """
        # create mock status collection
        mock_status_collection = Mock()
        mock_status_collection.delete_status = Mock(return_value = False)
        # bypass verify input functions
        with patch("verify_input.verify_status_id", return_value = [True, ""]):
            # try to delete status from database
            response = main.delete_status("", mock_status_collection)
            # make sure delete status is called once
            mock_status_collection.delete_status.assert_called_once_with("")
            # make sure it was deleted
            self.assertEqual(response, False)

    def test_search_status_valid(self):
        """
        Test for main's search_status function with a valid ID
        """
        # create mock status collection
        mock_status_collection = Mock()
        mock_status_collection.search_status = Mock(
            return_value = Mock(status_id = "testuser_00001")
            )
        # bypass verify input functions
        with patch("verify_input.verify_status_id", return_value = [True, ""]):
            # call search_status and get response
            response = main.search_status("testuser_00001", mock_status_collection)
            # make sure search status is called
            mock_status_collection.search_status.assert_called_once_with("testuser_00001")
            # make sure it matches test response
            self.assertEqual(response.status_id, "testuser_00001")

    def test_search_status_invalid(self):
        """
        Test for main's search_status function with an invalid ID
        """
        # create mock status collection
        mock_status_collection = Mock()
        mock_status_collection.search_status = Mock(return_value = False)
        # bypass verify input functions
        with patch("verify_input.verify_status_id", return_value = [True, ""]):
            # call search_status and get response
            response = main.search_status("test@user", mock_status_collection)
            # make sure search status is called
            mock_status_collection.search_status.assert_called_once_with("test@user")
            # make sure it matches test response
            self.assertEqual(response, False)
