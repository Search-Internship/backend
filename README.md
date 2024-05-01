## Description

ema-backend is a API for the search internship project.

## Setup Project :

### Linux & Mac :
```bash
$ chmod +x ./scripts/setup.sh
$ ./scripts/setup.sh
```
### Windows :
```powershell
$ Set-ExecutionPolicy Unrestricted -Scope CurrentUser -Force
$ .\scripts\setup.ps1
```


**Note**: This note serves as a reminder to users to be careful while running the setup scripts, especially if they're reusing a database name that may exist already.





## Envirenment Variable :
### 1. `env/database.env` :
#### USER_NAME (ALL - {sqlite})
- **Description**: The username used to authenticate to the database.
- **Example**: `USER_NAME="root"`

#### PASSWORD (ALL - {sqlite})
- **Description**: The password used to authenticate to the database.
- **Example**: `PASSWORD="admin"`

#### PORT (ALL - {sqlite})
- **Description**: The port number on which the database server is listening.
- **Example**: `PORT="3306"`

#### HOST (ALL - {sqlite})
- **Description**: The hostname or IP address of the database server.
- **Example**: `HOST="localhost"`

#### DB_NAME (ALL - {sqlite})
- **Description**: The name of the database.
- **Example**: `DB_NAME="easyinternship"`

#### DB_TYPE (ALL - {sqlite})
- **Description**: The type of the database ['mysql','mariadb','postgresql','oracle','oracledb','mssql','sqlserver','sqlite'].
- **Example**: `DB_TYPE="mysql"`

#### SERVICE_NAME (Only for Oracle)
- **Description**: The service name or SID of the Oracle database. This parameter is used to identify the specific Oracle instance to connect to.
- **Example**: `SERVICE_NAME="ORCL"`

#### DB_FILE_PATH (Only for Sqlite)
- **Description**: The file path for the SQLite database. This parameter is used when the database type is set to 'sqlite'.
- **Example**: `DB_FILE_PATH="/path/to/database.db"`

### 2. `env/secrets.env` :
#### FERNET_KEY
- **Description**: The key used for encryption and decryption with Fernet symmetric encryption.
- **Example**: `FERNET_KEY="Zsy6-8REWdN0-FkIhgBy8k19MJ7elYNAv3MxkWHFGOk="`
#### ALGORITHM
- **Description**: The algorithm used for JWT token encoding and decoding.
- **Example**: `ALGORITHM="HS256"`

#### ACCESS_TOKEN_EXPIRE_MINUTES
- **Description**: The duration (in minutes) after which JWT access tokens expire.
- **Example**: `ACCESS_TOKEN_EXPIRE_MINUTES=60`

#### JWT_SECRET_KEY
- **Description**: The secret key used for JWT token encoding and decoding.
- **Example**: `JWT_SECRET_KEY="abababababababbabhha"`

#### PDF_ENCRYPTION_SECRET
- **Description**: The secret key used for PDF encryption and decryption.
- **Example**: `PDF_ENCRYPTION_SECRET="abababababababbabhha"`

### 3. `env/tests.env` :
#### EMAIL_SENDER_UNIT_TEST
- **Description**: The email address used as the sender for unit tests.
- **Example**: `EMAIL_SENDER_UNIT_TEST="laamiri.laamiri@etu.uae.ac.ma"`

#### EMAIL_RECEIVER_UNIT_TEST
- **Description**: The email address used as the receiver for unit tests. You can use one from a temporary email service like [Temp Mail](https://temp-mail.org/fr/).
- **Example**: `EMAIL_RECEIVER_UNIT_TEST="laamirilaamiri@gmail.com"`

#### PASSWORD_UNIT_TEST
- **Description**: The password used for unit tests.
- **Example**: `PASSWORD_UNIT_TEST="fyxx cazo wmyo mnfu"`

### 4. `env/communication.env` :
#### EMAIL_PROJECT
- **Description**: The password of project used for send emails for users.
- **Example**: `EMAIL_SENDER_UNIT_TEST="laamiri.laamiri@etu.uae.ac.ma"`

#### PASSWORD_EMAIL_PROJECT
- **Description**: The password of project used for send emails for users.
- **Example**: `PASSWORD_UNIT_TEST="fyxx cazo wmyo mnfu"`


## Running the app : 
```bash
# Run application
$ uvicorn src.main:app --host 127.0.0.1 --port 5000 --reload
```
## Build Docker image : 
```bash
# build a docker image
$ docker build -t ema-back .
```
## Running the app in the Docker : 
```bash
# Run docker image
$ docker run -p you_port:5000 ema-back
```

## Working with Docker Hub : 
```bash
# Pull docker image
$ docker pull ouail02/ema-back:tagname
# Run docker image
$ docker run -p you_port:5000 ema-back:tagname
```















































## Database Tables :

### Users : 

| Attribute       | Description                                         |
|-----------------|-----------------------------------------------------|
| id              | Unique identifier for the user.                     |
| username        | User's username.                                    |
| email           | User's email address (unique).                      |
| linkedin_link   | User's LinkedIn profile link.                       |
| password_hash   | Hashed password for user authentication.            |
| phone_number    | User's phone number.                                |
| date            | Date of the operation.                              |
| time            | Time of the operation.                              |
| email_password  | Encrypted email password.                           |

---

### Operations : 

| Attribute         | Description                                                                 |
|-------------------|-----------------------------------------------------------------------------|
| id                | Unique identifier for the operation.                                        |
| from_email        | Source email address.                                                       |
| date              | Date of the operation.                                                      |
| time              | Time of the operation.                                                      |
| email_body        | Body of the email.                                                          |
| subject           | Subject of the email.                                                       |
| success_receiver  | Receiver of the successful operation.                                       |
| failed_receiver   | Receiver of the failed operation.                                           |
| user_id           | Foreign key referencing the id of the user associated.                      |
| pdf_id            | The id of the pdf send in this operations and stored in data/resume         |


## API Endpoints

### Index Endpoint

- **URL**: `GET /api/`
- **Description**: Check if the server is running.
- **Response**:
  - **Status Code**: 200 OK
  - **Response Body**:
    ```json
    {
        "message": "I am working good !"
    }
    ```

### Sending Internship Emails

- **URL**: `POST /api/email/send-internship`
- **Description**: Send internship emails with attachments.
- **Request Body**:
  - `access_token` (string): User access token.
  - `emails` (file): Text file containing email addresses.
  - `email_body` (string): Body of the email to be sent.
  - `resume` (file): Resume file to be attached.
  - `email_subject` (string): Subject of the email.
  - `file_separator` (string): Separator used in the emails file.
- **Response**:
  - **Status Code**: 200 OK
  - **Response Body**:
    ```json
    {
        "success_receiver": ["email1@example.com", "email2@example.com"],
        "failed_receiver": ["email3@example.com"],
        "saved": true
    }
    ```

### Sending Verification Code

- **URL**: `POST /api/email/send-verification-code`
- **Description**: Send a verification code to the provided email address.
- **Request Body**:
  - `to` (string): Recipient email address.
  - `language` (string, optional): Language of the email content (default: "fr").
  - `type_` (string, optional): The type of code : number,string,mixte (default: "number").
  - `length` (int, optional): The length of code sended (default: 4).
  
- **Response**:
  - **Status Code**: 200 OK
  - **Response Body**:
    ```json
    {
        "code": "verification-code"
    }
    ```

### User Management

- **URL**: `POST /api/users/`
- **Description**: Create a new user.
- **Request Body**:
  - `username` (string): User's username.
  - `email` (string): User's email address.
  - `linkedin_link` (string, optional): User's LinkedIn profile link.
  - `password` (string): User's password.
  - `phone_number` (string): User's phone number.
  - `email_password` (string, optional): Password for user's email account.
- **Password Constraint**:
  - Passwords must meet the following criteria:
    - Contains at least one lowercase character
    - Contains at least one uppercase character
    - Contains at least one digit
    - Has a minimum length of 8 characters
  - Email Passwoed meet the following criteria:
    - General form : xxxx xxxx xxxx xxxx , with x is a number or alphabet
- **Response**:
  - **Status Code**: 200 OK
  - **Response Body**:
    ```json
    {
        "message": "User created successfully"
    }
    ```

### User Login

- **URL**: `POST /api/users/login`
- **Description**: Authenticate a user and generate an access token.
- **Request Body**:
  - `email` (string): User's email address.
  - `password` (string): User's password.
- **Response**:
  - **Status Code**:
    - 200 OK: Successful authentication.
    - 401 Unauthorized: Invalid credentials.
  - **Response Body** (for 200 OK):
    ```json
    {
        "access_token": "your-access-token",
        "token_type": "bearer"
    }
    ```

### Check Email Existence

- **URL**: `POST /api/users/email-exist`
- **Description**: Check if an email exists.
- **Request Body**:
  - `email` (string): The email address to check.
- **Response**:
  - **Status Code**: 200 OK
  - **Response Body**:
    ```json
    {
        "exist": true
    }
    ```
    - `exist` (boolean): Indicates whether the email exists (`true`) or not (`false`).



### Changing Password

- **URL**: `PUT /api/users/change-password`
- **Description**: Change the password for a user.
- **Request Body**:
  - `new_password` (string): The new password for the user.
  - `access_token` (string): Token for accessing the user account.
- **Password Constraint**:
  - Passwords must meet the following criteria:
    - Contains at least one lowercase character
    - Contains at least one uppercase character
    - Contains at least one digit
    - Has a minimum length of 8 characters
- **Response**:
  - **Status Code**: 200 OK
  - **Response Body**:
    ```json
    {
        "message": "Password changed successfully"
    }
    ```

### Forgot Password

- **URL**: `PUT /api/users/forgot-password`
- **Description**: Reset the password for a user who has forgotten it.
- **Request Body**:
  - `new_password` (string): The new password for the user.
  - `email` (string): The email address of the user.
- **Password Constraint**:
  - Passwords must meet the following criteria:
    - Contains at least one lowercase character
    - Contains at least one uppercase character
    - Contains at least one digit
    - Has a minimum length of 8 characters
- **Response**:
  - **Status Code**: 200 OK
  - **Response Body**:
    ```json
    {
        "message": "Password changed successfully"
    }
    ```



### Create Operation

- **URL**: `POST /api/operations/`
- **Description**: Create a new operation associated with a user.
- **Request Body**:
  - `email_body` (string): Body of the email.
  - `subject` (string): Subject of the email.
  - `success_receiver` (string): Comma-separated list of successful recipients' email addresses.
  - `failed_receiver` (string): Comma-separated list of failed recipients' email addresses.
  - `access_token` (string): User access token.
- **Response**:
  - **Status Code**: 200 OK
  - **Response Body**:
    ```json
    {
        "message": "Operation created successfully"
    }
    ```

### Get Operation by ID

- **URL**: `GET /api/operations/{access_token}/{operation_id}/`
- **Description**: Get an operation by its ID.
- **Response**:
  - **Status Code**: 200 OK
  - **Response Body**: Operation details.

### Get Operation by User ID

- **URL**: `GET /api/operations/{access_token}/`
- **Description**: Get all operations associated with a user.
- **Response**:
  - **Status Code**: 200 OK
  - **Response Body**: List of operations.

  








































## Project Structure :
This project's directory structure is inspired by the article "[Structuring a FastAPI App: An In-Depth Guide](https://medium.com/@ketansomvanshi007/structuring-a-fastapi-app-an-in-depth-guide-cdec3b8f4710)" on Medium.

- **chat** : Directory for chat related functionality
- **docker** : The `docker` directory includes Docker-related files for containerizing the FastAPI application. It typically contains a Dockerfile and a docker-compose.yml file for defining the application's Docker image and services.
- **models** : The `models` directory holds the data models or schemas used by the application. It includes files for defining the application's models and their relationships. This also helps us to implement DTO(Data Transfer through Objects) pattern where we are exchanging data in between different layers through these model instances.
- **requirements** : Directory for requirements related files
- **scripts** : The `scripts` directory contains utility scripts for various purposes, such as setting up the database or generating data. It typically includes scripts like init_db.sql for initializing the database.
- **tests** : The `tests` directory contains unit tests to ensure the correctness of the application. It typically includes subdirectories for different components, such as service tests, and each test file corresponds to a specific component or module.
- **utils** : The `utils` directory houses utility modules and files required for the application's functionality. It typically includes files for handling exceptions, providing helper functions, and implementing common functionality such as JWT token handling and password hashing.
- **temp** : Directory for temporary files
- **templates** : Directory for HTML templates
- **src** :  Directory for source code of FastAPI application
- **env** :  Directory for envrenment variables



## Stay in touch :
- Author - [Ouail Laamiri](https://www.linkedin.com/in/ouaillaamiri/)

## License

Ema-back is [GPL licensed](LICENSE).