"""
Functions for verifying input coming in
"""

import re
from pathlib import Path

def verify_text_length(text, length = 50):
    """
    Verifies the length of text
    """
    if len(text) <= length:
        return True, ""
    return False, f"Text length is over the {length} character limit"

def verify_key_field(key):
    """
    Verifies can be a valid key
    """
    regex = r"^[A-Za-z0-9_.]+$"
    if re.fullmatch(regex, key):
        return True, ""
    return False, "Key does not only contain letters, numbers, and underscores"

def verify_text_is_not_empty(text):
    """
    Verifies that a text is not empty
    """
    if text != "":
        return True, ""
    return False, "Text is empty"

def verify_email_format(email):
    """
    Verifies the format of an email
    """
    regex = r"[A-Za-z0-9._]+@[A-Za-z0-9-]+\.[A-Za-z]+$"
    if re.fullmatch(regex, email):
        return True, ""
    return False, "Email does not have a valid format"

def verify_file_path(path):
    """
    Verifies the path to a file is valid
    """
    if Path(path).is_file():
        return True, ""
    return False, "File path is invalid"

def verify_csv_file(path):
    """
    Verifies a path is to a valid CSV
    """
    if path[-4:] == ".csv":
        if verify_file_path(path)[0]:
            return True, ""
        return False, "File path is invalid"
    if verify_file_path(path)[0]:
        return False, "File is not a valid CSV"
    return False, "File is not a valid path to a CSV"

def verify_user_id(user_id):
    """
    Verifies a user_id
    """
    is_not_empty, empty_msg = verify_text_is_not_empty(user_id)
    is_good_length, length_msg = verify_text_length(user_id, length=30)
    is_key, key_msg = verify_key_field(user_id)

    error_msg = ". ".join([empty_msg, length_msg, key_msg])
    valid_user_id = is_not_empty and is_good_length and is_key

    return valid_user_id, error_msg

def verify_email(email):
    """
    Verifies an email
    """
    is_not_empty, empty_msg = verify_text_is_not_empty(email)
    is_good_length, length_msg = verify_text_length(email, length=50)
    is_email, email_msg = verify_email_format(email)
    error_msg = ". ".join([empty_msg, length_msg, email_msg])
    valid_email = is_not_empty and is_good_length and is_email

    return valid_email, error_msg

def verify_user_name(user_name):
    """
    Verifies a user's name
    """
    is_not_empty, empty_msg = verify_text_is_not_empty(user_name)
    is_good_length, length_msg = verify_text_length(user_name, length=30)

    error_msg = ". ".join([empty_msg, length_msg])
    valid_user_name = is_not_empty and is_good_length

    return valid_user_name, error_msg

def verify_user_last_name(last_name):
    """
    Verifies a user's last name
    """
    is_not_empty, empty_msg = verify_text_is_not_empty(last_name)
    is_good_length, length_msg = verify_text_length(last_name, length=100)

    error_msg = ". ".join([empty_msg, length_msg])
    valid_last_name = is_not_empty and is_good_length

    return valid_last_name, error_msg

def verify_status_id(status_id):
    """
    Verifies a status id
    """
    is_not_empty, empty_msg = verify_text_is_not_empty(status_id)
    is_good_length, length_msg = verify_text_length(status_id, length=30)
    is_key, key_msg = verify_key_field(status_id)

    error_msg = ". ".join([empty_msg, length_msg, key_msg])
    valid_status_id = is_not_empty and is_good_length and is_key

    return valid_status_id, error_msg

def verify_status_text(status_text):
    """
    Verifies a status text
    """
    is_not_empty, empty_msg = verify_text_is_not_empty(status_text)
    is_good_length, length_msg = verify_text_length(status_text, length=100)

    error_msg = ". ".join([empty_msg, length_msg])
    valid_status_text = is_not_empty and is_good_length

    return valid_status_text, error_msg

def verify_yes_or_no(text):
    """
    Verifies if a text is Y/N
    """
    return True if text.lower() in ["y", "n"] else False

def verify_tag(tag):
    """
    Verify a picture tag
    """
    regex = r"^[A-Za-z_]+$"
    if re.fullmatch(regex, tag):
        return True, ""
    return False, "Tag does not only contain letters and underscores"
