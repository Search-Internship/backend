#!/bin/bash

# Function to create a folder if it doesn't exist
create_folder_if_not_exists() {
    folder_path=$1
    if [ ! -d "$folder_path" ]; then
        mkdir -p "$folder_path"
        echo "Folder '$folder_path' created."
    else
        echo "Folder '$folder_path' already exists."
    fi
}

# Function to create a file if it doesn't exist
create_file_if_not_exists() {
    file_path=$1
    if [ ! -f "$file_path" ]; then
        touch "$file_path"
        echo "File '$file_path' created."
    else
        echo "File '$file_path' already exists."
    fi
}

# Function to update environment variable in a file
update_env_variable() {
    file_path=$1
    variable_name=$2
    value=$3
    print_value=$4
    echo "$variable_name=$value" >> "$file_path"
    if [ "$print_value" = true ]; then
        echo "Variable '$variable_name' set to '$value' in '$file_path' file."
    else
        echo "Variable '$variable_name' set to '****' in '$file_path' file."
    fi
}

# Function to install a Python module
install_python_module() {
    module_name=$1
    if pip install "$module_name"; then
        echo "Module Installation: $module_name installed successfully."
    else
        echo "Module Installation: $module_name not installed."
    fi
}

# Function to create and activate a virtual environment
create_and_activate_venv() {
    venv_name=$1
    python_cmd="python3"
    create_cmd="$python_cmd -m venv $venv_name"
    activate_cmd="source $venv_name/bin/activate"
    
    # Create the virtual environment
    $create_cmd

    # Activate the virtual environment
    $activate_cmd

    echo "Virtual environment '$venv_name' created and activated."
}

# Function to install requirements from a file
install_requirements() {
    requirements_file=$1
    if pip install -r "$requirements_file"; then
        echo "Requirements installed successfully."
    else
        echo "Error installing requirements."
    fi
}

# Function to read password securely
read_password() {
    prompt=$1
    password=""
    while IFS= read -r -s -n 1 char; do
        if [[ $char == $'\0' ]]; then
            break
        fi
        if [[ $char == $'\177' ]]; then
            if [ -n "$password" ]; then
                password="${password%?}"
                echo -en "\b \b"
            fi
        else
            password+=$char
            echo -en "*"
        fi
    done
    echo
}





# Main function
main() {
    db_type=${1,,}
    if [[ ! " mysql mariadb postgresql oracle oracledb mssql sqlserver sqlite" =~ " $db_type " ]]; then
        echo "Usage: $0 db_type"
        echo "And db_type in ['mysql', 'mariadb', 'postgresql', 'oracle', 'oracledb', 'mssql', 'sqlserver', 'sqlite']"
        exit 1
    fi

    if [ -z "$db_type" ]; then
        db_type="sqlite"
    fi

    venv_name="venv"

    create_and_activate_venv "$venv_name"

    available_db=( ["mysql"]="mysql-connector-python" ["postgresql"]="psycopg2" ["oracle"]="cx_Oracle" ["oracledb"]="cx_Oracle" ["mssql"]="pymssql" ["sqlserver"]="pymssql" ["sqlite"]="")

    db_module=${available_db[$db_type]}
    if [ -n "$db_module" ]; then
        install_python_module "$db_module"
    else
        echo "No database module required for SQLite."
    fi

    install_requirements "requirements/base.txt"

    create_folder_if_not_exists "env"
    create_file_if_not_exists "env/database.env"

    
    if [ "$db_type" != "sqlite" ]; then
        default_db_name="easyinternship"
        default_host="localhost"
        default_user_name="root"
        default_password="admin"
        echo "Enter the database ($db_type) details:"
        read -p "Enter the database name (default is $default_db_name): " db_name
        read -p "Enter the host (default is $default_host): " host
        read -p "Enter the username (default is $default_user_name): " user_name
        stty -echo
        read -p "Enter the password (default is $default_password): " password
        stty echo
        echo
        

        update_env_variable "env/database.env" "DB_NAME" "${db_name:-default_db_name}"
        update_env_variable "env/database.env" "HOST" "${host:-default_host}"
        update_env_variable "env/database.env" "DB_TYPE" "${db_type:-default_db_type}"
        update_env_variable "env/database.env" "USER_NAME" "${user_name:-default_user_name}"
        update_env_variable "env/database.env" "PASSWORD" "${password:-default_password}"

    fi
    

    if [ "$db_type" = "mysql" ] || [ "$db_type" = "mariadb" ]; then
        read -p "Enter the port (default is 3306): " port
        update_env_variable "env/database.env" "PORT" "${port:-3306}"
    elif [ "$db_type" = "oracle" ] || [ "$db_type" = "oracledb" ]; then
        read -p "Enter the port (default is 1521): " port
        update_env_variable "env/database.env" "PORT" "${port:-1521}"
    elif [ "$db_type" = "mssql" ] || [ "$db_type" = "sqlserver" ]; then
        read -p "Enter the port (default is 1433): " port
        update_env_variable "env/database.env" "PORT" "${port:-1433}"
    elif [ "$db_type" = "postgresql" ]; then
        read -p "Enter the port (default is 5432): " port
        update_env_variable "env/database.env" "PORT" "${port:-5432}"
    elif [ "$db_type" = "sqlite" ]; then
        read -p "Enter the database file path: " db_file_path
        update_env_variable "env/database.env" "DB_FILE_PATH" "$db_file_path"
    fi

    # Additional environment files and variables can be set here

}

# Execute the main function with command-line argument
main "$@"
