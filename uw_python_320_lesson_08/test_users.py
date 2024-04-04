"""
Test class to test users.py
"""
# pylint: disable=R0903, E0401
import unittest
from playhouse.dataset import DataSet
import users

USER_TABLE = "UserModel"

class TestUsers(unittest.TestCase):
    """
    Testing class for users.py
    """

    def setUp(self):
        """
        Set up function to create dummy database
        """
        # set up database to be used in tests below
        db = DataSet("sqlite:///:memory:")
        # make sure user_id column is unique
        db[USER_TABLE].insert(id = 1,
                            user_id = "testuser",
                            user_email = "test@user.com",
                            user_name = "test",
                            user_last_name = "user")
        db[USER_TABLE].create_index(["user_id"], unique = True)
        self.db = db

    def tearDown(self):
        """
        Tear down function to reset database
        """
        self.db.close()

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
        add_user_to_db = users.add_user(self.db)
        response = add_user_to_db(user_id = test_id,
                                  user_email = test_email,
                                  user_name = test_name,
                                  user_last_name = test_last_name)
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
        add_user_to_db = users.add_user(self.db)
        response = add_user_to_db(user_id = test_id,
                                  user_email = test_email,
                                  user_name = test_name,
                                  user_last_name = test_last_name)
        # assure user was not added
        self.assertEqual(response, False)

    def test_usercollect_update_valid_user(self):
        """
        Test for UserCollection's update_user method with valid user
        """
        # update jakeh id with new email and last name
        modify_id = "testuser"
        modified_email = "testuser@uw.edu"
        modified_name = "test"
        modified_last_name = "user"
        # modify testuser
        update_user_in_db = users.update_user(self.db)
        response = update_user_in_db(user_id = modify_id,
                                     user_email = modified_email,
                                       user_name = modified_name,
                                        user_last_name = modified_last_name)
        # assure user was modified
        self.assertEqual(response, True)

    def test_usercollect_update_invalid_user(self):
        """
        Test for UserCollection's modify_user method with invalid user
        """
        # create bad id with data
        modify_id = "faketestuser"
        modified_email = "faketest@user.com"
        modified_name = "faketest"
        modified_last_name = "user"
        # modify testuser
        update_user_in_db = users.update_user(self.db)
        response = update_user_in_db(user_id = modify_id,
                                     user_email = modified_email,
                                       user_name = modified_name,
                                        user_last_name = modified_last_name)
        # assure nothing was modified
        self.assertEqual(response, False)

    def test_usercollect_delete_valid_user(self):
        """
        Test for UserCollection's delete_user method with valid user
        """
        # id to delete
        delete_id = "testuser"
        # delete id
        delete_user_from_db = users.delete_user(self.db)
        response = delete_user_from_db(user_id = delete_id)
        # assure user was deleted
        self.assertEqual(response, True)

    def test_usercollect_delete_invalid_user(self):
        """
        Test for UserCollection's delete_user method with invalid user
        """
        # fake id to delete
        delete_id = "faketestuser"
        # delete id
        delete_user_from_db = users.delete_user(self.db)
        response = delete_user_from_db(user_id = delete_id)
        # assure nothing was deleted
        self.assertEqual(response, False)

    def test_usercollect_search_valid_user(self):
        """
        Test for UserCollection's search_user method with a valid user
        """
        # search for this id
        search_id = "testuser"
        # search for user with search_id
        search_for_user = users.search_user(self.db)
        response = search_for_user(user_id = search_id)
        # assure user was found
        self.assertEqual(response["user_id"], search_id)

    def test_usercollect_search_invalid_user(self):
        """
        Test for UserCollection's search_user method with an invalid user
        """
        # try to search for this id
        search_id = "faketestuser"
        # search for user with search_id
        search_for_user = users.search_user(self.db)
        response = search_for_user(user_id = search_id)
        # assure user was not found
        self.assertEqual(response, None)
