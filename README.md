## Description

ema-backend is a API for the search internship project.
## Installation :
### Development :
```bash
# install requirements
$ pip install -r requirements/base.txt 
```
### Test :
```bash
# install requirements
$ pip install -r requirements/test.txt 
```
### Production :
```bash
# install requirements
$ pip install -r requirements/prod.txt 
```

## Envirenment Variable :
### 1. `env/database.env` :
#### USER_NAME
- **Description**: The username used to authenticate to the MySQL database.
- **Example**: `USER_NAME="root"`

#### PASSWORD
- **Description**: The password used to authenticate to the MySQL database.
- **Example**: `PASSWORD="admin"`

#### PORT
- **Description**: The port number on which the MySQL database server is listening.
- **Example**: `PORT="3306"`

#### HOST
- **Description**: The hostname or IP address of the MySQL database server.
- **Example**: `HOST="localhost"`

#### DB_NAME
- **Description**: The name of the MySQL database.
- **Example**: `DB_NAME="easyinternship"`

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

#### SECRET_KEY
- **Description**: The secret key used for JWT token encoding and decoding.
- **Example**: `SECRET_KEY="abababababababbabhha"`

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



## Running the app : 
```bash
# Run application
$ python3 scripts/database.py ; uvicorn src.main:app --host 127.0.0.1 --port 5000 --reload
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

## API Endpoints Documentation

### `/api/`

#### `GET /`
- **Description**: Endpoint to check if the API is running properly.
- **Response**:
  - **Status Code**: 200 OK
  - **Response Body**:
    ```json
    {
        "message": "I am working good !"
    }
    ```

### `/api/email/send-internship`

#### `POST /email/send-internship`
- **Description**: Endpoint to send internship emails.
- **Request Body**:
  - `emails` (file): A text file containing email addresses.
  - `email_body` (string): The body of the email to be sent.
  - `resume` (file): The resume file to be attached.
  - `sender_email` (string): The sender's email address.
  - `sender_password` (string): The sender's email password.
  - `email_subject` (string): The subject of the email.
  - `file_separator` (string): The separator used in the emails file.
- **Response**:
  - **Status Code**: 200 OK
  - **Response Body**:
    ```json
    {
        "success_receiver": ["email1@example.com", "email2@example.com"],
        "failed_receiver": ["email3@example.com"]
    }
    ```
- **Possible Errors**:
  - 400 Bad Request:
    - If the emails file is missing.
    - If the resume file is missing.
    - If the emails file is not a TXT file.
    - If the resume file is not a PDF file.
    - If the password form is incorrect.
    - If the email form is incorrect.
  - 503 Service Unavailable:
    - If failed to connect to the sender's email account.
- **Field Formats**:
  - `emails` (file): A text file containing email addresses separated by the specified separator.
  - `email_body` (string): Html string.
  - `resume` (file): A PDF file.
  - `sender_email` (string): A valid email address.
  - `sender_password` (string): A password following a specific format (four segments separated by spaces, each segment exactly four characters long).
  - `email_subject` (string): Any string.
  - `file_separator` (string): Any string used to separate email addresses in the emails file.



### `/api/users/`

#### `POST /users/`
- **Description**: Endpoint to create a new user.
- **Request Body**:
  - `username` (string): The username of the new user.
  - `email` (string): The email address of the new user.
  - `linkedin_link` (string, optional): The LinkedIn profile link of the new user.
  - `password` (string): The password of the new user.
  - `phone_number` (string): The phone number of the new user.
  - `email_password` (string): The password for the user's email account.
- **Response**:
  - **Status Code**: 200 OK
  - **Response Body**:
    ```json
    {
        "message": "User created successfully"
    }
    ```
- **Possible Errors**:
  - 400 Bad Request:
    - If the email is invalid.
    - If the email password structure is invalid.
    - If the password structure is invalid.
    - If the LinkedIn profile link structure is invalid.
- **Field Formats**:
  - `username` (string): Any string.
  - `email` (string): A valid email address.
  - `linkedin_link` (string, optional): A LinkedIn profile link or an empty string.
  - `password` (string): A password following a specific format (contains at least one lowercase character, one uppercase character, one digit, and has a minimum length of 8 characters).
  - `phone_number` (string): Any string.
  - `email_password` (string, optional): A password following a specific format (four segments separated by spaces, each segment exactly four characters long), or an empty string.

### `/api/users/login`

#### `POST /`
- **Description**: Endpoint to authenticate a user and generate an access token.
- **Parameters**:
  - `username_or_email` (required): The username or email of the user.
  - `password` (required): The password of the user.
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

### `/api/users/login`
#### `POST /`
- **Description**: Endpoint to authenticate a user and generate an access token.
- **Parameters**:
  - `username_or_email` (required): The username or email of the user.
  - `password` (required): The password of the user.
- **Response**:
  - **Status Code**: 200 OK
    - **Response Body**:
      ```json
      {
          "access_token": "your-access-token",
          "token_type": "bearer"
      }
      ```  
  - **Status Code**: 401 OK
    - **Response Body**:
      ```json
      {
          "detail":"Invalid credentials"
      }
      ```
  

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