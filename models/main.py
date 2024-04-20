from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

class DatabaseManager:
    _instances = {}

    def __new__(cls, database_type, *args, **kwargs):
        if database_type not in cls._instances:
            cls._instances[database_type] = super().__new__(cls)
        return cls._instances[database_type]

    def __init__(self, database_type, connection_string):
        if not hasattr(self, 'initialized'):
            self.initialized = True
            self.engine = create_engine(connection_string)
            self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()

# Example usage
if __name__ == "__main__":
    # Create instances of DatabaseManager for different database types
    postgres_manager = DatabaseManager('postgresql', 'postgresql://username:password@localhost/dbname')
    mysql_manager = DatabaseManager('mysql', 'mysql://username:password@localhost/dbname')
    sqlite_manager = DatabaseManager('sqlite', 'sqlite:///path/to/your/database.db')

    # Get sessions from the managers
    postgres_session = postgres_manager.get_session()
    mysql_session = mysql_manager.get_session()
    sqlite_session = sqlite_manager.get_session()
