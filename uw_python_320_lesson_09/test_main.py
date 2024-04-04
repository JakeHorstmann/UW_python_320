"""
Tests methods from main.py
"""
import io
from unittest import TestCase
from unittest.mock import Mock, patch, mock_open
from peewee import SqliteDatabase
import main
import users
import user_status
from playhouse.dataset import DataSet
from test_database_model import create_tables, close_connection, drop_tables


##IMPORTANT NOTE:
# To access the test database test_database.db, comment out
# Run test_database_model.py before running these tests


ds = DataSet('sqlite:///test_database.db')
test_status_table = ds['teststatus']
test_user_table = ds['testusers']


class TestMain(TestCase):
    """Class for testing main.py"""

    def setUp(self):
        create_tables()

    def tearDown(self):
        drop_tables()
        close_connection()

    def test_load_users(self):
        """Tests main.load_users() with mock data"""
        self.assertTrue(main.load_users("test_accounts.csv", table=test_user_table))
        janeway = test_user_table.find_one(user_id="kjaneway")
        self.assertEqual(janeway['user_email'], "kjaneway@voyager.com")
        self.assertEqual(janeway['user_name'], "Katherine")
        self.assertEqual(janeway['user_last_name'], "Janeway")

    def test_load_users_file_not_found(self):
        """Tests main.load_users() FileNotFound error"""
        with patch('sys.stdout', new_callable=io.StringIO) as mock_stdout:
            with patch('main.open', mock_open()) as mock_file:
                mock_file.side_effect = FileNotFoundError
                main.load_users("test_accounts.csv", table=test_user_table)
                self.assertEqual(["The file was not found"],
                                 mock_stdout.getvalue().strip().split("\n"))

    def test_load_users_duplicate_user(self):
        """Tests main.load_users() with a duplicate user"""
        main.add_user(user_id="bcrusher",
                      user_email="bcrusher@enterprise.com",
                      user_name="beverly",
                      user_last_name="crusher",
                      table=test_user_table)
        main.load_users("test_accounts.csv", table=test_user_table)
        self.assertEqual(len(test_user_table), 2)


    def test_load_status_updates(self):
        """Tests main.load_status_updates with mock data"""
        #Add one user, test status file contains statuses for 2 users.  Only one record should be saved
        test_user_table.insert(user_id="bcrusher",
                               user_email="bcrusher@enterprise.com",
                               user_name="beverly",
                               user_last_name="crusher")
        #Load status updates from csv
        main.load_status_updates("test_status_updates.csv", table_status=test_status_table, table_users=test_user_table)
        self.assertEqual(len(test_status_table), 1)
        crusher_status = test_status_table.find_one(status_id="brcusher001")
        self.assertEqual(crusher_status["status_text"], "Medical emergency on deck 4")

    def test_load_status_updates_file_not_found(self):
        """Tests main.load_status_updates when a file is not found"""
        with patch('sys.stdout', new=io.StringIO()) as mock_stdout:
            with patch('main.open', new=mock_open()) as mock_file:
                mock_file.side_effect = FileNotFoundError
                main.load_status_updates("status_updates.csv", table_status=test_status_table, table_users=test_user_table)
                self.assertEqual(["The file was not found"], mock_stdout.getvalue().strip().split("\n"))

    def test_add_user(self):
        """Tests main.add_user()"""
        self.assertTrue(main.add_user(user_id="bcrusher",
                                      user_email="bcrusher321@gmail.com",
                                      user_name="Beverly",
                                      user_last_name="Crusher",
                                      table=test_user_table,
                                      ))
        self.assertFalse(main.add_user(user_id="bcrusher",
                                       user_email="email",
                                       user_name="bev",
                                       user_last_name="crusher",
                                       table=test_user_table))
        result = test_user_table.find_one(user_id="bcrusher")
        self.assertEqual(result['user_email'], "bcrusher321@gmail.com")
        self.assertEqual(result['user_name'], "Beverly")
        self.assertEqual(result['user_last_name'], "Crusher")


    def test_update_user(self):
        """Tests main.update_user()"""
        test_user_table.insert(user_id="jlpicard",
                               user_email="jp@enterprise.com",
                               user_name="jeanluc",
                               user_last_name="picard")
        self.assertTrue(main.update_user(user_id="jlpicard",
                                         email="jpicard@starfleet.net",
                                         user_name="Jean-Luc",
                                         user_last_name="Picard",
                                         table=test_user_table
                                         ))
        result = test_user_table.find_one(user_id="jlpicard")
        self.assertEqual(result['user_email'], "jpicard@starfleet.net")
        self.assertEqual(result['user_name'], "Jean-Luc")
        self.assertEqual(result['user_last_name'], "Picard")

    def test_update_user_user_does_not_exist(self):
        self.assertFalse(main.update_user(user_id="no_user",
                         email="no_user@email.com",
                         user_name="No",
                         user_last_name="User",
                         table=test_user_table))

    def test_delete_user(self):
        """Tests main.delete_user()"""
        test_user_table.insert(user_id="jlpicard",
                               user_email="jp@enterprise.com",
                               user_name="jeanluc",
                               user_last_name="picard")
        self.assertTrue(main.delete_user("jlpicard", table_users=test_user_table, table_status=test_status_table))

    def test_delete_user_user_does_not_exist(self):
        self.assertFalse(main.delete_user("boboblaw", table_users=test_user_table, table_status=test_status_table))

    def test_search_user(self):
        """Tests main.search_user()"""
        test_user_table.insert(user_id="jlpicard",
                               user_email="jp@enterprise.com",
                               user_name="jeanluc",
                               user_last_name="picard")
        result = main.search_user(user_id="jlpicard", table=test_user_table)
        self.assertEqual(result["user_id"], "jlpicard")
        self.assertEqual(result["user_email"], "jp@enterprise.com")

    def test_add_status(self):
        """Tests main.add_status()"""
        test_user_table.insert(user_id="jlpicard",
                               user_email="jp@enterprise.com",
                               user_name="jeanluc",
                               user_last_name="picard")
        self.assertTrue(main.add_status(status_id="jlpicard002",
                                        user_id="jlpicard",
                                        status_text="Red alert!",
                                        table_status = test_status_table,
                                        table_users=test_user_table))
        self.assertFalse(main.add_status(status_id="jlpicard002",
                                         user_id="jlpicard",
                                         status_text="Did this update?",
                                         table_status = test_status_table,
                                         table_users=test_user_table))
        result = test_status_table.find_one(status_id="jlpicard002")
        self.assertEqual(result['status_text'], "Red alert!")

    def test_update_status(self):
        """Tests main.update_status()"""
        test_user_table.insert(user_id="wriker",
                               user_email="wriker@enterprise.com",
                               user_name="William",
                               user_last_name="Riker")
        self.assertTrue(main.add_status(status_id="wriker001",
                                        user_id="wriker",
                                        status_text="Red alert!",
                                        table_status=test_status_table,
                                        table_users=test_user_table))
        self.assertTrue(main.update_status(status_id="wriker001",
                                           user_id="wriker",
                                           status_text="Drinks are cancelled, red alert!",
                                           table_status=test_status_table,
                                           table_users=test_user_table))
        result = test_status_table.find_one(status_id="wriker001")
        self.assertEqual(result['status_text'], "Drinks are cancelled, red alert!")

    def update_status_status_does_not_exist(self):
        test_user_table.insert(user_id="wriker",
                               user_email="wriker@enterprise.com",
                               user_name="William",
                               user_last_name="Riker")
        main.add_status(status_id="wriker001",
                        user_id="wriker",
                        status_text="Red alert!",
                        table_status=test_status_table,
                        table_users=test_user_table)
        self.assertFalse(main.update_status(status_id="rando001",
                                            user_id="rando",
                                            status_text="I'm a rando!",
                                            table_status=test_status_table,
                                            table_users=test_user_table))

    def test_delete_status(self):
        """Tests main.delete_status()"""
        test_user_table.insert(user_id="wriker",
                               user_email="wriker@enterprise.com",
                               user_name="William",
                               user_last_name="Riker")
        main.add_status(status_id="wriker001",
                        user_id="wriker",
                        status_text="Red alert!",
                        table_status=test_status_table,
                        table_users=test_user_table)
        self.assertTrue(main.delete_status(status_id="wriker001", table=test_status_table))

    def delete_status_status_does_not_exist(self):
        self.assertFalse(main.delete_status(status_id="rando001", table=test_status_table))

    def test_search_status(self):
        """Tests main.search_status()"""
        test_user_table.insert(user_id="wriker",
                               user_email="wriker@enterprise.com",
                               user_name="William",
                               user_last_name="Riker")
        main.add_status(status_id="wriker001",
                        user_id="wriker",
                        status_text="Red alert!",
                        table_status=test_status_table,
                        table_users=test_user_table)
        self.assertTrue(main.search_status(status_id="wriker001", table=test_status_table))
