from jose import jwt
from datetime import datetime, timedelta, timezone
import os
import sys
parent_dir = os.path.abspath(os.path.join(os.getcwd(), '.'))
sys.path.append(parent_dir)
from dotenv import load_dotenv
from pathlib import Path
# Load variables from the specified .env file
load_dotenv(dotenv_path=str(Path("./env/secrets.env")))

ACCESS_TOKEN_EXPIRE_MINUTES=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
SECRET_KEY=os.getenv("SECRET_KEY")
ALGORITHM=os.getenv("ALGORITHM")

# Function to create access token
def create_access_token(user_id: str) -> str:
    """
    Create an access token for a user.

    Parameters:
        user_id (str): The user ID for whom the access token is being generated.

    Returns:
        str: The encoded JWT access token.
    """
    expires_delta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"sub": user_id, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Function to verify and decode JWT token
def decode_access_token(token: str) -> dict:
    """
    Decode and verify a JWT access token.

    Parameters:
        token (str): The JWT access token to decode and verify.

    Returns:
        dict: A dictionary containing the validation result and user ID.
            - 'valid' (bool): True if the token is valid, False otherwise.
            - 'user_id' (str or None): The user ID if the token is valid, None otherwise.
    """
    try:
        # Decode the token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        # Convert expiration time from seconds since epoch to datetime object
        expiration_time = datetime.fromtimestamp(payload["exp"], timezone.utc)
        
        # Check if the token is expired
        now = datetime.now(timezone.utc)
        if expiration_time < now:
            return {"valid": False, "user_id": None}
        
        # Token is valid and not expired
        user_id = payload.get("sub")
        return {"valid": True, "user_id": user_id}
    except jwt.ExpiredSignatureError:
        # Token has expired
        return {"valid": False, "user_id": None}
    except jwt.InvalidTokenError:
        # Token is invalid
        return {"valid": False, "user_id": None}