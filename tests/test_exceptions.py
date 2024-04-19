import os
import sys
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)
import subprocess
import pytest
import requests
from src.exceptions import PasswordException,FileExtensionException,FileNotFoundException
import os
import sys
import pytest
from fastapi.testclient import TestClient
from src.main import app  # Replace 'your_fastapi_module' with the actual module name

parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)

client = TestClient(app)

@pytest.fixture
def valid_files():
    return {
        "emails": ("test_emails.txt", b"test content"),
        "messages": ("test_messages.html", b"test content"),
        "resume": ("test_resume.pdf", b"test content")
    }

@pytest.fixture
def invalid_files():
    return {
        "emails": ("test_emails.csv", b"test content"),
        "messages": ("test_messages.txt", b"test content"),
        "resume": ("test_resume.docx", b"test content")
    }

def test_valid_request(valid_files):
    sender_email = "example@example.com"
    sender_password = "valid_password"
    email_subject = "Test Subject"

    response = client.post(
        "/send/",
        files=[
            ("emails", valid_files["emails"]),
            ("messages", valid_files["messages"]),
            ("resume", valid_files["resume"]),
        ],
        data={"sender_email": sender_email, "sender_password": sender_password, "email_subject": email_subject}
    )
    assert response.status_code == 200
    assert response.json() == {
        "emails_filename": "test_emails.txt",
        "messages_filename": "test_messages.html",
        "resume_filename": "test_resume.pdf"
    }

def test_invalid_file_extensions(invalid_files):
    sender_email = "example@example.com"
    sender_password = "valid_password"
    email_subject = "Test Subject"

    for field, (filename, content) in invalid_files.items():
        response = client.post(
            "/send/",
            files=[(field, (filename, content))],
            data={"sender_email": sender_email, "sender_password": sender_password, "email_subject": email_subject}
        )
        assert response.status_code == 422  # Unprocessable Entity

def test_invalid_password_structure(valid_files):
    sender_email = "example@example.com"
    sender_password = "invalid password"
    email_subject = "Test Subject"

    response = client.post(
        "/send/",
        files=[
            ("emails", valid_files["emails"]),
            ("messages", valid_files["messages"]),
            ("resume", valid_files["resume"]),
        ],
        data={"sender_email": sender_email, "sender_password": sender_password, "email_subject": email_subject}
    )
    assert response.status_code == 422  # Unprocessable Entity

# Add more test cases as needed

if __name__ == "__main__":
    pytest.main()
