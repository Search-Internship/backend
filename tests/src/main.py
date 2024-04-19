import os
import sys
import unittest
from fastapi.testclient import TestClient

parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)

from src.main import app  # Assuming your FastAPI app is defined in main.py
from dotenv import load_dotenv
from pathlib import Path

# Load variables from the specified .env file
load_dotenv(dotenv_path=str(Path("./tests/.env")))

# Access the variables
sender_email = os.getenv("EMAIL_SENDER_UNIT_TEST")
sender_password = os.getenv("PASSWORD_UNIT_TEST")
class TestEmailEndpoint(unittest.TestCase):
    def setUp(self):
        self.client = TestClient(app)

    def test_index(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_missing_files(self):
        response = self.client.post("/send/")
        self.assertEqual(response.status_code, 422)  # Expecting Unprocessable Entity status code for missing files

    def test_invalid_file_extensions(self):
        # Sending invalid file extensions
        files = {
            'emails': ('invalid_file.txt', b'file content'),
            'resume': ('invalid_file.txt', b'file content'),
        }
        form_data = {
            'sender_email': 'example@example.com',
            'sender_password': 'xxxx xxxx xxxx',
            'email_subject': 'Test Subject',
            'email_body': 'file content',
            'file_separator':"\n"
        }
        response = self.client.post("/send/", files=files, data=form_data)
        self.assertEqual(response.status_code, 422)  # Expecting Unprocessable Entity status code for invalid file extensions
        
    def test_invalid_email(self):
        # Sending valid files and form data
        files = {
            'emails': ('test_emails.txt', b'file content'),
            'resume': ('test_resume.pdf', b'file content'),
        }
        form_data = {
            'sender_email': 'exampleexample.com',
            'sender_password': 'xxxx xxxx xxxx xxxx',
            'email_subject': 'Test Subject',
            'email_body': 'file content',
            'file_separator':"\n"
        }
        response = self.client.post("/send/", files=files, data=form_data)
        self.assertEqual(response.status_code, 422)  # Expecting OK status code for a valid request

    def test_invalid_password(self):
        # Sending valid files and form data
        files = {
            'emails': ('test_emails.txt', b'file content'),
            'resume': ('test_resume.pdf', b'file content'),
        }
        form_data = {
            'sender_email': 'example@example.com',
            'sender_password': 'xxxx xxxx xxxx',
            'email_subject': 'Test Subject',
            'email_body': 'file content',
            'file_separator':"\n"
        }
        response = self.client.post("/send/", files=files, data=form_data)
        self.assertEqual(response.status_code, 422)  # Expecting OK status code for a valid request

    def test_email_connection(self):
        # Sending valid files and form data
        files = {
            'emails': ('test_emails.txt', b'file content'),
            'resume': ('test_resume.pdf', b'file content'),
        }
        form_data = {
            'sender_email': 'example@example.com',
            'sender_password': 'xxxx xxxx xxxx xxxx',
            'email_subject': 'Test Subject',
            'email_body': 'file content',
            'file_separator':"\n"
        }
        response = self.client.post("/send/", files=files, data=form_data)
        self.assertEqual(response.status_code, 601)  # Expecting OK status code for a valid request

    def test_valid_request(self):
        # Sending valid files and form data
        files = {
            'emails': ('test_emails.txt', b'file content'),
            'resume': ('test_resume.pdf', b'file content'),
        }
        form_data = {
            'sender_email': sender_email,
            'sender_password': sender_password,
            'email_subject': 'Test Subject',
            'email_body': 'file content',
            'file_separator':"\n"
        }
        response = self.client.post("/send/", files=files, data=form_data)
        self.assertEqual(response.status_code, 200)  # Expecting OK status code for a valid request

    





if __name__ == '__main__':
    unittest.main()