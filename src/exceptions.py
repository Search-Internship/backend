from fastapi import HTTPException

class FileExtensionException(HTTPException):
    def __init__(self, detail: str):
        self.status_code = 400
        self.detail = detail

class FileNotFoundException(HTTPException):
    def __init__(self, detail: str):
        self.status_code = 400
        self.detail = detail

class PasswordException(HTTPException):
    def __init__(self, detail: str):
        self.status_code = 400
        self.detail = detail
























