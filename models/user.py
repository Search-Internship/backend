import uuid
from sqlalchemy import Column, String,inspect
from passlib.hash import sha256_crypt
from cryptography.fernet import Fernet  # For encryption
import os
import sys
from typing import Union
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)
from database import session
from sqlalchemy.ext.declarative import declarative_base


# Base class for ORM
Base = declarative_base()
# Define User model
class User(Base):
    """
    User model representing a user in the database.

    Attributes:
        id (str): Unique identifier for the user.
        username (str): User's username.
        email (str): User's email address (unique).
        linkedin_link (str): User's LinkedIn profile link.
        password_hash (str): Hashed password for user authentication.
        phone_number (str): User's phone number.
        email_password (str): Encrypted email password.
    """
    __tablename__ = 'users'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String)
    email = Column(String,unique=True)
    linkedin_link = Column(String)
    password_hash = Column(String)
    phone_number = Column(String)
    email_password = Column(String)  # Store encrypted email password

    def set_password(self, password:str)->None:
        """
        Set the password for the user.

        Parameters:
            password (str): The password to set.
        """
        # Hashing the password
        self.password_hash = sha256_crypt.hash(password)

    def check_password(self, password:str)->None:
        """
        Check if the provided password matches the user's hashed password.

        Parameters:
            password (str): The password to verify.

        Returns:
            bool: True if the password is correct, False otherwise.
        """
        # Verifying the password
        return sha256_crypt.verify(password, self.password_hash)

    def set_email_password(self, email_password:str, encryption_key:str)->None:
        """
        Encrypt and set the email password for the user.

        Parameters:
            email_password (str): The email password to encrypt.
            encryption_key (str): The encryption key to use.
        """
        # Encrypt the email password
        cipher_suite = Fernet(encryption_key)
        self.email_password = cipher_suite.encrypt(email_password.encode()).decode()

    def get_email_password(self, encryption_key:str)->str:
        """
        Decrypt and retrieve the email password for the user.

        Parameters:
            encryption_key (str): The encryption key to use for decryption.

        Returns:
            str: The decrypted email password.
        """
        # Decrypt the email password
        cipher_suite = Fernet(encryption_key)
        decrypted_password = cipher_suite.decrypt(self.email_password.encode()).decode()
        return decrypted_password

    @classmethod
    def create_user(cls, username:str, email:str, linkedin_link:str, password:str, phone_number:str, email_password:str, encryption_key:str)->bool:
        """
        Create a new user and add them to the database.

        Parameters:
            username (str): User's username.
            email (str): User's email address.
            linkedin_link (str): User's LinkedIn profile link.
            password (str): User's password.
            phone_number (str): User's phone number.
            email_password (str): User's email password.
            encryption_key (str): Encryption key to encrypt email password.
        Returns:
            bool: The user created or not.
        """
        user = session.query(cls).filter(cls.email == email).first()
        if user:
            return False
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
        return True

    @classmethod
    def verify_login(cls, email:str, password:str)->tuple[bool,Union[str,None]]:
        """
        Verify user login credentials.

        Parameters:
            email (str): User's email address.
            password (str): User's password.

        Returns:
            tuple: A tuple containing a boolean indicating whether the login is successful and the user ID.
        """
        # Find user email
        user = session.query(cls).filter(cls.email == email).first()
        if user:
            # Verify password
            if user.check_password(password):
                # Decrypt and return email password
                user_id = user.id
                return True, user_id
        return False, None
