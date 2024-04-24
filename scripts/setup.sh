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
    default_value=$3
    if ! grep -q "^$variable_name=" "$file_path"; then
        echo "$variable_name=$default_value" >> "$file_path"
        echo "Variable '$variable_name' set to '$default_value' in '$file_path' file."
    else
        echo "Variable '$variable_name' already exists in '$file_path' file."
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

# Main function
main() {
    db_type=${1,,}
    if [[ ! " mysql mariadb postgresql oracle oracledb mssql sqlserver sqlite " =~ " $db_type " ]]; then
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
    update_env_variable "env/database.env" "DB_NAME" "easyinternship"
    update_env_variable "env/database.env" "HOST" "localhost"
    update_env_variable "env/database.env" "DB_TYPE" "$db_type"
    update_env_variable "env/database.env" "USER_NAME" "root"
    update_env_variable "env/database.env" "PASSWORD" "admin"
    if [ "$db_type" = "mysql" ] || [ "$db_type" = "mariadb" ]; then
        update_env_variable "env/database.env" "PORT" "3306"
    elif [ "$db_type" = "oracle" ] || [ "$db_type" = "oracledb" ]; then
        update_env_variable "env/database.env" "PORT" "3306"
    elif [ "$db_type" = "mssql" ] || [ "$db_type" = "sqlserver" ]; then
        update_env_variable "env/database.env" "PORT" "3306"
    elif [ "$db_type" = "postgresql" ]; then
        update_env_variable "env/database.env" "PORT" "3306"
    fi

    # Additional environment files and variables can be set here

}

# Execute the main function with command-line argument
main "$@"
