from fastapi import APIRouter
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from Authorized.auth import verify_token
from Loggers.log import err_log, app_log

router = APIRouter()


