import unittest
from unittest.mock import patch, MagicMock
import os
import sys
from dotenv import load_dotenv
from pathlib import Path
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)
from src.emails.main import *

# Load variables from the specified .env file
load_dotenv(dotenv_path=str(Path("./env/tests.env")))

# Access the variables
sender_email = os.getenv("EMAIL_SENDER_UNIT_TEST")
sender_password = os.getenv("PASSWORD_UNIT_TEST")
receive_email = os.getenv("EMAIL_RECEIVER_UNIT_TEST")

class TestEmailFunctions(unittest.TestCase):
    def test_message_from_file(self):
        expected_html_message = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Template</title>
</head>
<body>
    <h1>Welcome, John Doe!</h1>
    <p>This is a message for ACME Inc</p>
    <p>Here is some information about your company:</p>
    <ul>
        <li>Contact Name: John Doe</li>
        <li>Company Name: ACME Inc</li>
        <li>Sector of Activity: DEVELOPMENT INFORMATIQUE</li>
    </ul>
    <p>Contact details:</p>
    <ul>
        <li>Email: john@example.com</li>
        <li>Phone: 123456789</li>
        <li>Name: John</li>
        <li>LinkedIn: linkedin.com/johndoe</li>
    </ul>
</body>
</html>
"""
        html_message = message_from_file("John Doe", "ACME Inc", "DEVELOPMENT INFORMATIQUE", "john@example.com", "123456789", "John", "linkedin.com/johndoe", str(Path("./tests/resource/message.html")))
        self.assertEqual(html_message, expected_html_message)

    def test_send_email_smtp(self):
        expected_result = True
        with patch('smtplib.SMTP') as mock_smtp:
            instance = mock_smtp.return_value
            instance.sendmail.return_value = None
            result = send_email_smtp(sender_email, sender_password, receive_email, "Subject", "Hello *Body*")
            self.assertEqual(result, expected_result)

    def test_message_from_html(self):
        expected_html_message = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Template</title>
</head>
<body>
    <p>Email: test@example.com</p>
    <p>Phone: 123456789</p>
    <p>Name: John</p>
    <p>LinkedIn: linkedin.com/johndoe</p>
</body>
</html>
"""
        html_message = message_from_html("test@example.com", "123456789", "John", "linkedin.com/johndoe", str(Path("./tests/resource/message-ws.html")))
        self.assertEqual(html_message, expected_html_message)

    def test_is_password_structure(self):
        self.assertTrue(is_password_structure("abcd efgh ijkl mnop"))
        self.assertFalse(is_password_structure("abcd efgh ijkl"))
        self.assertFalse(is_password_structure("abc defg ijkl mnop"))

    @patch('smtplib.SMTP')
    def test_check_gmail_connection(self, mock_smtp):
        instance = mock_smtp.return_value
        instance.starttls.return_value = None
        instance.login.return_value = None
        instance.quit.return_value = None
        self.assertTrue(check_gmail_connection(sender_email, sender_password))
        instance.starttls.assert_called_once()
        instance.login.assert_called_once_with(sender_email, sender_password)
        instance.quit.assert_called_once()
    
    def test_is_valid_email(self):
        self.assertTrue(is_valid_email(sender_email))
        self.assertFalse(is_valid_email("test.example.com"))

if __name__ == '__main__':
    unittest.main()
