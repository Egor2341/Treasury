import datetime
import os
from typing import Dict, Annotated, Any

import jwt
from dotenv import load_dotenv
from fastapi import HTTPException, status
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from exceptions.InvalidTokenError import InvalidTokenError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7


def create_access_token(data: Dict):
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: Dict):
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def get_user_roles(token:str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise InvalidTokenError("The token has expired")
    except jwt.InvalidTokenError:
        raise InvalidTokenError("Invalid token")

def get_user_from_token(token:str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise InvalidTokenError("The token has expired")
    except jwt.InvalidTokenError:
        raise InvalidTokenError("Invalid token")


class RoleChecker:
    def __init__(self, allowed_roles):
        self.allowed_roles = allowed_roles

    def __call__(self, params: Annotated[Any, Depends(get_user_roles)]):
        if any(role in self.allowed_roles for role in params["roles"]):
            return params["sub"]
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You don't have enough permissions")

