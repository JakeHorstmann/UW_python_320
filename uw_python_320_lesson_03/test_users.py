"""
Test class to test users.py
"""
# pylint: disable=R0903, E0401
import unittest
from peewee import SqliteDatabase
import users
from socialnetwork_model import UserModel

class TestUsers(unittest.TestCase):
    """
    Testing class for users.py
    """

    def setUp(self):
        """
        Set up function to create dummy database
        """
        # set up database to be used in tests below
        self.database = SqliteDatabase(":memory:", pragmas={"foreign_keys": 1})
        self.database.bind([UserModel])
        self.database.connect()
        self.database.create_tables([UserModel])
        self.user_collection = users.UserCollection(self.database)
        # create test user to add to database
        user_id = "testuser"
        email = "test@user.com"
        user_name = "test"
        user_last_name = "user"
        self.user_collection.add_user(user_id, email, user_name, user_last_name)

    def tearDown(self):
        """
        Tear down function to reset database
        """
        self.database.drop_tables([UserModel])
        self.database.close()

    def test_usercollect_add_valid_user(self):
        """
        Test for UserCollection's add_user method with valid user
        """
        # create test user to add to user collection
        test_id = "anothertestuser"
        test_email = "anothertest@user.com"
        test_name = "anothertest"
        test_last_name = "user"
        # add in test data
        response = self.user_collection.add_user(
            test_id, test_email, test_name, test_last_name)
        # assure user was added correctly
        self.assertEqual(response, True)

    def test_usercollect_add_invalid_user(self):
        """
        Test for UserCollection's add_user method with duplicate user
        """
        # create test user to add to user collection
        test_id = "testuser"
        test_email = "test@user.com"
        test_name = "test"
        test_last_name = "user"
        # add in test data
        response = self.user_collection.add_user(
            test_id, test_email, test_name, test_last_name)
        # assure user was not added
        self.assertEqual(response, False)

    def test_usercollect_modify_valid_user(self):
        """
        Test for UserCollection's modify_user method with valid user
        """
        # update jakeh id with new email and last name
        modify_id = "testuser"
        modified_email = "testuser@uw.edu"
        modified_name = "test"
        modified_last_name = "user"
        # modify testuser
        response = self.user_collection.modify_user(modify_id, modified_email,
                                               modified_name, modified_last_name)
        # assure user was modified
        self.assertEqual(response, True)

    def test_usercollect_modify_invalid_user(self):
        """
        Test for UserCollection's modify_user method with invalid user
        """
        # create bad id with data
        modify_id = "faketestuser"
        modified_email = "faketest@user.com"
        modified_name = "faketest"
        modified_last_name = "user"
        # try to modify invalid id
        response = self.user_collection.modify_user(modify_id, modified_email,
                                               modified_name, modified_last_name)
        # assure nothing was modified
        self.assertEqual(response, False)

    def test_usercollect_delete_valid_user(self):
        """
        Test for UserCollection's delete_user method with valid user
        """
        # id to delete
        delete_id = "testuser"
        # delete id
        response = self.user_collection.delete_user(delete_id)
        # assure user was deleted
        self.assertEqual(response, True)

    def test_usercollect_delete_invalid_user(self):
        """
        Test for UserCollection's delete_user method with invalid user
        """
        # fake id to delete
        delete_id = "faketestuser"
        # try to delete id
        response = self.user_collection.delete_user(delete_id)
        # assure nothing was deleted
        self.assertEqual(response, False)

    def test_usercollect_search_valid_user(self):
        """
        Test for UserCollection's search_user method with a valid user
        """
        # search for this id
        search_id = "testuser"
        # search for user with search_id
        response = self.user_collection.search_user(search_id)
        # assure user was found
        self.assertEqual(response.user_id, search_id)

    def test_usercollect_search_invalid_user(self):
        """
        Test for UserCollection's search_user method with an invalid user
        """
        # try to search for this id
        search_id = "faketestuser"
        # search for user with search_id
        response = self.user_collection.search_user(search_id)
        # assure user was not found
        self.assertEqual(response, False)
