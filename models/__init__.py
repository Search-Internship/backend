import uuid
from sqlalchemy import Column, String,ForeignKey,Text
from passlib.hash import sha256_crypt
from cryptography.fernet import Fernet  # For encryption
import os
import sys
from typing import Union
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import datetime


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
        date (str): Date of the operation.
        time (str): Time of the operation.
        avatar_base64 (str): Base64 encoded avatar image.
    """
    __tablename__ = 'users'
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String,max_length=255)
    email = Column(String,unique=True)
    linkedin_link = Column(String,max_length=255)
    password_hash = Column(String,max_length=255)
    phone_number = Column(String,max_length=255)
    date = Column(String)
    time = Column(String)
    email_password = Column(String,max_length=255)  # Store encrypted email password
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
    



class Operations(Base):
    """
    Operations model representing an operation in the database.

    Attributes:
        id (str): Unique identifier for the operation.
        from_email (str): Source email address.
        date (str): Date of the operation.
        time (str): Time of the operation.
        email_body (str): Body of the email.
        subject (str): Subject of the email.
        success_receiver (str): Receiver of the successful operation.
        failed_receiver (str): Receiver of the failed operation.
        user_id (str): Foreign key referencing the id of the user associated with this operation.
    """
    __tablename__ = 'operations'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    from_email = Column(String,max_length=255)
    date = Column(String,max_length=255)
    time = Column(String,max_length=255)
    email_body = Column(String,max_length=255)
    subject = Column(String,max_length=255)
    success_receiver = Column(Text)
    failed_receiver = Column(Text)
    user_id = Column(String, ForeignKey('users.id'))

    # Define the relationship to the Users table
    user = relationship("User", back_populates="operations")

    @classmethod
    def create_operation(cls, session, from_email, email_body, subject, success_receiver, failed_receiver, user_id):
        """
        Create a new operation associated with a user.

        Args:
            session (Session): SQLAlchemy session object.
            from_email (str): Source email address.
            resume_base64 (str): Base64 encoded PDF data.
            email_body (str): Body of the email.
            subject (str): Subject of the email.
            success_receiver (str): Receiver of the successful operation.
            failed_receiver (str): Receiver of the failed operation.
            user_id (str): ID of the user associated with this operation.

        Returns:
            Operations: The newly created operation object.
        
        Raises:
            ValueError: If the user with the provided user_id does not exist.
        """
        # Check if the user exists
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            raise ValueError("User with user_id {} does not exist".format(user_id))

        # Create the operation
        operation = cls(
            from_email=from_email,
            date=str(datetime.date.today()),  # Add current date
            time=str(datetime.datetime.now().time()),  # Add current time
            email_body=email_body,
            subject=subject,
            success_receiver=success_receiver,
            failed_receiver=failed_receiver,
            user_id=user_id
        )
        
        session.add(operation)
        session.commit()
        return True

    @classmethod
    def get_operations_info(cls, session, user_id):
        """
        Retrieve the subject and date-time of operations associated with a user.

        Args:
            session (Session): SQLAlchemy session object.
            user_id (str): ID of the user associated with the operations.

        Returns:
            list: A list of dictionaries containing subject and date-time information for each operation.
        
        Raises:
            ValueError: If the user with the provided user_id does not exist.
        """
        # Check if the user exists
        user:User|None = session.query(User).filter_by(id=user_id).first()
        if not user:
            raise ValueError("User with user_id {} does not exist".format(user_id))

        # Query for operations subject and date-time
        operations_info = session.query(cls.id,cls.subject, cls.date, cls.time).filter_by(user_id=user_id).all()

        # Convert query result to list of dictionaries
        operations_info_list:list = []
        for id,subject, date, time in operations_info:
            operations_info_list.append({
                'id': id,
                'subject': subject,
                'date': date,
                'time': time
            })

        return operations_info_list
    @classmethod
    def get_operation_by_id(cls, session, operation_id, user_id):
        """
        Retrieve an operation by its ID and associated user ID.

        Args:
            session (Session): SQLAlchemy session object.
            operation_id (str): ID of the operation to retrieve.
            user_id (str): ID of the user associated with the operation.

        Returns:
            dict: A dictionary containing information about the operation if found, None otherwise.
        
        Raises:
            ValueError: If the user with the provided user_id does not exist.
        """
        # Check if the user exists
        user = session.query(User).filter_by(id=user_id).first()
        if not user:
            raise ValueError("User with user_id {} does not exist".format(user_id))

        # Query for the operation by its ID and associated user ID
        operation = session.query(cls).filter_by(id=operation_id, user_id=user_id).first()

        # If operation not found, return None
        if not operation:
            return None

        # Return operation information as a dictionary
        return {
            'id': operation.id,
            'from_email': operation.from_email,
            'date': operation.date,
            'time': operation.time,
            'email_body': operation.email_body,
            'subject': operation.subject,
            'success_receiver': operation.success_receiver,
            'failed_receiver': operation.failed_receiver,
            'user_id': operation.user_id
        }