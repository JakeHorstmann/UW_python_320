"""
Test class to test user_status.py
"""
# pylint: disable=R0903, E0401
import unittest
from playhouse.dataset import DataSet
import user_status

USER_TABLE = "UserModel"
STATUS_TABLE = "StatusModel"

class TestUserStatus(unittest.TestCase):
    """
    Testing class for user_status.py
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
        db[STATUS_TABLE].insert(id = 1,
                                status_id = "testuser_00001",
                                user_id = "testuser",
                                status_text = "test text")
        db[STATUS_TABLE].create_index(["status_id"], unique = True)
        self.db = db

    def tearDown(self):
        """
        Tear down function to reset database
        """
        self.db.close()

    def test_statuscollection_add_valid_status(self):
        """
        Test for StatusCollection's add_status method with good data
        """
        # create test status to add to user collection
        test_status_id = "testuser_00002"
        test_id = "testuser"
        test_text = "this is my second entry!"
        # add in test data
        add_status_to_db = user_status.add_status(self.db)
        response = add_status_to_db(status_id = test_status_id,
                                    user_id = test_id,
                                    status_text = test_text)
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
        add_status_to_db = user_status.add_status(self.db)
        response = add_status_to_db(status_id = test_status_id,
                                    user_id = test_id,
                                    status_text = test_text)
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
        add_status_to_db = user_status.add_status(self.db)
        response = add_status_to_db(status_id = test_status_id,
                                    user_id = test_id,
                                    status_text = test_text)
        # assure status was not added
        self.assertEqual(response, False)

    def test_statuscollect_update_valid_status(self):
        """
        Test for StatusCollection's modify_status method with good status
        """
        # update status to have more enthusiasm
        modify_status_id = "testuser_00001"
        modified_id = "testuser"
        modified_text = "My first status post!!!!"
        # modify status in status_collection
        update_status_in_db = user_status.update_status(self.db)
        response = update_status_in_db(status_id = modify_status_id,
                                       user_id = modified_id,
                                       status_text = modified_text)
        # assure status was modified correctly
        self.assertEqual(response, True)

    def test_statuscollect_update_invalid_status(self):
        """
        Test for StatusCollection's modify_status method with bad status
        """
        # try to modify a status that DNE
        modify_status_id = "testuser_99999"
        modified_id = "testuser"
        modified_text = "this better not work"
        # modify status in user_status_collection
        update_status_in_db = user_status.update_status(self.db)
        response = update_status_in_db(status_id = modify_status_id,
                                       user_id = modified_id,
                                       status_text = modified_text)
        # assure status was not modified
        self.assertEqual(response, False)

    def test_statuscollect_update_status_no_foreign_key(self):
        """
        Test for StatusCollection's modify_status method with an invalid foreign key
        """
        # create test status that has invalid user
        modify_status_id = "testuser_00001"
        modified_id = "testuserthatDNE"
        modified_text = "this better not work"
        # try to modify status
        update_status_in_db = user_status.update_status(self.db)
        response = update_status_in_db(status_id = modify_status_id,
                                       user_id = modified_id,
                                       status_text = modified_text)
        # assure status was not added
        self.assertEqual(response, False)

    def test_statuscollect_delete_valid_status(self):
        """
        Test for StatusCollection's delete_status method with valid status
        """
        # status id to delete
        delete_status_id = "testuser_00001"
        # delete status
        delete_status_from_db = user_status.delete_status(self.db)
        response = delete_status_from_db(status_id = delete_status_id)
        # assure status was deleted
        self.assertEqual(response, True)

    def test_statuscollect_delete_invalid_status(self):
        """
        Test for StatusCollection's delete_status method with invalid status
        """
        # set up invalid status id
        delete_status_id = "testuser_99999"
        # try to delete fake id
        delete_status_from_db = user_status.delete_status(self.db)
        response = delete_status_from_db(status_id = delete_status_id)
        # assure nothing was deleted
        self.assertEqual(response, False)

    def test_statuscollect_search_valid_status(self):
        """
        Test for StatusCollection's search_status method
        """
        # search for this status
        search_status_id = "testuser_00001"
        # search for status with search_id
        search_status_in_db = user_status.search_status(self.db)
        response = search_status_in_db(status_id = search_status_id)
        # assure status was found
        self.assertEqual(response["status_id"], search_status_id)

    def test_statuscollect_search_invalid_status(self):
        """
        Test for StatusCollection's search_status method with invalid status
        """
        # set up invalid status id
        search_status_id = "testuser_99999"
        # search for status with search_id
        search_status_in_db = user_status.search_status(self.db)
        response = search_status_in_db(status_id = search_status_id)
        # assure status was not found
        self.assertEqual(response, None)
