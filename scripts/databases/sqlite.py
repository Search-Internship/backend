import sqlite3
import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv(dotenv_path=str(Path("./env/database.env")))

# Define SQLite database file path
db_file = os.getenv('DB_FILE_PATH')

try:
    # Create connection to SQLite database
    connection = sqlite3.connect(db_file)
    cursor = connection.cursor()

    # Create database if it doesn't exist
    cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute("DROP TABLE IF EXISTS operations")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            username TEXT,
            date TEXT,
            time TEXT,
            email TEXT UNIQUE,
            linkedin_link TEXT,
            password_hash TEXT,
            phone_number TEXT,
            email_password TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS operations (
            id TEXT PRIMARY KEY,
            from_email TEXT,
            date TEXT,
            time TEXT,
            email_body TEXT,
            subject TEXT,
            pdf_id TEXT,
            success_receiver TEXT,
            failed_receiver TEXT,
            user_id TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    # Commit changes and close connection
    connection.commit()
    connection.close()

    print("SQLite database and tables created successfully!")

except Exception as e:
    print(f"Error: {e}")
