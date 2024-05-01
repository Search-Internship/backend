# Function to create a folder if it doesn't exist
function create_folder_if_not_exists {
    param(
        [string]$folder_path
    )
    if (-not (Test-Path $folder_path -PathType Container)) {
        New-Item -ItemType Directory -Path $folder_path | Out-Null
        Write-Host "Folder '$folder_path' created."
    } else {
        Write-Host "Folder '$folder_path' already exists."
    }
}

# Function to create a file if it doesn't exist
function create_file_if_not_exists {
    param(
        [string]$file_path
    )
    if (-not (Test-Path $file_path -PathType Leaf)) {
        New-Item -ItemType File -Path $file_path | Out-Null
        Write-Host "File '$file_path' created."
    } else {
        Write-Host "File '$file_path' already exists."
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
    (Get-Content $file_path) | Where-Object {$_ -notmatch "^$variable_name="} | Set-Content $file_path

    # Add the new variable to the file
    Add-Content -Path $file_path -Value "$variable_name=$value"

    # Print the appropriate message based on the print_value flag
    if ($print_value) {
        Write-Host "Variable '$variable_name' set to '$value' in '$file_path' file."
    } else {
        Write-Host "Variable '$variable_name' set to '**' in '$file_path' file."
    }
}

# Function to install a Python module
function install_python_module {
    param(
        [string]$module_name
    )
    if (pip install $module_name) {
        Write-Host "Module Installation: $module_name installed successfully."
    } else {
        Write-Host "Module Installation: $module_name not installed."
    }
}

# Function to create and activate a virtual environment
function create_and_activate_venv {
    param(
        [string]$venv_name
    )
    $python_cmd = "python"
    $create_cmd = "$python_cmd -m venv $venv_name"
    $activate_cmd = "$venv_name\Scripts\Activate"

    # Create the virtual environment
    Invoke-Expression $create_cmd

    # Activate the virtual environment
    Invoke-Expression $activate_cmd

    Write-Host "Virtual environment '$venv_name' created and activated."
}

# Function to install requirements from a file
function install_requirements {
    param(
        [string]$requirements_file
    )
    if (pip install -r $requirements_file) {
        Write-Host "Requirements installed successfully."
    } else {
        Write-Host "Error installing requirements."
    }
}

# Function to read password securely
function read_password {
    $password = Read-Host "Enter password" -AsSecureString
    $password_text = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto([System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($password))
    return $password_text
}

# Main function
function main {
    $DB_TYPE = "sqlite"
    Write-Host
    Write-Host "Available database type : mysql , mariadb, postgresql, oracle, oracledb, mssql, sqlserver, sqlite"
    $db_type = Read-Host "Enter the database type (default is $DB_TYPE): "

    if ($db_type -notin "mysql", "mariadb", "postgresql", "oracle", "oracledb", "mssql", "sqlserver", "sqlite") {
        Write-Host "$db_type not in ['mysql', 'mariadb', 'postgresql', 'oracle', 'oracledb', 'mssql', 'sqlserver', 'sqlite']"
        exit 1
    }

    if ([string]::IsNullOrEmpty($db_type)) {
        $db_type = $DB_TYPE
    }

    Write-Host
    $venv_name = Read-Host "Enter the virtual environment name (default is venv): "
    # Check if $venv_name is empty, if so, set it to the default value

    if ([string]::IsNullOrEmpty($venv_name)) {
        $venv_name = "venv"
    }

    create_and_activate_venv $venv_name

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
    if (-not [string]::IsNullOrEmpty($db_module)) {
        install_python_module $db_module
    } else {
        Write-Host "No database module required for SQLite."
    }

    install_requirements "requirements/base.txt"

    create_folder_if_not_exists "env"
    create_file_if_not_exists "env/database.env"

    if ($db_type -ne "sqlite") {
        $default_db_name = "easyinternship"
        $default_host = "localhost"
        $default_user_name = "root"
        $default_password = ""
        Write-Host "Enter the database ($db_type) details:"
        Write-Host
        $db_name = Read-Host "Enter the database name (default is easyinternship): "
        Write-Host
        $db_host = Read-Host "Enter the host (default is localhost): "
        Write-Host
        $user_name = Read-Host "Enter the username (default is root): "
        Write-Host
        $password = read_password
        if ([string]::IsNullOrEmpty($db_name)) {
            $db_name = "easyinternship"
        }
        if ([string]::IsNullOrEmpty($db_host)) {
            $db_host = "localhost"
        }
        if ([string]::IsNullOrEmpty($user_name)) {
            $user_name = "root"
        }
        update_env_variable "env/database.env" "DB_NAME" $db_name 1
        update_env_variable "env/database.env" "HOST" $db_host 1
        update_env_variable "env/database.env" "DB_TYPE" $db_type 1
        update_env_variable "env/database.env" "USER_NAME" $user_name 1
        update_env_variable "env/database.env" "PASSWORD" $password 0
    }

    if ($db_type -eq "mysql" -or $db_type -eq "mariadb") {
        $port = Read-Host "Enter the port (default is 3306): "
        if ([string]::IsNullOrEmpty($port)) {
            $port = 3306
        }
        update_env_variable "env/database.env" "PORT" $port 1
        Write-Host
    } elseif ($db_type -eq "oracle" -or $db_type -eq "oracledb") {
        $port = Read-Host "Enter the port (default is 1521): "
        if ([string]::IsNullOrEmpty($port)) {
            $port = 1521
        }
        $service_name = Read-Host "Enter the service name (default is ORCL): "
        if ([string]::IsNullOrEmpty($service_name)) {
            $service_name = "ORCL"
        }
        update_env_variable "env/database.env" "PORT" $port 1
        update_env_variable "env/database.env" "SERVICE_NAME" $service_name 1
    } elseif ($db_type -eq "mssql" -or $db_type -eq "sqlserver") {
        $port = Read-Host "Enter the port (default is 1433): "
        if ([string]::IsNullOrEmpty($port)) {
            $port = 1433
        }
        update_env_variable "env/database.env" "PORT" $port 1
    } elseif ($db_type -eq "postgresql") {
        $port = Read-Host "Enter the port (default is 5432): "
        if ([string]::IsNullOrEmpty($port)) {
            $port = 5432
        }
        update_env_variable "env/database.env" "PORT" $port 1
    } elseif ($db_type -eq "sqlite") {
        $db_file_path = Read-Host "Enter the database file path: "
        update_env_variable "env/database.env" "DB_FILE_PATH" $db_file_path 1
    }

    Write-Host "Application Communication Details:"
    create_file_if_not_exists "env/communication.env"

    Write-Host
    while (1) {
        $email_address = Read-Host "Enter the email address: "

        # Check if the email address is valid
        if ($email_address -match '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$') {
            break  # Break the loop if email address is valid
        } else {
            Write-Host
            Write-Host "Error: Invalid email address '$email_address'."
        }
    }

    # Loop until a valid email password is entered
    Write-Host
    while (1) {
        $password = read_password

        # Call your function to validate email password structure
        if ($password -match '^.... .... .... ....$') {
            break
        } else {
            Write-Host "Error: Invalid email password structure. Password must consist of four segments separated by spaces, each segment must be exactly four characters long."
        }
    }

    update_env_variable "env/communication.env" "EMAIL_PROJECT" $email_address 1
    update_env_variable "env/communication.env" "PASSWORD_EMAIL_PROJECT" $password 0

    Write-Host "Application Security Details:"
    create_file_if_not_exists "env/secrets.env"

    Write-Host
    $fernet_key = Read-Host "FERNET KEY (default is Zsy6-8REWdN0-FkIhgBy8k19MJ7elYNAv3MxkWHFGOk=): "
    Write-Host
    $access_token_expire_minutes = Read-Host "JWT ACCESS TOKEN EXPIRE MINUTES (default is 60): "
    Write-Host
    $jwt_secret_key = Read-Host "JWT KEY (default is abababababababbabhha): "
    Write-Host
    $algorithm = Read-Host "JWT ALGORITHM (default is HS256): "
    Write-Host
    $pdf_encryption_secret = Read-Host "PDF ENCRYPTION SECRET (default is pdfababababab): "
    Write-Host
    if ([string]::IsNullOrEmpty($fernet_key)) {
        $fernet_key = "Zsy6-8REWdN0-FkIhgBy8k19MJ7elYNAv3MxkWHFGOk="
    }
    if ([string]::IsNullOrEmpty($access_token_expire_minutes)) {
        $access_token_expire_minutes = "60"
    }
    if ([string]::IsNullOrEmpty($jwt_secret_key)) {
        $jwt_secret_key = "abababababababbabhha"
    }
    if ([string]::IsNullOrEmpty($algorithm)) {
        $algorithm = "HS256"
    }
    if ([string]::IsNullOrEmpty($pdf_encryption_secret)) {
        $pdf_encryption_secret = "pdfababababab"
    }
    update_env_variable "env/secrets.env" "FERNET_KEY" $fernet_key 1
    update_env_variable "env/secrets.env" "ACCESS_TOKEN_EXPIRE_MINUTES" $access_token_expire_minutes 1
    update_env_variable "env/secrets.env" "JWT_SECRET_KEY" $jwt_secret_key 1
    update_env_variable "env/secrets.env" "ALGORITHM" $algorithm 1
    update_env_variable "env/secrets.env" "PDF_ENCRYPTION_SECRET" $pdf_encryption_secret 1

    Write-Host "Unit Testing Details: "
    create_file_if_not_exists "env/tests.env"

    Write-Host
    while (1) {
        $email_sender_unit_test = Read-Host "Enter the email sender for unit test : "

        # Check if the email address is valid
        if ($email_sender_unit_test -match '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$') {
            break  # Break the loop if email address is valid
        } else {
            Write-Host
            Write-Host "Error: Invalid email address '$email_sender_unit_test'."
        }
    }

    Write-Host
    while (1) {
        $password = read_password

        # Call your function to validate email password structure
        if ($password -match '^.... .... .... ....$') {
            break
        } else {
            Write-Host "Error: Invalid email password structure. Password must consist of four segments separated by spaces, each segment must be exactly four characters long."
        }
    }

    Write-Host

    while (1) {
        $email_receiver_unit_test = Read-Host "Enter the email receiver for unit test : "

        # Check if the email address is valid
        if ($email_receiver_unit_test -match '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$') {
            break  # Break the loop if email address is valid
        } else {
            Write-Host
            Write-Host "Error: Invalid email address '$email_receiver_unit_test'."
        }
    }

    update_env_variable "env/tests.env" "EMAIL_SENDER_UNIT_TEST" $email_sender_unit_test 1
    update_env_variable "env/tests.env" "EMAIL_RECEIVER_UNIT_TEST" $email_receiver_unit_test 1
    update_env_variable "env/tests.env" "PASSWORD_UNIT_TEST" $password 0

    ## Create the database
    if ($db_type -eq "mysql" -or $db_type -eq "mariadb") {
        python scipts\databases\mysql.py
    } elseif ($db_type -eq "oracle" -or $db_type -eq "oracledb") {
        python scipts\databases\oracle.py
    } elseif ($db_type -eq "mssql" -or $db_type -eq "sqlserver") {
        python scipts\databases\mssql.py
    } elseif ($db_type -eq "postgresql") {
        python scipts\databases\postgresql.py
    } elseif ($db_type -eq "sqlite") {
        python scipts\databases\sqlite.py
    }




}

# Execute the main function
main