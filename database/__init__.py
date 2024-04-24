import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pathlib import Path
from models import Base
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)
from utils.database import get_database_url

# Load variables from the specified .env file
load_dotenv(dotenv_path=str(Path("./env/database.env")))


DATABASE_URL:str=get_database_url(database_type=os.getenv("DB_TYPE"),username=os.getenv("USER_NAME"),password=os.getenv("PASSWORD"),port=os.getenv("PORT"),host=os.getenv("HOST"),database_name=os.getenv("DB_NAME"),db_file_path=os.getenv("DB_FILE_PATH"))
# Create an engine
engine = create_engine(DATABASE_URL, echo=True)  # Change the URL according to your database setup

# Create tables
Base.metadata.create_all(engine, checkfirst=True)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()
