import os
import sys
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)
from dotenv import load_dotenv
from pathlib import Path
import platform


def create_folder_if_not_exists(folder_path):
    """
    Verify if a folder exists and create it if it doesn't.

    Args:
        folder_path (str): Path to the folder to be verified and created.

    Returns:
        str: Path to the folder.
    """
    # Check if the folder exists
    if not os.path.exists(folder_path):
        # Create the folder
        os.makedirs(folder_path)
        print(f"Folder '{folder_path}' created.")
    else:
        print(f"Folder '{folder_path}' already exists.")


def create_file_if_not_exists(file_path):
    """
    Verify if a file exists and create it if it doesn't.

    Args:
        file_path (str): Path to the file to be verified and created.

    Returns:
        str: Path to the file.
    """
    # Check if the file exists
    if not os.path.exists(file_path):
        # Create the file
        with open(file_path, 'w') as f:
            f.write('')
        print(f"File '{file_path}' created.")
    else:
        print(f"File '{file_path}' already exists.")
    
    return file_path

def update_env_variable(file_path,variable_name, default_value):
    """
    Check if a variable exists in the .env file, if not, create it and set its value.

    Args:
        file_path (str): Path to the .env file
        variable_name (str): Name of the environment variable.
        default_value (str): Default value to set if the variable doesn't exist in the .env file.
    """
    # Load environment variables from .env file
    load_dotenv(file_path)

    # Get the value of the variable from the environment
    value = os.getenv(variable_name)

    # Check if the variable exists in the .env file
    if value is None:
        # Variable doesn't exist, set default value
        with open(file_path, 'a') as f:
            f.write(f'\n{variable_name}={default_value}\n')
        print(f"Variable '{variable_name}' set to '{default_value}' in {file_path} file.")
    else:
        print(f"Variable '{variable_name}' already exists in {file_path} file.")


## mysql-connector-python

def install_python_module(module_name:str)->bool:
    try:
        os.system(" ".join(["pip", "install", module_name]))
        print(f"Module Installation : {module_name} installed successfully")
        return True
    except:
        print(f"Module Installation : {module_name} not installed")
        return False



def create_and_activate_venv(venv_name):
    # Determine the appropriate command to create a virtual environment based on the operating system
    if platform.system() == "Windows":
        create_cmd = "python -m venv"
        activate_cmd = str(Path(f"{venv_name}/Scripts/activate"))
    else:
        create_cmd = f"python3 -m venv"
        activate_cmd = str(Path(f"{venv_name}/bin/activate"))

    # Create the virtual environment
    os.system(" ".join([create_cmd, venv_name]))

    # Activate the virtual environment
    if platform.system() == "Windows":
        activate_cmd = f"cmd /K {activate_cmd}"
    else:
        activate_cmd = f"source {activate_cmd}"
    os.system(activate_cmd)

    print(f"Virtual environment '{venv_name}' created and activated.")

def install_requirements(requirements_file):
    try:
        os.system(" ".join(["pip", "install", "-r", requirements_file]))
        print("Requirements installed successfully.")
    except Exception as e:
        print(f"Error installing requirements: {e}")



if __name__=="__main__":
    db_type=None
    if len(sys.argv) != 2:
        if platform.system() == "Windows":
            print("Usage: python scripts/setup.py db_type\nAnd db_type in ['mysql','mariadb','postgresql','oracle','oracledb','mssql','sqlserver','sqlite']")
        else:
            print("Usage: python3 scripts/setup.py db_type\nAnd db_type in ['mysql','mariadb','postgresql','oracle','oracledb','mssql','sqlserver','sqlite']")
        sys.exit(1)
    
    db_type = str(sys.argv[1]).lower()
    if db_type not in ['mysql','mariadb','postgresql','oracle','oracledb','mssql','sqlserver','sqlite']:
        if platform.system() == "Windows":
            print("Usage: python scripts/setup.py db_type\nAnd db_type in ['mysql','mariadb','postgresql','oracle','oracledb','mssql','sqlserver','sqlite']")
        else:
            print("Usage: python3 scripts/setup.py db_type\nAnd db_type in ['mysql','mariadb','postgresql','oracle','oracledb','mssql','sqlserver','sqlite']")
        sys.exit(1)
    if db_type is None:
        db_type:str="sqlite"
    # create_folder_if_not_exists(str(Path("venv")))
    create_and_activate_venv(str(Path("venv")))
    available_db:dict[str,str]={
        "mysql":'mysql-connector-python',
        "postgresql":'psycopg2',
        "oracle":'cx_Oracle',
        "oracledb":'cx_Oracle',
        "mssql":'pymssql',
        "sqlserver":'pymssql',
        "sqlite":'',
    }
    db_name:str = "easyinternship"
    db_host:str = "localhost"
    db_module:str = available_db[db_type]
    if db_module:
        if install_python_module(db_module):
            print(f"Database module {db_module} installed successfully.")
        else:
            print(f"Database module {db_module} not installed.")
    else:
        print("No database module required for SQLite.")
    install_requirements(str(Path("requirements/base.txt")))
    create_folder_if_not_exists(str(Path("env")))
    ############### DATABASE ####################################
    create_file_if_not_exists(str(Path("env/database.env")))
    update_env_variable(str(Path("env/database.env")),"DB_NAME","easyinternship")
    update_env_variable(str(Path("env/database.env")),"HOST","localhost")
    update_env_variable(str(Path("env/database.env")),"DB_TYPE",f"{db_type}")
    update_env_variable(str(Path("env/database.env")),"USER_NAME","root")
    update_env_variable(str(Path("env/database.env")),"PASSWORD","admin")
    if db_type in ["mysql","mariadb"]:
        update_env_variable(str(Path("env/database.env")),"PORT","3306")
    elif db_type in ["oracle","oracledb"]:
        update_env_variable(str(Path("env/database.env")),"PORT","3306")
    elif db_type in ["mssql","sqlserver"]:
        update_env_variable(str(Path("env/database.env")),"PORT","3306")
    elif db_type=="postgresql":
        update_env_variable(str(Path("env/database.env")),"PORT","3306")
    
    ############### Secrets ####################################
    create_file_if_not_exists(str(Path("env/secrets.env")))
    update_env_variable(str(Path("env/secrets.env")),"FERNET_KEY","Zsy6-8REWdN0-FkIhgBy8k19MJ7elYNAv3MxkWHFGOk=")
    update_env_variable(str(Path("env/secrets.env")),"ACCESS_TOKEN_EXPIRE_MINUTES","60")
    update_env_variable(str(Path("env/secrets.env")),"JWT_SECRET_KEY","abababababababbabhha")
    update_env_variable(str(Path("env/secrets.env")),"ALGORITHM","HS256")
    update_env_variable(str(Path("env/secrets.env")),"PDF_ENCRYPTION_SECRET","pdfababababab")
    ############## tests #####################################
    create_file_if_not_exists(str(Path("env/tests.env")))
    update_env_variable(str(Path("env/tests.env")),"EMAIL_SENDER_UNIT_TEST","")
    update_env_variable(str(Path("env/tests.env")),"EMAIL_RECEIVER_UNIT_TEST","")
    update_env_variable(str(Path("env/tests.env")),"PASSWORD_UNIT_TEST","")
    ############## communication #####################################
    create_file_if_not_exists(str(Path("env/communication.env")))
    update_env_variable(str(Path("env/communication.env")),"EMAIL_PROJECT","")
    update_env_variable(str(Path("env/communication.env")),"PASSWORD_EMAIL_PROJECT","")


