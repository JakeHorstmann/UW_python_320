"""
Test class to test user_status.py
"""

import unittest
from unittest.mock import Mock
import user_status

# pylint: disable=C0103


class TestUserStatus(unittest.TestCase):
    """
    Testing class for user_status.py
    """

    def setUp(self):
        """
        Method to create dummy status data used in testing
        """
        # set up dummy data used in tests below
        test_user_status = [
            user_status.UserStatus("jakeh_00001", "jakeh",
                                   "Working through Python 320 tests"),
            user_status.UserStatus("elizabethc_00001", "elizabethc",
                                   "Just got Jake some donuts!"),
            user_status.UserStatus("matthewm_00001", "matthewm",
                                   "I'm making the best movie called Interstellar"),
            user_status.UserStatus("jakeh_00002", "jakeh",
                                   "Struggling through Python 320 tests..."),
            user_status.UserStatus("jakeh_00003", "jakeh",
                                   "Made it through Python 320 tests!")]
        test_user_status_data = {}
        # format dictionary for the user status tool
        for test_status in test_user_status:
            test_user_status_data[test_status.status_id] = test_status
        # create dummy user status data
        test_data = user_status.UserStatusCollection()
        test_data.database = test_user_status_data
        # override user status collection tool to return fake data
        user_status.UserStatusCollection = Mock(return_value=test_data)

    def test_StatusCollect_add_valid_status(self):
        """
        Test for StatusCollection's add_status method with good data
        """
        # create test status to add to user collection
        test_status_id = "testuser_00001"
        test_id = "testuser"
        test_text = "My first status post"
        # create user_status_collection with dummy data
        user_status_collection = user_status.UserStatusCollection()
        # add in test data
        response = user_status_collection.add_status(
            test_status_id, test_id, test_text)
        # assure status was added correctly
        self.assertEqual(response, True)

    def test_StatusCollect_add_duplicate_status(self):
        """
        Test for StatusCollection's add_status method with duplicate ID
        """
        # create test status with duplicate data to add to user collection
        test_status_id = "jakeh_00001"
        test_id = "jakeh"
        test_text = "My first status post"
        # create user_status_collection with dummy data
        user_status_collection = user_status.UserStatusCollection()
        # add in duplicate data
        response = user_status_collection.add_status(
            test_status_id, test_id, test_text)
        # assure status was not added
        self.assertEqual(response, False)

    def test_StatusCollect_modify_valid_status(self):
        """
        Test for StatusCollection's modify_status method with good status
        """
        # update jake's 3rd status to have more enthusiasm
        modify_status_id = "jakeh_00003"
        modified_id = "jakeh"
        modified_text = "Made it through Python 320 tests!!!"
        # create user_status_collection with dummy data
        user_status_collection = user_status.UserStatusCollection()
        # modify status in user_status_collection
        response = user_status_collection.modify_status(
            modify_status_id, modified_id, modified_text
        )
        # assure status was modified correctly
        self.assertEqual(response, True)

    def test_StatusCollect_modify_invalid_status(self):
        """
        Test for StatusCollection's modify_status method with bad status
        """
        # update jake's 3rd status to have more enthusiasm
        modify_status_id = "jakeh_99999"
        modified_id = "jakeh"
        modified_text = "this better not work"
        # create user_status_collection with dummy data
        user_status_collection = user_status.UserStatusCollection()
        # modify status in user_status_collection
        response = user_status_collection.modify_status(
            modify_status_id, modified_id, modified_text
        )
        # assure status was not modified
        self.assertEqual(response, False)

    def test_StatusCollect_delete_valid_status(self):
        """
        Test for StatusCollection's delete_status method with valid status
        """
        # status id to delete cause i did better than i thought
        delete_status_id = "jakeh_00002"
        # create user_status_collection with dummy data
        user_status_collection = user_status.UserStatusCollection()
        # delete jakeh_00002 status
        response = user_status_collection.delete_status(delete_status_id)
        # assure status was deleted
        self.assertEqual(response, True)

    def test_StatusCollect_delete_invalid_status(self):
        """
        Test for StatusCollection's delete_status method with invalid status
        """
        # set up invalid status id
        delete_status_id = "jakeh_99999"
        # create user_status_collection with dummy data
        user_status_collection = user_status.UserStatusCollection()
        # try to delete
        response = user_status_collection.delete_status(delete_status_id)
        # assure nothing was deleted
        self.assertEqual(response, False)

    def test_StatusCollect_search_valid_status(self):
        """
        Test for StatusCollection's search_status method
        """
        # search for this status
        search_status_id = "jakeh_00001"
        # create user_status_collection with fake user to search for
        user_status_collection = user_status.UserStatusCollection()
        # search for status with search_id
        response = user_status_collection.search_status(search_status_id)
        # assure status was found
        self.assertEqual(response.status_id, search_status_id)

    def test_StatusCollect_search_invalid_status(self):
        """
        Test for StatusCollection's search_status method with invalid status
        """
        # search for this status
        search_status_id = "jakeh_99999"
        # create user_status_collection with fake data
        user_status_collection = user_status.UserStatusCollection()
        # search for status with search_id
        response = user_status_collection.search_status(search_status_id)
        # assure status was not found
        self.assertEqual(response.status_id, None)
