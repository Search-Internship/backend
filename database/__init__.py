import os
import sys
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from pathlib import Path
import mysql.connector
from models import Base
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)

# Load variables from the specified .env file
load_dotenv(dotenv_path=str(Path("./env/database.env")))

if os.getenv("DB_TYPE"):
    if str(os.getenv("DB_TYPE")).lower() in ["mysql","nariadb"]:
        DATABASE_URL = f"mysql+mysqlconnector://{os.getenv('USER_NAME')}:{os.getenv('PASSWORD')}@{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('DB_NAME')}"
    elif str(os.getenv("DB_TYPE")).lower()=="postgresql":
        DATABASE_URL = f"postgresql+psycopg2://{os.getenv('USER_NAME')}:{os.getenv('PASSWORD')}@{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('DB_NAME')}"
    elif str(os.getenv("DB_TYPE")).lower() in ["oracle","oracledb"]:
        DATABASE_URL = f"oracle+cx_oracle://{os.getenv('USER_NAME')}:{os.getenv('PASSWORD')}@{os.getenv('HOST')}:{os.getenv('PORT')}/{os.getenv('DB_NAME')}"
else:
    pass


# Create an engine
engine = create_engine(DATABASE_URL, echo=True)  # Change the URL according to your database setup

# Create tables
Base.metadata.create_all(engine, checkfirst=True)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()
