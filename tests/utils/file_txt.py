import os
import sys
import unittest

parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)
from utils.file_txt import parse_text_file
from pathlib import Path

class TestParseTextFile(unittest.TestCase):
    def test_parse_text_file_newline_separator(self):
        # Test parsing with newline separator
        expected_emails = ['email1@example.com', 'email2@example.com', 'email3@example.com']
        actual_emails = parse_text_file(str(Path("./tests/resource/test_data_newline.txt")))
        self.assertEqual(actual_emails, expected_emails)

    def test_parse_text_file_comma_separator(self):
        # Test parsing with comma separator
        expected_emails = ['email1@example.com', 'email2@example.com', 'email3@example.com']
        actual_emails = parse_text_file(str(Path("./tests/resource/test_data_comma.txt")), sep=",")
        self.assertEqual(actual_emails, expected_emails)

    def test_parse_text_file_semicolon_separator(self):
        # Test parsing with semicolon separator
        expected_emails = ['email1@example.com', 'email2@example.com', 'email3@example.com']
        actual_emails = parse_text_file(str(Path("./tests/resource/test_data_semicolon.txt")), sep=";")
        self.assertEqual(actual_emails, expected_emails)

if __name__ == '__main__':
    unittest.main()