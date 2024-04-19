## Description

ema-backend 
## Installation :
### Development :
```bash
# install requirements
$ pip install -r requirements/base.txt 
```
### Test :
```bash
# install requirements
$ pip install -r requirements/base.txt 
```
### Production :
```bash
# install requirements
$ pip install -r requirements/prod.txt 
```
## Running the app : 
```bash
# Run application
$ uvicorn main:app --workers 1 --host 127.0.0.1 --port 3000 --reload --log-level info
```
## Build Docker image : 
```bash
# build a docker image
$ docker build -t ema-back .
```
## Running the app in the Docker : 
```bash
# Run docker image
$ docker run -p 5000:5000 ema-back
```

## Available Endpoints

### 1. Index

- **Endpoint:** `/`
- **Method:** GET
- **Description:** Check if the ema-back is operational.

### 2. Upload Image for Image-Client Category

- **Endpoint:** `/drive/image-client`
- **Method:** POST
- **Description:** Upload an image for the image-client category to Google Drive.
- **Parameters:** 
    - `file: FileParams` - JSON body with the file_path parameter.
- **Response:**
    - `200`: Successful file upload with the file URL.
    - `500`: Failed to upload file.

### 3. Upload Image for Image-Vihecule Category

- **Endpoint:** `/drive/image-vihecule`
- **Method:** POST
- **Description:** Upload an image for the image-vihecule category to Google Drive.
- **Parameters:** 
    - `file: FileParams` - JSON body with the file_path parameter.
- **Response:**
    - `200`: Successful file upload with the file URL.
    - `500`: Failed to upload file.

### 4. Upload PDF Contract to Drive

- **Endpoint:** `drive/contract-pdf`
- **Method:** POST
- **Description:** Upload a PDF contract to Google Drive.
- **Parameters:** 
    - `file: FileParams` - JSON body with the file_path parameter.
- **Response:**
    - `200`: Successful file upload with the file URL.
    - `500`: Failed to upload file.

### 5. Upload Image for Driver Licence Category

- **Endpoint:** `/drive/driver-licence`
- **Method:** POST
- **Description:** Upload an image for the driver-licence category to Google Drive.
- **Parameters:** 
  - `file: FileParams` - JSON body with the file_path parameter.
- **Response:**
  - `200`: Successful file upload with the file URL.
  - `500`: Failed to upload file.

### 6.  Upload Image for National Identity Card Category

- **Endpoint:** `/drive/national-identity-card`
- **Method:** POST
- **Description:** Upload an image for the national-identity-card category to Google Drive.
- **Parameters:** 
  - `file: FileParams` - JSON body with the file_path parameter.
- **Response:**
    - `200`: Successful file upload with the file URL.
    - `500`: Failed to upload file.







## Stay in touch :
- Author - [Ouail Laamiri](https://www.linkedin.com/in/ouaillaamiri/)
- Test - [Postman](https://www.postman.com/avionics-meteorologist-32935362/workspace/postman-api-fundamentals-student-expert/collection/29141176-282aba17-b309-429b-94ff-a7d13f6f4e1a?action=share&creator=29141176)
- Documentation - [Postman](https://documenter.getpostman.com/view/29141176/2s9Ykt4eMm)

## License

File-Service is [GPL licensed](LICENSE).