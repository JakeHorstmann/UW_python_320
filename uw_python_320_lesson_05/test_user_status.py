"""
Test class to test user_status.py
"""
# pylint: disable=R0903, E0401
import unittest
from pymongo import MongoClient
from user_status import UserStatusCollection
from users import UserCollection

client = MongoClient(host="localhost", port = 27017)

class TestUserStatus(unittest.TestCase):
    """
    Testing class for user_status.py
    """
    def setUp(self):
        """
        Set up function to create dummy database
        """
        # set up database to be used in tests below
        self.database = client.database
        self.user_collection = UserCollection(self.database["TestUserAccounts"])
        self.status_collection = UserStatusCollection(self.database["TestStatusUpdates"])
        # create test user to add to database
        user_id = "testuser"
        email = "test@user.com"
        user_name = "test"
        user_last_name = "user"
        self.user_collection.add_user(user_id, email, user_name, user_last_name)
        # create test status to add to user status collection
        test_status_id = "testuser_00001"
        test_id = "testuser"
        test_text = "My first status post"
        self.status_collection.add_status(test_status_id, test_id, test_text)

    def tearDown(self):
        """
        Tear down function to reset database
        """
        self.database["TestUserAccounts"].drop()
        self.database["TestStatusUpdates"].drop()

    def test_statuscollection_add_valid_status(self):
        """
        Test for StatusCollection's add_status method with good data
        """
        # create test status to add to user collection
        test_status_id = "testuser_00002"
        test_id = "testuser"
        test_text = "this is my second entry!"
        # add in test data
        response = self.status_collection.add_status(
            test_status_id, test_id, test_text)
        # assure status was added correctly
        self.assertEqual(response, True)

    def test_statuscollect_add_duplicate_status(self):
        """
        Test for StatusCollection's add_status method with duplicate ID
        """
        # create test status that is duplicate data
        test_status_id = "testuser_00001"
        test_id = "testuser"
        test_text = "My first status post"
        # add in duplicate data
        response = self.status_collection.add_status(
            test_status_id, test_id, test_text)
        # assure status was not added
        self.assertEqual(response, False)

    def test_statuscollect_add_status_no_foreign_key(self):
        """
        Test for StatusCollection's add_status method with an invalid foreign key
        """
        # create test status that has invalid user
        test_status_id = "testuser_00001"
        test_id = "testuserthatDNE"
        test_text = "My first status post"
        # add in invalid data
        response = self.status_collection.add_status(
            test_status_id, test_id, test_text)
        # assure status was not added
        self.assertEqual(response, False)

    def test_statuscollect_modify_valid_status(self):
        """
        Test for StatusCollection's modify_status method with good status
        """
        # update status to have more enthusiasm
        modify_status_id = "testuser_00001"
        modified_id = "testuser"
        modified_text = "My first status post!!!!"
        # modify status in status_collection
        response = self.status_collection.modify_status(
            modify_status_id, modified_id, modified_text
        )
        # assure status was modified correctly
        self.assertEqual(response, True)

    def test_statuscollect_modify_invalid_status(self):
        """
        Test for StatusCollection's modify_status method with bad status
        """
        # try to modify a status that DNE
        modify_status_id = "testuser_99999"
        modified_id = "testuser"
        modified_text = "this better not work"
        # modify status in user_status_collection
        response = self.status_collection.modify_status(
            modify_status_id, modified_id, modified_text
        )
        # assure status was not modified
        self.assertEqual(response, False)

    # def test_statuscollect_modify_status_no_foreign_key(self):
    #     """
    #     Test for StatusCollection's modify_status method with an invalid foreign key
    #     """
    #     # create test status that has invalid user
    #     modify_status_id = "testuser_00001"
    #     modified_id = "testuserthatDNE"
    #     modified_text = "this better not work"
    #     # try to modify status
    #     response = self.status_collection.modify_status(
    #         modify_status_id, modified_id, modified_text
    #     )
    #     # assure status was not added
    #     self.assertEqual(response, False)

    def test_statuscollect_delete_valid_status(self):
        """
        Test for StatusCollection's delete_status method with valid status
        """
        # status id to delete
        delete_status_id = "testuser_00001"
        # delete jakeh_00002 status
        response = self.status_collection.delete_status(delete_status_id)
        # assure status was deleted
        self.assertEqual(response, True)

    def test_statuscollect_delete_invalid_status(self):
        """
        Test for StatusCollection's delete_status method with invalid status
        """
        # set up invalid status id
        delete_status_id = "testuser_99999"
        # try to delete fake id
        response = self.status_collection.delete_status(delete_status_id)
        # assure nothing was deleted
        self.assertEqual(response, False)

    def test_statuscollect_search_valid_status(self):
        """
        Test for StatusCollection's search_status method
        """
        # search for this status
        search_status_id = "testuser_00001"
        # search for status with search_id
        response = self.status_collection.search_status(search_status_id)
        # assure status was found
        self.assertEqual(response["_id"], search_status_id)

    def test_statuscollect_search_invalid_status(self):
        """
        Test for StatusCollection's search_status method with invalid status
        """
        # set up invalid status id
        search_status_id = "testuser_99999"
        # search for status with search_id
        response = self.status_collection.search_status(search_status_id)
        # assure status was not found
        self.assertEqual(response, False)
