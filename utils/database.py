from pathlib import Path

def get_database_url(database_type:str="",username:str="",password:str="",port:str="",host:str="",database_name:str="",db_file_path:str=""):
    """
    Generate a database URL for different SQL databases.

    Args:
        db_type (str): Type of the SQL database ('mariadb', 'mysql', 'postgresql', 'mssql', 'sqlite',).
        user (str): Username for connecting to the database.
        password (str): Password for connecting to the database.
        host (str): Hostname or IP address of the database server.
        port (int): Port number of the database server.
        db_name (str): Name of the database to connect to.

    Returns:
        str: Database URL.
    """
    if database_type:
        if str(database_type).lower() in ["mysql","mariadb"]:
            return f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database_name}"
        elif str(database_type).lower()=="postgresql":
            return f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}"
        elif str(database_type).lower() in ["oracle","oracledb"]:
            return f"oracle+cx_oracle://{username}:{password}@{host}:{port}/{database_name}"
        elif str(database_type).lower()=="sqlite":
            return f"sqlite:///{str(Path(db_file_path))}"
        elif str(database_type).lower() in ["sqlserver","mssql"]:
            return f"mssql+pyodbc://{username}:{password}@{host}:{port}/{database_name}"
        else:
            raise ValueError("Unsupported database type. we are support just (sqlite,mysql,mariadb,sqlserver(mssql),oracledb,postgresql)")
    else:
        raise ValueError("database type cannot be null")