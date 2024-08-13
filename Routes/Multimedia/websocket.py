from fastapi import APIRouter , websockets
from fastapi.security import OAuth2PasswordBearer
from Authorized.auth import verify_token

router = APIRouter()