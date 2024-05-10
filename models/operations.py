import uuid
from sqlalchemy import Column, String, ForeignKey,Text
from sqlalchemy.orm import relationship
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)
import datetime
from database import Base
from models.user import User


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
    

    __table_args__ = {'extend_existing': True}

    __tablename__ = 'operations'

    id = Column(String(37), primary_key=True, default=lambda: str(uuid.uuid4()))
    from_email = Column(String(55))
    date = Column(String(55))
    time = Column(String(55))
    email_body = Column(Text)
    subject = Column(String(255))
    pdf_id = Column(String(37))
    success_receiver = Column(Text)
    failed_receiver = Column(Text)
    user_id = Column(String(37), ForeignKey('users.id'))

    # Define the relationship to the Users table
    user = relationship("User", back_populates="operations")

    @classmethod
    def create_operation(cls, session, from_email, email_body, subject, success_receiver, failed_receiver,pdf_id, user_id):
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
            pdf_id=pdf_id,
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
            'pdf_id': operation.pdf_id,
            'user_id': operation.user_id
        }