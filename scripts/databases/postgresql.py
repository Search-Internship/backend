import os
import sys
import psycopg2
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=str(Path("./env/database.env")))

try:
    # Create a connection to PostgreSQL server without specifying database
    connection = psycopg2.connect(
        host=os.getenv('HOST'),
        user=os.getenv('USER_NAME'),
        password=os.getenv('PASSWORD')
    )
    cursor = connection.cursor()

    # Create database if it doesn't exist
    cursor.execute(f"DROP DATABASE IF EXISTS {os.getenv('DB_NAME')}")
    cursor.execute(f"CREATE DATABASE {os.getenv('DB_NAME')}")

    # Close cursor and connection
    cursor.close()
    connection.close()
    print(f"{os.getenv('DB_NAME')} database created !")
except Exception as e:
    print(f"Error creating database: {e}")

is_connect = False

try:
    # Establish connection to PostgreSQL database
    connection = psycopg2.connect(
        host=os.getenv('HOST'),
        user=os.getenv('USER_NAME'),
        password=os.getenv('PASSWORD'),
        database=os.getenv('DB_NAME')
    )

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()
    is_connect = True
except Exception as e:
    is_connect = False
    print("Problem on connection to PostgreSQL:", e)

if is_connect:
    try:
        # SQL query to create the users table
        create_table_query = """
        CREATE TABLE IF NOT EXISTS users (
            id VARCHAR(37) PRIMARY KEY,
            username VARCHAR(255),
            date VARCHAR(255),
            time VARCHAR(255),
            email VARCHAR(255) UNIQUE,
            linkedin_link VARCHAR(255),
            password_hash VARCHAR(255),
            phone_number VARCHAR(255),
            email_password VARCHAR(255)
        )
        """

        # Execute the SQL query
        cursor.execute(create_table_query)

        # Commit the transaction
        connection.commit()
        print("Table Users Created !")
    except Exception as e:
        print(f"Error creating users table: {e}")

    try:
        # SQL query to create the operations table
        create_operations_table_query = """
        CREATE TABLE IF NOT EXISTS operations (
            id VARCHAR(37) PRIMARY KEY,
            from_email VARCHAR(255),
            date VARCHAR(255),
            time VARCHAR(255),
            email_body TEXT,
            subject TEXT,
            pdf_id VARCHAR(37),
            success_receiver VARCHAR(255),
            failed_receiver VARCHAR(255),
            user_id VARCHAR(255),
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        """

        # Execute the SQL query to create operations table
        cursor.execute(create_operations_table_query)

        # Commit the transaction
        connection.commit()
        print("Table Operations Created !")
    except Exception as e:
        print(f"Error creating operations table: {e}")

    connection.close()
