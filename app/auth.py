from datetime import datetime, timedelta
from jose import jwt
from dotenv import load_dotenv
import os
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_access_token(data: dict):

    to_encode = data.copy()

    expire = datetime.now() + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

    return encoded_jwt

from jose import JWTError

def verify_token(token: str):

    try:

        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        return {
            "email": payload.get("sub"),
            "user_id": payload.get("user_id"),
            "role": payload.get("role")
}

    except JWTError as e:
        print("JWT ERROR:", e)
    return None

def get_current_user(token: str = Depends(oauth2_scheme)):

    user = verify_token(token)

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid or Expired Token"
    )

    return user
