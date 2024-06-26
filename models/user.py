import uuid
from sqlalchemy import Column, String
from passlib.hash import sha256_crypt
from cryptography.fernet import Fernet  # For encryption
import os
import sys
from typing import Union
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)
from database import Base
from sqlalchemy.orm import relationship
import datetime


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
        date (str): Date of the operation.
        time (str): Time of the operation.
        avatar_base64 (str): Base64 encoded avatar image.
    """


    __table_args__ = {'extend_existing': True}

    __tablename__ = 'users'
    id = Column(String(37), primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String(55))
    email = Column(String(55),unique=True)
    linkedin_link = Column(String(55))
    password_hash = Column(String(255))
    phone_number = Column(String(255))
    date = Column(String(55))
    time = Column(String(55))
    email_password = Column(String(255))  # Store encrypted email password
    # Define the relationship to the Operations table
    operations = relationship("Operations", back_populates="user")
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
    def create_user(cls, session, username:str, email:str, linkedin_link:str, password:str, phone_number:str, email_password:str, encryption_key:str)->bool:
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
            phone_number=phone_number,
            date=str(datetime.date.today()),  # Add current date
            time=str(datetime.datetime.now().time())  # Add current time
        )
        # Set password and email password
        new_user.set_password(password)
        new_user.set_email_password(email_password, encryption_key)

        # Add the user to the database
        session.add(new_user)
        session.commit()
        return True

    @classmethod
    def verify_login(cls, session, email:str, password:str)->tuple[bool,Union[str,None]]:
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
    @classmethod
    def get_user_by_id(cls, session, user_id:str)-> Union['User', None]:
        """
        Get a user by user_id.

        Parameters:
            user_id (str): The user's ID.

        Returns:
            Union['User', None]: The user object if found, otherwise None.
        """
        return session.query(cls).filter(cls.id == user_id).first()
    @classmethod
    def get_user_by_email(cls, session, user_email:str)-> Union['User', None]:
        """
        Get a user by user_email.

        Parameters:
            user_email (str): The user's Email.

        Returns:
            Union['User', None]: The user object if found, otherwise None.
        """
        return session.query(cls).filter(cls.email == user_email).first()
    @classmethod
    def email_exists(cls, session, email: str) -> bool:
        """
        Check if an email already exists in the database.

        Parameters:
            session: SQLAlchemy session object.
            email (str): Email address to check.

        Returns:
            bool: True if the email exists, False otherwise.
        """
        return session.query(cls).filter(cls.email == email).count() > 0

    

