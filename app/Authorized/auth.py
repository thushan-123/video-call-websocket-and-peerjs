from datetime import datetime, timedelta
from jose import JWTError, jwt
from typing import Optional
import os
from dotenv import load_dotenv
from Loggers.log import err_log, app_log

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("TIME"))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    try:
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        app_log.info("|auth - create_access_token| create successfully")
        return encoded_jwt
    except Exception as e:
        err_log.error(f"|auth ->create_access_token| -> {e}")


def verify_token(token: str):
    try:
        data_dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        app_log.info("|auth -> verify_token| - successful Decode JWT")
        return data_dict
    except JWTError as e:
        err_log.error(f"|auth - verify_token| -> {e}")
        return None
