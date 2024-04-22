import os
import sys

parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base
from dotenv import load_dotenv
from pathlib import Path

# Load variables from the specified .env file
load_dotenv(dotenv_path=str(Path("./env/database.env")))
DATABASE_URL = f"mysql+mysqlconnector://{os.getenv("USER_NAME")}:{os.getenv("PASSWORD")}@{os.getenv("HOST")}:{os.getenv("PORT")}/{os.getenv("DB_NAME")}"

# Create an engine
engine = create_engine(DATABASE_URL, echo=True)  # Change the URL according to your database setup

# Create tables
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()
