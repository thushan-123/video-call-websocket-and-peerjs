from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

MYSQL_DB_URL = os.getenv("MYSQL_DATABASE_URL")
print(MYSQL_DB_URL)

# POSTGRESQL_DATABASE_URL = "postgresql://root:thush@localhost/school"

engine = create_engine(MYSQL_DB_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()