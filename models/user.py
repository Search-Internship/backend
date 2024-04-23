import uuid
from sqlalchemy import Column, String,inspect
from passlib.hash import sha256_crypt
from cryptography.fernet import Fernet  # For encryption
import os
import sys

parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)
from database import session
from sqlalchemy.ext.declarative import declarative_base


# Base class for ORM
Base = declarative_base()
# Define User model
class User(Base):
    __tablename__ = 'users'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String)
    email = Column(String)
    linkedin_link = Column(String)
    password_hash = Column(String)
    phone_number = Column(String, unique=True)
    email_password = Column(String)  # Store encrypted email password

    def set_password(self, password):
        # Hashing the password
        self.password_hash = sha256_crypt.hash(password)

    def check_password(self, password):
        # Verifying the password
        return sha256_crypt.verify(password, self.password_hash)

    def set_email_password(self, email_password, encryption_key):
        # Encrypt the email password
        cipher_suite = Fernet(encryption_key)
        self.email_password = cipher_suite.encrypt(email_password.encode()).decode()

    def get_email_password(self, encryption_key):
        # Decrypt the email password
        cipher_suite = Fernet(encryption_key)
        decrypted_password = cipher_suite.decrypt(self.email_password.encode()).decode()
        return decrypted_password

    @classmethod
    def create_user(cls, username, email, linkedin_link, password, phone_number, email_password, encryption_key):
        # Create a new user instance
        new_user = cls(
            username=username,
            email=email,
            linkedin_link=linkedin_link,
            phone_number=phone_number
        )
        # Set password and email password
        new_user.set_password(password)
        new_user.set_email_password(email_password, encryption_key)

        # Add the user to the database
        session.add(new_user)
        session.commit()

    @classmethod
    def verify_login(cls, username_or_email, password, encryption_key):
        # Find user by username or email
        user = session.query(cls).filter((cls.username == username_or_email) | (cls.email == username_or_email)).first()
        if user:
            # Verify password
            if user.check_password(password):
                # Decrypt and return email password
                email_password = user.get_email_password(encryption_key)
                return True, email_password
        return False, None
