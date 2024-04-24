from fastapi import HTTPException, status

class FileExtensionException(HTTPException):
    """
    Custom exception for file extension errors.

    Parameters:
        detail (str): Additional details about the exception.
    """
    def __init__(self, detail: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = detail

class FileNotFoundException(HTTPException):
    """
    Custom exception for file not found errors.

    Parameters:
        detail (str): Additional details about the exception.
    """
    def __init__(self, detail: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = detail

class PasswordException(HTTPException):
    """
    Custom exception for password-related errors.

    Parameters:
        detail (str): Additional details about the exception.
    """
    def __init__(self, detail: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = detail

class EmailException(HTTPException):
    """
    Custom exception for email-related errors.

    Parameters:
        detail (str): Additional details about the exception.
    """
    def __init__(self, detail: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = detail

class EmailConnectionFailedException(HTTPException):
    """
    Custom exception for email connection failures.

    Parameters:
        detail (str): Additional details about the exception.
    """
    def __init__(self, detail: str):
        self.status_code = status.HTTP_503_SERVICE_UNAVAILABLE
        self.detail = detail

class LinkException(HTTPException):
    """
    Custom exception for link-related errors.

    Parameters:
        detail (str): Additional details about the exception.
    """
    def __init__(self, detail: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = detail


class UserExistException(HTTPException):
    """
    Custom exception for user creation errors.

    Parameters:
        detail (str): Additional details about the exception.
    """
    def __init__(self, detail: str):
        self.status_code = status.HTTP_400_BAD_REQUEST
        self.detail = detail
