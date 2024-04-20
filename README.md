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
## Running the app : 
```bash
# Run application
$ uvicorn src.main:app --workers 1 --host 127.0.0.1 --port 8000 --reload --log-level info
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

## Endpoints

### 1. GET /
- **Description:** Returns a message indicating that the service is working properly.
- **Response:** JSON object with a message.
- **Status Code:** 200 OK

### 2. POST /send/
- **Description:** Sends emails to the specified recipients.
- **Request:**
  - **emails:** UploadFile (TXT file containing email addresses)
  - **email_body:** str (Email body text)
  - **resume:** UploadFile (PDF file containing resume)
  - **sender_email:** str (Sender's email address)
  - **sender_password:** str (Sender's email password)
  - **email_subject:** str (Email subject)
  - **file_separator:** str (Separator used in the email file)
- **Response:** 
  - **success_receiver:** list (List of successfully sent email addresses)
  - **failed_receiver:** list (List of email addresses that failed to send)
- **Possible Responses:**
  - **200 OK:** The request was successful, and emails were sent to all recipients.
    ```json
    {
        "success_receiver": ["recipient1@example.com", "recipient2@example.com"],
        "failed_receiver": ["recipient3@example.com"]
    }
    ```
  - **400 Bad Request:** The request was malformed or missing required parameters.
    ```json
    {
        "detail": "Emails TXT files are missing."
    }
    ```
  - **422 Unprocessable Entity:** The request parameters were valid, but the server was unable to process the request due to semantic errors.
    ```json
    {
        "detail": "The email form is incorrect"
    }
    ```
  - **601 The server declined the request:** The request parameters were valid, but the email and password not valid.
    ```json
    {
        "detail": "Failed to connect to gmail."
    }
    ```
  - **500 Internal Server Error:** The server encountered an unexpected error while processing the request.
    ```json
    {
        "detail": "Internal Server Error"
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


## Stay in touch :
- Author - [Ouail Laamiri](https://www.linkedin.com/in/ouaillaamiri/)

## License

Ema-back is [GPL licensed](LICENSE).