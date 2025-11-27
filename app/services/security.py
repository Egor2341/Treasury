import datetime
import os
from typing import Dict

import jwt
from dotenv import load_dotenv
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer

from exceptions.InvalidTokenError import InvalidTokenError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

load_dotenv()
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_jwt_token(data: Dict):
    to_encode = data.copy()
    expire = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def get_user_from_token(token:str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload.get("sub")
    except jwt.ExpiredSignatureError:
        raise InvalidTokenError("The token has expired")
    except jwt.InvalidTokenError:
        raise InvalidTokenError("Invalid token")

