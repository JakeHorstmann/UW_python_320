"""
Tests UserStatusCollection methods from user_status.py
"""
import io
from unittest.mock import patch
from unittest import TestCase
import user_status
from test_database_model import drop_tables, create_tables, close_connection
from playhouse.dataset import DataSet

ds = DataSet('sqlite:///test_database.db')
test_status_table = ds['teststatus']

class TestUserStatus(TestCase):
    """Class for testing UserStatusCollection methods from user_status.py"""
    def setUp(self):
        create_tables()

    def tearDown(self):
        drop_tables()
        close_connection()

    def test_add_status(self):
        """Tests UserStatusCollection.add_status method"""
        add_status = user_status.add_status(test_status_table)
        self.assertTrue(add_status(status_id="wriker002",
                                   user_id="wriker",
                                   status_text="Shields up"))



    def test_add_status_already_exists(self):
        """Tests UserStatusCollection.add_status when status already exists"""
        add_status = user_status.add_status(test_status_table)
        add_status(status_id="wriker002",
                   user_id="wriker",
                   status_text="Shields up")
        self.assertFalse(add_status(status_id="wriker002",
                                    user_id="wriker",
                                    status_text="Nothing to see here"))
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            add_status(status_id="wriker002",
                       user_id="wriker",
                       status_text="Should be rejected")
            self.assertEqual("Status ID wriker002 already exists", mock_stdout.getvalue().strip().split("\n")[0])

    def test_modify_status(self):
        """Tests UserStatusCollection.modify_status method"""
        add_status = user_status.add_status(test_status_table)
        add_status(status_id="wriker001", user_id="wriker", status_text="Two to beam up!")
        update_status = user_status.modify_status(test_status_table)
        self.assertTrue(update_status(status_id="wriker001",
                                      user_id="wriker",
                                      status_text="Six to beam up!"))
        result = test_status_table.find_one(status_id="wriker001")
        self.assertEqual(result['status_text'], "Six to beam up!")

    def test_update_status_user_does_not_exist(self):
        """Tests UserStatusCollection.update_status method when user does not exist"""
        update_status = user_status.modify_status(test_status_table)
        self.assertFalse(update_status(status_id="not_a_user",
                                       user_id="fake_user",
                                       status_text="This should not be saved"))

    def test_update_status_status_does_not_exist(self):
        """Tests UserStatusCollection.update_status method when status does not exist"""
        update_status = user_status.modify_status(test_status_table)
        self.assertFalse(update_status(status_id="not_a_status"))

    def test_delete_status(self):
        """Tests UserStatusCollection.delete_status method"""
        add_status = user_status.add_status(test_status_table)
        add_status(status_id="wriker002",
                   user_id="wriker",
                   status_text="Shields up")
        delete_status = user_status.delete_status(test_status_table)
        self.assertTrue(delete_status(status_id="wriker002"))

    def test_delete_status_does_not_exist(self):
        """Tests UserStatusCollection.delete_status method when status does not exist"""
        delete_status = user_status.delete_status(test_status_table)
        self.assertFalse(delete_status(status_id="mylittlepony001"))


    def test_search_status(self):
        """Tests UserStatusCollection.search_status method"""
        add_status = user_status.add_status(test_status_table)
        add_status(status_id="jlpicard001", user_id="jlpicard", status_text="Engage")
        search_status = user_status.search_status(test_status_table)
        self.assertTrue(search_status(status_id="jlpicard001"))
        result = search_status(status_id="jlpicard001")
        self.assertEqual(result['status_text'], "Engage")

        # self.assertEqual(self.status_collection_instance.search_status(status_id="not_a_user").user_id, None)
        # self.assertEqual(self.status_collection_instance.search_status(status_id="not_a_user").status_text, None)
        # self.assertEqual(self.status_collection_instance.search_status(status_id="not_a_user").status_id, None)
