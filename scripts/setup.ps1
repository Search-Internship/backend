# Function to create a folder if it doesn't exist
function create-folder-if-not-exists {
    param (
        [string]$folder_path
    )
    if (-not (Test-Path $folder_path -PathType Container)) {
        New-Item -Path $folder_path -ItemType Directory | Out-Null
        Write-Output "Folder '$folder_path' created."
    } else {
        Write-Output "Folder '$folder_path' already exists."
    }
}

# Function to create a file if it doesn't exist
function create-file-if-not-exists {
    param (
        [string]$file_path
    )
    if (-not (Test-Path $file_path -PathType Leaf)) {
        New-Item -Path $file_path -ItemType File | Out-Null
        Write-Output "File '$file_path' created."
    } else {
        Write-Output "File '$file_path' already exists."
    }
}

# Function to update environment variable in a file
function update-env-variable {
    param (
        [string]$file_path,
        [string]$variable_name,
        [string]$value,
        [bool]$print_value
    )

    # Delete the line if it exists
    (Get-Content $file_path) -replace "^$variable_name=.*", "" | Set-Content $file_path

    # Add the new variable to the file
    Add-Content $file_path "$variable_name=$value"

    # Print the appropriate message based on the print_value flag
    if ($print_value) {
        Write-Output "Variable '$variable_name' set to '$value' in '$file_path' file."
    } else {
        Write-Output "Variable '$variable_name' set to '****' in '$file_path' file."
    }
}

# Function to install a Python module
function install-python-module {
    param (
        [string]$module_name
    )
    if (pip install $module_name) {
        Write-Output "Module Installation: $module_name installed successfully."
    } else {
        Write-Output "Module Installation: $module_name not installed."
    }
}

# Function to read password securely
function read-password {
    $password = Read-Host "Enter password" -AsSecureString
    $BSTR = [System.Runtime.InteropServices.Marshal]::SecureStringToBSTR($password)
    $password_text = [System.Runtime.InteropServices.Marshal]::PtrToStringAuto($BSTR)
    return $password_text
}

# Function to check if a password follows Gmail password structure
function is-gmail-password-structure {
    param (
        [string]$password
    )
    $pattern = '^\w{4} \w{4} \w{4} \w{4}$'
    if ($password -match $pattern) {
        return $true
    } else {
        return $false
    }
}

# Function to check if an email address is valid
function is-valid-email {
    param (
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
    param (
        [string]$db_type
    )

    $db_type = $db_type.ToLower()
    if (-not (" mysql mariadb postgresql oracle oracledb mssql sqlserver sqlite" -split '\s+' -contains $db_type)) {
        Write-Host "Usage: $MyInvocation.MyCommand db_type"
        Write-Host "And db_type in ['mysql', 'mariadb', 'postgresql', 'oracle', 'oracledb', 'mssql', 'sqlserver', 'sqlite']"
        exit 1
    }

    if (-not $db_type) {
        $db_type = "sqlite"
    }

    $venv_name = "venv"

    create-folder-if-not-exists $venv_name

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
    if ($db_module) {
        install-python-module $db_module
    } else {
        Write-Host "No database module required for SQLite."
    }

    install-requirements "requirements/base.txt"

    create-folder-if-not-exists "env"
    create-file-if-not-exists "env/database.env"

    if ($db_type -ne "sqlite") {
        $default_db_name = "easyinternship"
        $default_host = "localhost"
        $default_user_name = "root"
        $default_password = ""
        Write-Host "Enter the database ($db_type) details:"
        Write-Host
        $db_name = Read-Host "Enter the database name (default is $default_db_name)"
        Write-Host
        $host = Read-Host "Enter the host (default is $default_host)"
        Write-Host
        $user_name = Read-Host "Enter the username (default is $default_user_name)"
        Write-Host
        Write-Host -NoNewline "Enter the password (default is vide): "
        $password = read-password
        Write-Host

        update-env-variable "env/database.env" "DB_NAME" "${db_name:-$default_db_name}" $true
        update-env-variable "env/database.env" "HOST" "${host:-$default_host}" $true
        update-env-variable "env/database.env" "DB_TYPE" "${db_type:-$default_db_type}" $true
        update-env-variable "env/database.env" "USER_NAME" "${user_name:-$default_user_name}" $true
        update-env-variable "env/database.env" "PASSWORD" "${password:-$default_password}" $false
    }

    if ($db_type -eq "mysql" -or $db_type -eq "mariadb") {
        $port = Read-Host "Enter the port (default is 3306)"
        update-env-variable "env/database.env" "PORT" "${port:-3306}" $true
        Write-Host
    } elseif ($db_type -eq "oracle" -or $db_type -eq "oracledb") {
        $port = Read-Host "Enter the port (default is 1521)"
        update-env-variable "env/database.env" "PORT" "${port:-1521}" $true
    } elseif ($db_type -eq "mssql" -or $db_type -eq "sqlserver") {
        $port = Read-Host "Enter the port (default is 1433)"
        update-env-variable "env/database.env" "PORT" "${port:-1433}" $true
    } elseif ($db_type -eq "postgresql") {
        $port = Read-Host "Enter the port (default is 5432)"
        update-env-variable "env/database.env" "PORT" "${port:-5432}" $true
    } elseif ($db_type -eq "sqlite") {
        $db_file_path = Read-Host "Enter the database file path"
        update-env-variable "env/database.env" "DB_FILE_PATH" "$db_file_path" $true
    }

    Write-Host "Application Communication Details:"
    Write-Host
    while ($true) {
        $email_address = Read-Host "Enter the email address"

        # Check if the email address is valid
        if (is-valid-email $email_address) {
            break  # Break the loop if email address is valid
        } else {
            Write-Host
            Write-Host "Error: Invalid email address '$email_address'."
        }
    }

    # Loop until a valid email password is entered
    Write-Host
    while ($true) {
        Write-Host -NoNewline "Enter the email password (xxxx xxxx xxxx xxxx): "
        $password = read-password

        # Call your function to validate email password structure
        if (is-gmail-password-structure $password) {
            break
        } else {
            Write-Host "Error: Invalid email password structure. Password must consist of four segments separated by spaces, each segment must be exactly four characters long."
        }
    }

    update-env-variable "env/communication.env" "EMAIL_PROJECT" "$email_address" $true
    update-env-variable "env/communication.env" "PASSWORD_EMAIL_PROJECT" "$password" $false

    Write-Host "Application Security Details:"
    Write-Host
    $FERNET_KEY = "Zsy6-8REWdN0-FkIhgBy8k19MJ7elYNAv3MxkWHFGOk="
    $ACCESS_TOKEN_EXPIRE_MINUTES = 60
    $JWT_SECRET_KEY = "abababababababbabhha"
    $ALGORITHM = "HS256"
    $PDF_ENCRYPTION_SECRET = "pdfababababab"
    $fernet_key = Read-Host "FERNET KEY (default is $FERNET_KEY)"
    Write-Host
    $access_token_expire_minutes = Read-Host "JWT ACCESS TOKEN EXPIRE MINUTES (default is $ACCESS_TOKEN_EXPIRE_MINUTES)"
    Write-Host
    $jwt_secret_key = Read-Host "JWT KEY (default is $JWT_SECRET_KEY)"
    Write-Host
    $algorithm = Read-Host "JWT ALGORITHM (default is $ALGORITHM)"
    Write-Host
    $pdf_encryption_secret = Read-Host "PDF ENCRYPTION SECRET (default is $PDF_ENCRYPTION_SECRET)"
    Write-Host
    update-env-variable "env/secrets.env" "FERNET_KEY" "${fernet_key:-$FERNET_KEY}" $true
    update-env-variable "env/secrets.env" "ACCESS_TOKEN_EXPIRE_MINUTES" "${access_token_expire_minutes:-$ACCESS_TOKEN_EXPIRE_MINUTES}" $true
    update-env-variable "env/secrets.env" "JWT_SECRET_KEY" "${jwt_secret_key:-$JWT_SECRET_KEY}" $true
    update-env-variable "env/secrets.env" "ALGORITHM" "${algorithm:-$ALGORITHM}" $true
    update-env-variable "env/secrets.env" "PDF_ENCRYPTION_SECRET" "${pdf_encryption_secret:-$PDF_ENCRYPTION_SECRET}" $true

    Write-Host "Unit Testing Details: "
    Write-Host
    $EMAIL_SENDER_UNIT_TEST = "laamiri.ouail@etu.uae.ac.ma"
    $EMAIL_RECEIVER_UNIT_TEST = "laamiriouail@gmail.com"
    $PASSWORD_UNIT_TEST = "cfkd dihq xxyw ugin "
    while ($true) {
        $email_sender_unit_test = Read-Host "Enter the email sender for unit test"

        # Check if the email address is valid
        if (is-valid-email $email_sender_unit_test) {
            break  # Break the loop if email address is valid
        } else {
            Write-Host
            Write-Host "Error: Invalid email address '$email_sender_unit_test'."
        }
    }

    Write-Host
    while ($true) {
        Write-Host -NoNewline "Password for unit test email (xxxx xxxx xxxx xxxx): "
        $password = read-password

        # Call your function to validate email password structure
        if (is-gmail-password-structure $password) {
            break
        } else {
            Write-Host "Error: Invalid email password structure. Password must consist of four segments separated by spaces, each segment must be exactly four characters long."
        }
    }

    Write-Host

    while ($true) {
        $email_receiver_unit_test = Read-Host "Enter the email receiver for unit test"

        # Check if the email address is valid
        if (is-valid-email $email_receiver_unit_test) {
            break  # Break the loop if email address is valid
        } else {
            Write-Host
            Write-Host "Error: Invalid email address '$email_receiver_unit_test'."
        }
    }

    update-env-variable "env/unit_test.env" "EMAIL_SENDER_UNIT_TEST" "$email_sender_unit_test" $true
    update-env-variable "env/unit_test.env" "EMAIL_RECEIVER_UNIT_TEST" "$email_receiver_unit_test" $true
    update-env-variable "env/unit_test.env" "PASSWORD_UNIT_TEST" "$password" $false
}

# Execute the main function with command-line argument
main $args
