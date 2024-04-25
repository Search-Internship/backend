import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Operations(Base):
    """
    Operations model representing an operation in the database.

    Attributes:
        id (str): Unique identifier for the operation.
        from_email (str): Source email address.
        date (str): Date of the operation.
        time (str): Time of the operation.
        pdf_base64 (str): Base64 encoded PDF data.
        email_body (str): Body of the email.
        subject (str): Subject of the email.
        success_receiver (str): Receiver of the successful operation.
        failed_receiver (str): Receiver of the failed operation.
        user_id (str): Foreign key referencing the id of the user associated with this operation.
    """
    __tablename__ = 'operations'

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    from_email = Column(String)
    date = Column(String)
    time = Column(String)
    pdf_base64 = Column(String)
    email_body = Column(String)
    subject = Column(String)
    success_receiver = Column(String)
    failed_receiver = Column(String)
    user_id = Column(String, ForeignKey('users.id'))

    # Define the relationship to the Users table
    user = relationship("User", back_populates="operations")