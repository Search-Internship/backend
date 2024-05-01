import os
import sys
import cx_Oracle
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=str(Path("./env/database.env")))

try:
    dsn = cx_Oracle.makedsn(os.getenv('HOST'), os.getenv('PORT'), service_name=os.getenv('SERVICE_NAME'))
    # Establish connection to Oracle database
    connection = cx_Oracle.connect(
        user=os.getenv('USER_NAME'),
        password=os.getenv('PASSWORD'),
        dsn=dsn 
    )
    cursor = connection.cursor()

    # Create tablespace if necessary
    cursor.execute(f"CREATE TABLESPACE {os.getenv('TABLESPACE_NAME')} DATAFILE '{os.getenv('DATAFILE_PATH')}' SIZE {os.getenv('DATAFILE_SIZE')}")

    # Create user and grant necessary privileges
    cursor.execute(f"CREATE USER {os.getenv('USER_NAME')} IDENTIFIED BY {os.getenv('USER_PASSWORD')} DEFAULT TABLESPACE {os.getenv('TABLESPACE_NAME')}")

    # Grant necessary privileges
    cursor.execute(f"GRANT CONNECT, RESOURCE TO {os.getenv('USER_NAME')}")

    # Close cursor and connection
    cursor.close()
    connection.close()
    print("Oracle database objects created successfully!")
except Exception as e:
    print(f"Error creating Oracle database objects: {e}")

is_connect = False

try:
    dsn = cx_Oracle.makedsn(os.getenv('HOST'), os.getenv('PORT'), service_name=os.getenv('SERVICE_NAME'))
    # Establish connection to Oracle database
    connection = cx_Oracle.connect(
        user=os.getenv('USER_NAME'),
        password=os.getenv('PASSWORD'),
        dsn=dsn 
    )

    # Create a cursor object to execute SQL queries
    cursor = connection.cursor()
    is_connect = True
except Exception as e:
    is_connect = False
    print("Problem on connection to Oracle:", e)

if is_connect:
    try:
        # SQL query to create the users table
        create_table_query = """
        CREATE TABLE users (
            id VARCHAR2(37) PRIMARY KEY,
            username VARCHAR2(255),
            date VARCHAR2(255),
            time VARCHAR2(255),
            email VARCHAR2(255) UNIQUE,
            linkedin_link VARCHAR2(255),
            password_hash VARCHAR2(255),
            phone_number VARCHAR2(255),
            email_password VARCHAR2(255)
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
        CREATE TABLE operations (
            id VARCHAR2(37) PRIMARY KEY,
            from_email VARCHAR2(255),
            date VARCHAR2(255),
            time VARCHAR2(255),
            email_body CLOB,
            subject CLOB,
            pdf_id VARCHAR2(37),
            success_receiver VARCHAR2(255),
            failed_receiver VARCHAR2(255),
            user_id VARCHAR2(255),
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
