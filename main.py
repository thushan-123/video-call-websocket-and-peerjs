from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from starlette.middleware.cors import CORSMiddleware
from Databases import models
from Databases.database import engine
import os
from dotenv import load_dotenv
from Routes.Admin import admin
from Routes.Student import student_logging
from Routes.video_stream import websocket
from Loggers.log import app_log, err_log, conference_log, log_conference
import uvicorn

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
REDIS_DB_URL = os.getenv("REDIS_DATABASE_URL")

# Create a Database tables
try:
    models.Base.metadata.create_all(bind=engine)
    app_log.info("Database is created")
except Exception as e:
    err_log.error(f"cannot create tables in mariaDB - {e}")

# Get the JWT token from the Authorization header
oauth2_schme = OAuth2PasswordBearer(tokenUrl="token")
#docs_url=None, redoc_url=None, openapi_url=None

app = FastAPI(docs_url=None, redoc_url=None, openapi_url=None)

origins = ["http://localhost", "http://localhost:8000"]
blocked_urls = ["/docs"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(admin.router, prefix="/api/v1/admin")
app.include_router(student_logging.router, prefix="/api/v1/user")
app.include_router(websocket.router)


