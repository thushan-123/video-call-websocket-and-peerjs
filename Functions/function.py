import hashlib
from Databases.database import SessionLocal
import random
import string
from datetime import datetime, date
import pytz
import re


# Convert hash password
def password_hash(password: str) -> str:
    byte_string = password.encode()
    sha1_hash = hashlib.sha1()
    sha1_hash.update(byte_string)
    hex_digest = sha1_hash.hexdigest()
    return hex_digest


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Generate username  format { kamal-5d4t }
def generate_unique_username(first_name: str) -> str:
    # Generate a random string of 4 characters
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=4))
    # Combine first name and random string
    username = f"{first_name.lower()}-{random_string}"
    return username


# Verify the password
def verify_password(password1: str, password2: str) -> bool:
    if password1 == password2:
        return True
    else:
        return False


# Generate OTP -> 4 digits random choices
def get_OTP() -> str:
    otp = str(random.randint(1000, 9999))
    return otp


# Generate a 6 digits password

def get_gen_password() -> str:
    random_password = "".join(random.choices(string.ascii_lowercase + string.digits, k=6))
    return random_password


def get_sl_DateTime(Date_=False):
    sl_time_zone = pytz.timezone("Asia/colombo")  # Select sri lankan time zone
    sl_now_time = datetime.now(sl_time_zone)
    if Date_:
        return sl_now_time.date()
    else:
        return sl_now_time


def is_valid_email(email: str) -> bool:
    email_regx = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(email_regx,email) is not None
