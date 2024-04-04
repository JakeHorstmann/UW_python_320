"""
Tests UserCollection methods from users.py
"""
import io
from unittest.mock import patch
from unittest import TestCase
import users
from test_database_model import drop_tables, create_tables, close_connection
from playhouse.dataset import DataSet

ds = DataSet('sqlite:///test_database.db')
test_user_table = ds['testusers']

class TestUsers(TestCase):
    """Class for testing UserCollection methods from users.py"""
    def setUp(self):
        create_tables()


    def tearDown(self):
        drop_tables()
        close_connection()

    def test_add_user(self):
        """Tests users.add_user"""
        add_user = users.add_user(test_user_table)
        self.assertTrue(add_user(user_id="jlpicard",
                                 user_name="Jean Luc",
                                 user_last_name="picard",
                                 user_email="jlpicard@starfleet.com"))
        self.assertTrue(test_user_table.find_one(user_id="jlpicard"))


    def test_add_user_duplicate(self):
        """Tests users.add_user when adding duplicate user"""
        add_user = users.add_user(test_user_table)
        add_user(user_id="bcrusher",
                 user_name="Beverly",
                 user_last_name="Crusher",
                 user_email="bcrusher@starfleet.com")
        add_user1 = users.add_user(test_user_table)
        self.assertFalse(add_user1(user_id="bcrusher",
                                   user_email="bevc@enterprise.com",
                                   user_name="Bev",
                                   user_last_name="c"))
        with patch("sys.stdout", new=io.StringIO()) as mock_stdout:
            add_user = users.add_user(test_user_table)
            add_user(user_id="bcrusher",
                     user_email="glaforge@enterprise.com",
                     user_name="Geordi",
                     user_last_name="Laforge")
            self.assertEqual("ERROR: User bcrusher already exists",
                             mock_stdout.getvalue().strip().split("\n")[0])

    def test_modify_user_user_does_not_exist(self):
        """Tests user_status.modify_user"""
        update_user = users.modify_user(test_user_table)
        self.assertFalse(
            update_user(user_id="wcrusher",
                        user_email="wcrusher@starfleetacademy.edu",
                        user_name="Wesley",
                        user_last_name="Crusher")
        )

    def test_modify_user(self):
        add_user = users.add_user(test_user_table)
        add_user(user_id="glaforge",
                 user_name="Geordi",
                 user_last_name="Laforge",
                 user_email="glaforge@enterprise.com")
        test_user_table.find_one(user_id="glaforge")
        update_user = users.modify_user(test_user_table)
        self.assertTrue(update_user(user_id="glaforge",
                                    user_name="Jeordi",
                                    user_last_name="la forge",
                                    user_email="glaforge@starfleet.com"))
        result = test_user_table.find_one(user_id="glaforge")
        self.assertEqual(result['user_email'], "glaforge@starfleet.com")
        self.assertEqual(result['user_name'], "Jeordi")


    def test_delete_user(self):
        """Tests UserCollection.delete_user"""
        add_user = users.add_user(test_user_table)
        add_user(user_id="glaforge",
                 user_name="Geordi",
                 user_last_name="Laforge",
                 user_email="glaforge@enterprise.com")
        delete_user = users.delete_user(test_user_table)
        self.assertTrue(delete_user(user_id="glaforge"))
        self.assertFalse(delete_user(user_id="not_a_user"))

    def test_delete_user_does_not_exist(self):
        """Tests UserCollection.delete_user when user does not exist"""
        add_user = users.add_user(test_user_table)
        add_user(user_id="glaforge",
                 user_name="Geordi",
                 user_last_name="Laforge",
                 user_email="glaforge@enterprise.com")
        delete_user = users.delete_user(test_user_table)
        self.assertFalse(delete_user(user_id="not_a_user"))

    def test_search_user(self):
        """Tests UserCollection.search_user"""
        add_user = users.add_user(test_user_table)
        add_user(user_id="bcrusher",
                 user_name="Beverly",
                 user_last_name="Crusher",
                 user_email="bcrusher@starfleet.com")
        search_user = users.search_user(test_user_table)
        self.assertTrue(search_user(user_id="bcrusher"))
        bev_crusher = search_user(user_id="bcrusher")
        self.assertEqual(bev_crusher['user_email'], "bcrusher@starfleet.com")
        self.assertEqual(bev_crusher['user_last_name'], "Crusher")
        self.assertEqual(bev_crusher['user_name'], "Beverly")

    def test_search_user_user_does_not_exist(self):
        search_user = users.search_user(test_user_table)
        self.assertEqual(search_user(user_id="not_a_user"), None)
