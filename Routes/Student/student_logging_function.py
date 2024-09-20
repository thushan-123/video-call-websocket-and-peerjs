from dns.resolver import query
from sqlalchemy.exc import IntegrityError

from Databases import models
from sqlalchemy import update, text
from sqlalchemy.orm import Session
from Functions.function import verify_password, password_hash, get_sl_DateTime
from Loggers.log import err_log, app_log


# student logging check db is valid student
def check_registered_student(db: Session, username: str, password: str):
    try:
        result = db.query(models.User).filter(models.User.user_name == username, models.User.verify == True,
                                              models.User.is_blocked == False).first()
        app_log.info("|student_logging_function - check_registered_student| -> get data from database success")
        if result:
            if verify_password(result.password, password):
                data_dict = {"id": result.id, "f_name": result.f_name, "l_name": result.l_name,
                             "user_name": result.user_name, "email": result.email, "mobile": result.mobile}
                return data_dict
            else:
                return None
        else:
            return None
    except Exception as e:
        err_log.error(f"|student_logging_function - check_registered_student| -> {e}")
        return None


# check for email and mobile number is already taken
def check_email_mobile(db: Session, email: str, mobile: int) -> bool:
    try:
        result_email = db.query(models.User).filter(models.User.email == email).first()
        result_mobile = db.query(models.User).filter(models.User.mobile == mobile).first()
        app_log.info("|student_logging_function - check_email_mobile| -> get data from database success")
        if result_email or result_mobile:
            return True
        else:
            return False
    except Exception as e:
        err_log.error(f"|student_logging_function - check_email_mobile| -> {e}")
        return False


# insert validate data in database
def insert_student_data(db: Session, f_name: str, l_name: str, user_name: str, email: str, mobile: int, password: str):
    try:
        query = models.User(f_name=f_name, l_name=l_name, user_name=user_name, email=email, mobile=mobile,
                            password=password, join_date=get_sl_DateTime(Date_=True))
        db.add(query)
        db.commit()
        db.refresh(query)
        app_log.info(f"|student_login_function - insert_student_data| new data row add successfully {user_name}")
        return True
    except IntegrityError as e:
        db.rollback()  # Rollback on integrity error
        err_log.error(f"|student_login_function - insert_student_data| -> {e}")
    except Exception as e:
        err_log.error(f"|student_login_function - insert_student_data| -> {e}")
        return False


# check student in the database
def check_student(db: Session, user_name: str, email: str):
    try:
        data = db.query(models.User).filter(models.User.user_name == user_name, models.User.email == email).first()
        app_log.info("|student_login_function - check_student| -> get student data successfully")
        if data:
            return True
        else:
            return False
    except Exception as e:
        err_log.error(f"|student_logging_function - check_student| -> {e}")
        return False


def get_student_data(db: Session, email: str):
    try:
        data = db.query(models.User).filter(models.User.email == email).first()
        app_log.info("|student_login_function - get_student_data| -> get student data successfully")
        if data:
            data_dict = {"id": data.id, "user_name": data.user_name, "email": data.email}
            return data_dict
        else:
            return False
    except Exception as e:
        err_log.error(f"|student_logging_function - get_student_data| -> {e}")


# update the student password after authentication
def update_password(db: Session, id: int, username: str, password: str) -> bool:
    try:
        query = update(models.User).where(models.User.id == id).values(password=password)
        db.execute(query)
        db.commit()
        app_log.info(f"|student_logging_function - update_password| -> password update successfully {username}")
        return True
    except Exception as e:
        err_log.error(f"|student_logging_function| -> {e}")
        return False
