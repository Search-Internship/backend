import mysql.connector
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=str(Path("./env/database.env")))


# Create a connection to MySQL server without specifying database
try:
    connection = mysql.connector.connect(
        host=os.getenv('HOST'),
        user=os.getenv('USER_NAME'),
        password=os.getenv('PASSWORD')
    )
    cursor = connection.cursor()
    
    # Create database if it doesn't exist
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {os.getenv('DB_NAME')}")
    
    # Close cursor and connection
    cursor.close()
    connection.close()
    print(f"{os.getenv('DB_NAME')} database created !")
except Exception as e:
    print(f"Error creating database: {e}")







is_connect:bool=False

try:
    # Establish connection to MySQL database
    connection = mysql.connector.connect(
        host=os.getenv('HOST'),
        user=os.getenv('USER_NAME'),
        password=os.getenv('PASSWORD'),
        database=os.getenv('DB_NAME')
    )

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()
    is_connect=True
except:
    is_connect=False
    print("Problem on connection to MySQL")


if is_connect:
    # SQL query to create the users table
    create_table_query = """
    CREATE TABLE IF NOT EXISTS users (
        id VARCHAR(255) PRIMARY KEY,
        username VARCHAR(255),
        email VARCHAR(255),
        linkedin_link VARCHAR(255),
        password_hash VARCHAR(255),
        phone_number VARCHAR(255) UNIQUE,
        email_password VARCHAR(255)
    )
    """

    # Execute the SQL query
    cursor.execute(create_table_query)

    # Commit the transaction and close the connection
    connection.commit()
    connection.close()
    print("Table Users Created !")