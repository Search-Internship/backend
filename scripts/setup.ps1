# Function to create a folder if it doesn't exist
function create_folder_if_not_exists {
    param(
        [string]$folder_path
    )
    if (-not (Test-Path $folder_path)) {
        New-Item -ItemType Directory -Path $folder_path | Out-Null
        Write-Output "Folder '$folder_path' created."
    } else {
        Write-Output "Folder '$folder_path' already exists."
    }
}

# Function to create a file if it doesn't exist
function create_file_if_not_exists {
    param(
        [string]$file_path
    )
    if (-not (Test-Path $file_path)) {
        New-Item -ItemType File -Path $file_path | Out-Null
        Write-Output "File '$file_path' created."
    } else {
        Write-Output "File '$file_path' already exists."
    }
}

# Function to update environment variable in a file
function update_env_variable {
    param(
        [string]$file_path,
        [string]$variable_name,
        [string]$value,
        [bool]$print_value
    )
    # Delete the line if it exists
    (Get-Content $file_path) -notmatch "^$variable_name=" | Set-Content $file_path

    # Add the new variable to the file
    Add-Content $file_path "$variable_name=$value"

    # Print the appropriate message based on the print_value flag
    if ($print_value -eq $true) {
        Write-Output "Variable '$variable_name' set to '$value' in '$file_path' file."
    } else {
        Write-Output "Variable '$variable_name' set to '****' in '$file_path' file."
    }
}

# Function to install a Python module
function install_python_module {
    param(
        [string]$module_name
    )
    if (pip install $module_name) {
        Write-Output "Module Installation: $module_name installed successfully."
    } else {
        Write-Output "Module Installation: $module_name not installed."
    }
}

# Function to create and activate a virtual environment
function create_and_activate_venv {
    param(
        [string]$venv_name
    )
    $python_cmd = "python3"
    $create_cmd = "$python_cmd -m venv $venv_name"
    $activate_cmd = "Activate $venv_name"

    # Create the virtual environment
    Invoke-Expression $create_cmd

    # Activate the virtual environment
    Invoke-Expression $activate_cmd

    Write-Output "Virtual environment '$venv_name' created and activated."
}

# Function to install requirements from a file
function install_requirements {
    param(
        [string]$requirements_file
    )
    if (pip install -r $requirements_file) {
        Write-Output "Requirements installed successfully."
    } else {
        Write-Output "Error installing requirements."
    }
}

# Function to read password securely
function read_password {
    $password = Read-Host -Prompt "Enter password" -AsSecureString
    $password = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($password))
    return $password
}

# Function to validate Gmail password structure
function is_gmail_password_structure {
    param(
        [string]$password
    )
    # Define the password structure regex pattern
    $pattern = '^.... .... .... ....$'
    
    # Check if the password matches the pattern
    if ($password -match $pattern) {
        return $true
    } else {
        return $false
    }
}

# Function to validate email address
function is_valid_email {
    param(
        [string]$email
    )
    $pattern = '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$'
    if ($email -match $pattern) {
        return $true
    } else {
        return $false
    }
}

# Main function
function main {
    $DB_TYPE = "sqlite"
    Write-Output ""
    Write-Output "Available database type : mysql , mariadb, postgresql, oracle, oracledb, mssql, sqlserver, sqlite"
    $db_type = Read-Host "Enter the database type (default is $DB_TYPE)"
    
    if (-not (" mysql mariadb postgresql oracle oracledb mssql sqlserver sqlite" -contains " $db_type")) {
        Write-Output "$db_type not in ['mysql', 'mariadb', 'postgresql', 'oracle', 'oracledb', 'mssql', 'sqlserver', 'sqlite']"
        exit 1
    }

    if ([string]::IsNullOrWhiteSpace($db_type)) {
        $db_type = $DB_TYPE
    }

    $VENV_NAME = "venv"
    $venv_name = Read-Host "Enter the virtual environment name (default is $VENV_NAME)"
    create_and_activate_venv ($venv_name -or $VENV_NAME)

    $available_db = @{
        "mysql" = "mysql-connector-python"
        "postgresql" = "psycopg2"
        "oracle" = "cx_Oracle"
        "oracledb" = "cx_Oracle"
        "mssql" = "pymssql"
        "sqlserver" = "pymssql"
        "sqlite" = ""
    }

    $db_module = $available_db[$db_type]
    if ([string]::IsNullOrWhiteSpace($db_module)) {
        Write-Output "No database module required for SQLite."
    } else {
        install_python_module $db_module
    }

    install_requirements "requirements/base.txt"

    create_folder_if_not_exists "env"
    create_file_if_not_exists "env/database.env"

    if ($db_type -ne "sqlite") {
        $default_db_name = "easyinternship"
        $default_host = "localhost"
        $default_user_name = "root"
        $default_password = ""
        Write-Output "Enter the database ($db_type) details:"
        $db_name = Read-Host "Enter the database name (default is $default_db_name)"
        $host = Read-Host "Enter the host (default is $default_host)"
        $user_name = Read-Host "Enter the username (default is $default_user_name)"
        Write-Output -NoNewline "Enter the password (default is vide): "
        $password = read_password
        Write-Output ""

        update_env_variable "env/database.env" "DB_NAME" ($db_name -or $default_db_name) $true
        update_env_variable "env/database.env" "HOST" ($host -or $default_host) $true
        update_env_variable "env/database.env" "DB_TYPE" ($db_type -or $default_db_type) $true
        update_env_variable "env/database.env" "USER_NAME" ($user_name -or $default_user_name) $true
        update_env_variable "env/database.env" "PASSWORD" ($password -or $default_password) $false
    }

    if ($db_type -eq "mysql" -or $db_type -eq "mariadb") {
        $port = Read-Host "Enter the port (default is 3306)"
        update_env_variable "env/database.env" "PORT" ($port -or 3306) $true
        Write-Output ""
    } elseif ($db_type -eq "oracle" -or $db_type -eq "oracledb") {
        $port = Read-Host "Enter the port (default is 1521)"
        update_env_variable "env/database.env" "PORT" ($port -or 1521) $true
    } elseif ($db_type -eq "mssql" -or $db_type -eq "sqlserver") {
        $port = Read-Host "Enter the port (default is 1433)"
        update_env_variable "env/database.env" "PORT" ($port -or 1433) $true
    } elseif ($db_type -eq "postgresql") {
        $port = Read-Host "Enter the port (default is 5432)"
        update_env_variable "env/database.env" "PORT" ($port -or 5432) $true
    } elseif ($db_type -eq "sqlite") {
        $db_file_path = Read-Host "Enter the database file path"
        update_env_variable "env/database.env" "DB_FILE_PATH" $db_file_path $true
    }

    Write-Output "Application Communication Details:"
    create_file_if_not_exists "env/communication.env"

    Write-Output ""
    while ($true) {
        $email_address = Read-Host "Enter the email address"

        # Check if the email address is valid
        if (is_valid_email $email_address) {
            break  # Break the loop if email address is valid
        } else {
            Write-Output ""
            Write-Output "Error: Invalid email address '$email_address'."
        }
    }

    # Loop until a valid email password is entered
    Write-Output ""
    while ($true) {
        Write-Output -NoNewline "Enter the email password (xxxx xxxx xxxx xxxx): "
        $password = read_password

        # Call your function to validate email password structure
        if (is_gmail_password_structure $password) {
            break
        } else {
            Write-Output "Error: Invalid email password structure. Password must consist of four segments separated by spaces, each segment must be exactly four characters long."
        }
    }

    Write-Output ""

    update_env_variable "env/communication.env" "EMAIL_PROJECT" $email_address $true
    update_env_variable "env/communication.env" "PASSWORD_EMAIL_PROJECT" $password $false


    Write-Output "Application Security Details:"
    create_file_if_not_exists "env/secrets.env"

    Write-Output ""
    $FERNET_KEY = "Zsy6-8REWdN0-FkIhgBy8k19MJ7elYNAv3MxkWHFGOk="
    $ACCESS_TOKEN_EXPIRE_MINUTES = 60
    $JWT_SECRET_KEY = "abababababababbabhha"
    $ALGORITHM = "HS256"
    $PDF_ENCRYPTION_SECRET = "pdfababababab"
    $fernet_key = Read-Host "FERNET KEY (default is $FERNET_KEY)"
    $access_token_expire_minutes = Read-Host "JWT ACCESS TOKEN EXPIRE MINUTES (default is $ACCESS_TOKEN_EXPIRE_MINUTES)"
    $jwt_secret_key = Read-Host "JWT KEY (default is $JWT_SECRET_KEY)"
    $algorithm = Read-Host "JWT ALGORITHM (default is $ALGORITHM)"
    $pdf_encryption_secret = Read-Host "PDF ENCRYPTION SECRET (default is $PDF_ENCRYPTION_SECRET)"

    Write-Output ""
    update_env_variable "env/secrets.env" "FERNET_KEY" ($fernet_key -or $FERNET_KEY) $true
    update_env_variable "env/secrets.env" "ACCESS_TOKEN_EXPIRE_MINUTES" ($access_token_expire_minutes -or $ACCESS_TOKEN_EXPIRE_MINUTES) $true
    update_env_variable "env/secrets.env" "JWT_SECRET_KEY" ($jwt_secret_key -or $JWT_SECRET_KEY) $true
    update_env_variable "env/secrets.env" "ALGORITHM" ($algorithm -or $ALGORITHM) $true
    update_env_variable "env/secrets.env" "PDF_ENCRYPTION_SECRET" ($pdf_encryption_secret -or $PDF_ENCRYPTION_SECRET) $true

    Write-Output "Unit Testing Details: "
    create_file_if_not_exists "env/tests.env"

    Write-Output ""
    $EMAIL_SENDER_UNIT_TEST = "laamiri.ouail@etu.uae.ac.ma"
    $EMAIL_RECEIVER_UNIT_TEST = "laamiriouail@gmail.com"
    $PASSWORD_UNIT_TEST = "cfkd dihq xxyw ugin "
    while ($true) {
        $email_sender_unit_test = Read-Host "Enter the email sender for unit test"

        # Check if the email address is valid
        if (is_valid_email $email_sender_unit_test) {
            break  # Break the loop if email address is valid
        } else {
            Write-Output ""
            Write-Output "Error: Invalid email address '$email_sender_unit_test'."
        }
    }

    Write-Output ""
    while ($true) {
        Write-Output -NoNewline "Password for unit test email (xxxx xxxx xxxx xxxx): "
        $password = read_password

        # Call your function to validate email password structure
        if (is_gmail_password_structure $password) {
            break
        } else {
            Write-Output "Error: Invalid email password structure. Password must consist of four segments separated by spaces, each segment must be exactly four characters long."
        }
    }

    Write-Output ""

    while ($true) {
        $email_receiver_unit_test = Read-Host "Enter the email receiver for unit test"

        # Check if the email address is valid
        if (is_valid_email $email_receiver_unit_test) {
            break  # Break the loop if email address is valid
        } else {
            Write-Output ""
            Write-Output "Error: Invalid email address '$email_receiver_unit_test'."
        }
    }

    update_env_variable "env/tests.env" "EMAIL_SENDER_UNIT_TEST" $email_sender_unit_test $true
    update_env_variable "env/tests.env" "EMAIL_RECEIVER_UNIT_TEST" $email_receiver_unit_test $true
    update_env_variable "env/tests.env" "PASSWORD_UNIT_TEST" $password $false
}
    
# Execute the main function
main
