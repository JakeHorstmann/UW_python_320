"""
Test class to test verify_input.py
"""

import unittest
import verify_input

class TestVerifyInputText(unittest.TestCase):
    """
    Testing class for verify_inpu.py's functions that take in text
    """

    def test_verify_text_length_valid(self):
        """
        Tests verify_text_length with a valid length
        """
        test_text = "hello I am awesome"
        result = verify_input.verify_text_length(test_text)[0]
        self.assertEqual(result, True)

    def test_verify_text_length_invalid(self):
        """
        Tests verify_text_length with an invalid length
        """
        # pylint: disable=C0301
        test_text = "hellooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooooo"
        result = verify_input.verify_text_length(test_text)[0]
        self.assertEqual(result, False)

    def test_verify_key_field_valid(self):
        """
        Tests verify_key_field with a valid key
        """
        test_key = "footballlover"
        result = verify_input.verify_key_field(test_key)[0]
        self.assertEqual(result, True)

    def test_verify_key_field_valid_underscore(self):
        """
        Tests verify_key_field with a valid key that has an underscore
        """
        test_key = "football_lover"
        result = verify_input.verify_key_field(test_key)[0]
        self.assertEqual(result, True)

    def test_verify_key_field_invalid_character(self):
        """
        Tests verify_key_field with an invalid key (@ sign)
        """
        test_key = "football@lover"
        result = verify_input.verify_key_field(test_key)[0]
        self.assertEqual(result, False)

    def test_verify_text_is_not_empty(self):
        """
        Test verify_text_is_not_empty with a string that is not empty
        """
        test_text = "hello"
        result = verify_input.verify_text_is_not_empty(test_text)[0]
        self.assertEqual(result, True)

    def test_verify_text_is_empty(self):
        """
        Test verify_text_is_not_empty with a string that is empty
        """
        test_text = ""
        result = verify_input.verify_text_is_not_empty(test_text)[0]
        self.assertEqual(result, False)

    def test_verify_email_format_valid(self):
        """
        Test verify_email_format with a valid email format
        """
        test_email = "hello@gmail.com"
        result = verify_input.verify_email_format(test_email)[0]
        self.assertEqual(result, True)

    def test_verify_email_format_invalid(self):
        """
        Test verify_email_format with invalid email formats
        """
        test_email = "hellogmail.com"
        result = verify_input.verify_email_format(test_email)[0]
        self.assertEqual(result, False)
        test_email = "hello@gmailcom"
        result = verify_input.verify_email_format(test_email)[0]
        self.assertEqual(result, False)
        test_email = "hellogmailcom"
        result = verify_input.verify_email_format(test_email)[0]
        self.assertEqual(result, False)

    def test_verify_file_path_valid(self):
        """
        Test verify_file_path with a valid path
        NEED TO REMOVE DEPENDENCE TO ACTUAL FILE
        """
        test_path = "main.py"
        result = verify_input.verify_file_path(test_path)[0]
        self.assertEqual(result, True)

    def test_verify_file_path_invalid(self):
        """
        Test verify_file_path with an invalid path
        """
        test_path = "invalid/path.csv"
        result = verify_input.verify_file_path(test_path)[0]
        self.assertEqual(result, False)

    def test_verify_csv_file_valid(self):
        """
        Test verify_csv_file with a valid file
        NEED TO REMOVE DEPENDENCE TO ACTUAL CSV
        """
        test_path = "accounts.csv"
        result = verify_input.verify_csv_file(test_path)[0]
        self.assertEqual(result, True)

    def test_verify_csv_file_invalid(self):
        """
        Test verify_csv_file with an invalid file
        """
        test_path = "fake/accounts.csv"
        result = verify_input.verify_csv_file(test_path)[0]
        self.assertEqual(result, False)
