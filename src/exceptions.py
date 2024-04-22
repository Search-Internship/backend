from fastapi import HTTPException,status

class FileExtensionException(HTTPException):
    def __init__(self, detail: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = detail

class FileNotFoundException(HTTPException):
    def __init__(self, detail: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = detail

class PasswordException(HTTPException):
    def __init__(self, detail: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = detail

class EmailException(HTTPException):
    def __init__(self, detail: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = detail


class EmailConnectionFailedException(HTTPException):
    def __init__(self, detail: str):
        self.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        self.detail = detail

class LinkException(HTTPException):
    def __init__(self, detail: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = detail






















