from jose import jwt
from datetime import datetime, timedelta, timezone


# Function to create access token
def create_access_token(user_id: str,access_token_expire_minutes:str,jwt_secret_key:str,algorithm:str) -> str:
    expires_delta = timedelta(minutes=access_token_expire_minutes)
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {"sub": user_id, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, jwt_secret_key, algorithm=algorithm)
    return encoded_jwt


# Function to verify and decode JWT token
def decode_access_token(token: str,jwt_secret_key:str,algorithm:str) -> dict:
    try:
        # Decode the token
        payload = jwt.decode(token, jwt, algorithms=[algorithm])
        
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