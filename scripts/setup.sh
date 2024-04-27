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

    # Delete the line if it exists
    sed -i "/^$variable_name=/d" "$file_path"

    # Add the new variable to the file
    echo "$variable_name=$value" >> "$file_path"

    # Print the appropriate message based on the print_value flag
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

is_gmail_password_structure() {
    # Define the password structure regex pattern
    local pattern='^.... .... .... ....$'
    
    # Check if the password matches the pattern
    if [[ "$1" =~ $pattern ]]; then
        return 0
    else
        return 1
    fi
}

is_valid_email() {
    local email=$1
    if [[ "$email" =~ ^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$ ]]; then
        return 0
    else
        return 1
    fi
}





# Main function
main() {
    DB_TYPE="sqlite"
    echo
    echo "Available database type : mysql , mariadb, postgresql, oracle, oracledb, mssql, sqlserver, sqlite"
    read -p "Enter the database type (default is $DB_TYPE): " db_type

    if [[ ! " mysql mariadb postgresql oracle oracledb mssql sqlserver sqlite" =~ " ${db_type:-$DB_TYPE} " ]]; then
        echo "$db_type not in ['mysql', 'mariadb', 'postgresql', 'oracle', 'oracledb', 'mssql', 'sqlserver', 'sqlite']"
        exit 1
    fi

    if [ -z "$db_type" ]; then
        db_type="$DB_TYPE"
    fi

    VENV_NAME="venv"
    echo
    read -p "Enter the virtual envirenment name (default is $VENV_NAME): " venv_name
    create_and_activate_venv "${venv_name:-$VENV_NAME}"

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
        default_password=""
        echo "Enter the database ($db_type) details:"
        echo
        read -p "Enter the database name (default is $default_db_name): " db_name
        echo
        read -p "Enter the host (default is $default_host): " host
        echo
        read -p "Enter the username (default is $default_user_name): " user_name
        echo
        echo -n "Enter the password (default is vide): "
        read_password
        echo
        

        update_env_variable "env/database.env" "DB_NAME" "${db_name:-$default_db_name}" true
        update_env_variable "env/database.env" "HOST" "${host:-$default_host}" true
        update_env_variable "env/database.env" "DB_TYPE" "${db_type:-$default_db_type}" true
        update_env_variable "env/database.env" "USER_NAME" "${user_name:-$default_user_name}" true
        update_env_variable "env/database.env" "PASSWORD" "${password:-$default_password}" false

    fi
    

    if [ "$db_type" = "mysql" ] || [ "$db_type" = "mariadb" ]; then
        read -p "Enter the port (default is 3306): " port
        update_env_variable "env/database.env" "PORT" "${port:-3306}" true
        echo
    elif [ "$db_type" = "oracle" ] || [ "$db_type" = "oracledb" ]; then
        read -p "Enter the port (default is 1521): " port 
        update_env_variable "env/database.env" "PORT" "${port:-1521}" true
    elif [ "$db_type" = "mssql" ] || [ "$db_type" = "sqlserver" ]; then
        read -p "Enter the port (default is 1433): " port 
        update_env_variable "env/database.env" "PORT" "${port:-1433}" true
    elif [ "$db_type" = "postgresql" ]; then
        read -p "Enter the port (default is 5432): " port 
        update_env_variable "env/database.env" "PORT" "${port:-5432}" true
    elif [ "$db_type" = "sqlite" ]; then
        read -p "Enter the database file path: " db_file_path
        update_env_variable "env/database.env" "DB_FILE_PATH" "$db_file_path" true
    fi

    echo "Application Communication Details:"
    create_file_if_not_exists "env/communication.env"

    echo
    while true; do
        read -p "Enter the email address: " email_address

        # Check if the email address is valid
        if is_valid_email "$email_address"; then
            break  # Break the loop if email address is valid
        else
            echo
            echo "Error: Invalid email address '$email_address'."
        fi
    done

    # Loop until a valid email password is entered
    echo
    while true; do
        echo -n "Enter the email password (xxxx xxxx xxxx xxxx): "
        read_password

        # Call your function to validate email password structure
        if is_gmail_password_structure "$password"; then
            break
        else
            echo "Error: Invalid email password structure. Password must consist of four segments separated by spaces, each segment must be exactly four characters long."
        fi
    done

    update_env_variable "env/communication.env" "EMAIL_PROJECT" "$email_address" true
    update_env_variable "env/communication.env" "PASSWORD_EMAIL_PROJECT" "$password" false


    echo "Application Security Details:"
    create_file_if_not_exists "env/secrets.env"

    echo
    FERNET_KEY="Zsy6-8REWdN0-FkIhgBy8k19MJ7elYNAv3MxkWHFGOk="
    ACCESS_TOKEN_EXPIRE_MINUTES=60
    JWT_SECRET_KEY="abababababababbabhha"
    ALGORITHM="HS256"
    PDF_ENCRYPTION_SECRET="pdfababababab"
    read -p "FERNET KEY (default is $FERNET_KEY): " fernet_key
    echo
    read -p "JWT ACCESS TOKEN EXPIRE MINUTES (default is $ACCESS_TOKEN_EXPIRE_MINUTES): " access_token_expire_minutes
    echo
    read -p "JWT KEY (default is $JWT_SECRET_KEY): " jwt_secret_key
    echo
    read -p "JWT ALGORITHM (default is $ALGORITHM): " algorithm
    echo
    read -p "PDF ENCRYPTION SECRET (default is $PDF_ENCRYPTION_SECRET): " pdf_encryption_secret
    echo
    update_env_variable "env/secrets.env" "FERNET_KEY" "${fernet_key:-$FERNET_KEY}" true
    update_env_variable "env/secrets.env" "ACCESS_TOKEN_EXPIRE_MINUTES" "${access_token_expire_minutes:-$ACCESS_TOKEN_EXPIRE_MINUTES}" true
    update_env_variable "env/secrets.env" "JWT_SECRET_KEY" "${jwt_secret_key:-$JWT_SECRET_KEY}" true
    update_env_variable "env/secrets.env" "ALGORITHM" "${algorithm:-$ALGORITHM}" true
    update_env_variable "env/secrets.env" "PDF_ENCRYPTION_SECRET" "${pdf_encryption_secret:-$PDF_ENCRYPTION_SECRET}" true

    echo "Unit Testing Details: "
    create_file_if_not_exists "env/tests.env"

    echo
    EMAIL_SENDER_UNIT_TEST="laamiri.ouail@etu.uae.ac.ma"
    EMAIL_RECEIVER_UNIT_TEST="laamiriouail@gmail.com"
    PASSWORD_UNIT_TEST="cfkd dihq xxyw ugin "
    while true; do
        read -p "Enter the email sender for unit test : " email_sender_unit_test

        # Check if the email address is valid
        if is_valid_email "$email_sender_unit_test"; then
            break  # Break the loop if email address is valid
        else
            echo
            echo "Error: Invalid email address '$email_sender_unit_test'."
        fi
    done

    echo
    while true; do
        echo -n "Password for unit test email (xxxx xxxx xxxx xxxx): "
        read_password

        # Call your function to validate email password structure
        if is_gmail_password_structure "$password"; then
            break
        else
            echo "Error: Invalid email password structure. Password must consist of four segments separated by spaces, each segment must be exactly four characters long."
        fi
    done

    echo

    while true; do
        read -p "Enter the email receiver for unit test : " email_receiver_unit_test

        # Check if the email address is valid
        if is_valid_email "$email_receiver_unit_test"; then
            break  # Break the loop if email address is valid
        else
            echo
            echo "Error: Invalid email address '$email_receiver_unit_test'."
        fi
    done
    

    update_env_variable "env/tests.env" "EMAIL_SENDER_UNIT_TEST" "$email_sender_unit_test" true
    update_env_variable "env/tests.env" "EMAIL_RECEIVER_UNIT_TEST" "$email_receiver_unit_test" true
    update_env_variable "env/tests.env" "PASSWORD_UNIT_TEST" "$password" false

    

}

# Execute the main function with command-line argument
main "$@"
