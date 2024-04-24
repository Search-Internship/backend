# Function to create a folder if it doesn't exist
function create_folder_if_not_exists {
    param([string]$folder_path)
    if (-not (Test-Path $folder_path -PathType Container)) {
        New-Item -ItemType Directory -Path $folder_path | Out-Null
        Write-Host "Folder '$folder_path' created."
    } else {
        Write-Host "Folder '$folder_path' already exists."
    }
}

# Function to create a file if it doesn't exist
function create_file_if_not_exists {
    param([string]$file_path)
    if (-not (Test-Path $file_path -PathType Leaf)) {
        New-Item -ItemType File -Path $file_path | Out-Null
        Write-Host "File '$file_path' created."
    } else {
        Write-Host "File '$file_path' already exists."
    }
}

# Function to update environment variable in a file
function update_env_variable {
    param([string]$file_path, [string]$variable_name, [string]$default_value)
    if (-not ((Get-Content $file_path) -match "^$variable_name=")) {
        Add-Content -Path $file_path -Value "$variable_name=$default_value"
        Write-Host "Variable '$variable_name' set to '$default_value' in '$file_path' file."
    } else {
        Write-Host "Variable '$variable_name' already exists in '$file_path' file."
    }
}

# Function to install a Python module
function install_python_module {
    param([string]$module_name)
    if (pip install $module_name) {
        Write-Host "Module Installation: $module_name installed successfully."
    } else {
        Write-Host "Module Installation: $module_name not installed."
    }
}

# Function to create and activate a virtual environment
function create_and_activate_venv {
    param([string]$venv_name)
    $python_cmd = "python3"
    $create_cmd = "$python_cmd -m venv $venv_name"
    $activate_cmd = "$venv_name\Scripts\Activate.ps1"
    
    # Create the virtual environment
    & $create_cmd

    # Activate the virtual environment
    & $activate_cmd

    Write-Host "Virtual environment '$venv_name' created and activated."
}

# Function to install requirements from a file
function install_requirements {
    param([string]$requirements_file)
    if (pip install -r $requirements_file) {
        Write-Host "Requirements installed successfully."
    } else {
        Write-Host "Error installing requirements."
    }
}

# Main function
function main {
    param([string]$db_type)
    $db_type = $db_type.ToLower()
    $available_db = @{
        "mysql" = "mysql-connector-python";
        "postgresql" = "psycopg2";
        "oracle" = "cx_Oracle";
        "oracledb" = "cx_Oracle";
        "mssql" = "pymssql";
        "sqlserver" = "pymssql";
        "sqlite" = "";
    }

    if (-not $available_db.ContainsKey($db_type)) {
        Write-Host "Usage: $($MyInvocation.MyCommand.Name) db_type"
        Write-Host "And db_type in ['mysql', 'postgresql', 'oracle', 'oracledb', 'mssql', 'sqlserver', 'sqlite']"
        exit 1
    }

    if (-not $db_type) {
        $db_type = "sqlite"
    }

    $venv_name = "venv"

    create_and_activate_venv $venv_name

    $db_module = $available_db[$db_type]
    if ($db_module) {
        install_python_module $db_module
    } else {
        Write-Host "No database module required for SQLite."
    }

    install_requirements "requirements\base.txt"

    create_folder_if_not_exists "env"
    create_file_if_not_exists "env\database.env"
    update_env_variable "env\database.env" "DB_NAME" "easyinternship"
    update_env_variable "env\database.env" "HOST" "localhost"
    update_env_variable "env\database.env" "DB_TYPE" "$db_type"
    update_env_variable "env\database.env" "USER_NAME" "root"
    update_env_variable "env\database.env" "PASSWORD" "admin"
    update_env_variable "env\database.env" "DB_FILE_PATH" "database/data.db"
    if ($db_type -eq "mysql" -or $db_type -eq "mariadb") {
        update_env_variable "env/database.env" "PORT" "3306"
    }
    elseif ($db_type -eq "oracle" -or $db_type -eq "oracledb") {
        update_env_variable "env/database.env" "PORT" "1521"
    }
    elseif ($db_type -eq "mssql" -or $db_type -eq "sqlserver") {
        update_env_variable "env/database.env" "PORT" "1433"
    }
    elseif ($db_type -eq "postgresql") {
        update_env_variable "env/database.env" "PORT" "5432"
    }

        # Additional environment files and variables can be set here
    }

# Execute the main function with command-line argument
main $args
