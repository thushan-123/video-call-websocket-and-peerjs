from Databases import models
from sqlalchemy import update, delete
from sqlalchemy.orm import Session
from Functions.function import password_hash, get_sl_DateTime, is_valid_email
from Loggers.log import err_log, app_log


# Insert student in the database by admin account -> verify is True (because student is added by admin)
def add_student(db: Session, trainer_id: str, f_name: str, l_name: str, username: str, email: str,
                mobile: int, password: str):
    query = models.User(trainer_id=trainer_id, f_name=f_name, l_name=l_name, user_name=username, email=email,
                        mobile=mobile, password=password_hash(password), join_date=get_sl_DateTime(Date_=True),
                        verify=True)
    try:
        db.add(query)
        db.commit()
        db.refresh(query)
        app_log.info("|student_function - add_student| -> student added successfully")
        return True
    except Exception as e:
        err_log.error(f"|student_function - add_add_student| -> {e}")
        return False


# update the student details by admin account
def update_student(db: Session, id: int, f_name: str, l_name: str, email: str, mobile: int):
    try:
        query = update(models.User).where(models.User.id == id).values(f_name=f_name, l_name=l_name, email=email,
                                                                       mobile=mobile)
        db.execute(query)
        db.commit()
        app_log.info("|student_function - update_student| -> student update successfully")
        return True
    except Exception as e:
        err_log.error(f"|student_function - update_student| -> {e}")
        return False


# Block or Unblock student
def block_student(db: Session, id: int, blocked=True):
    try:
        if blocked:
            query = update(models.User).where(models.User.id == id).values(is_blocked=True)
            db.execute(query)
            db.commit()
            app_log.info("|student_function - block_student| -> successfully blocked student")
            return True
        else:
            query = update(models.User).where(models.User.id == id).values(is_blocked=False)
            db.execute(query)
            db.commit()
            app_log.info("|student_function - block_student| -> successfully unblocked student")
            return True
    except Exception as e:
        err_log.error(f"|student_function - block_student| -> {e}")
        return False


# Delete student in User table using id
def delete_student(db: Session, id: int):
    try:
        query = delete(models.User).where(models.User.id == id)
        db.execute(query)
        db.commit()
        app_log.info("|student_function - delete_student| -> delete successfully")
        return True
    except Exception as e:
        err_log.error(f"|student_function - delete_student| -> {e}")
        return False


# Get all student detail sort by join_date
def get_student_detail(db: Session):
    try:
        result_set = db.query(models.User).filter(models.User.verify == True).all()

        app_log.info("|student_function - get_student_detail| -> get student detail query successfully execute")
        if not (result_set is None):
            data_list = []
            for row in result_set:
                row_dict = {"id": row.id, "trainer_id": row.trainer_id, "f_name": row.f_name, "l_name": row.l_name,
                            "user_name": row.user_name,
                            "email": row.email, "mobile": row.mobile, "join_date": row.join_date.strftime("%y-%m-%d"),
                            "is_blocked": row.is_blocked, "verify": row.verify}
                data_list.append(row_dict)
            data_list.reverse()
            return data_list
        else:
            return None
    except Exception as e:
        err_log.error(f"|student_function - get_student_detail| -> {e}")
        return None


# Search verify student  id, trainer_id , f_name, l_name, user_name, email, mobile
def search_student(db: Session, search: str):
    try:
        query = db.query(models.User).filter(models.User.verify == True)
        try:
            data_list = []
            search = int(search)
            result_set_id = query.filter(models.User.id == search).all()
            result_set_mobile = query.filter(models.User.mobile == search).all()
            result_set_trainer = query.filter(models.User.trainer_id == search).all()
            app_log.info("|student_function - search_student| -> search value is int , get result id or mobile")
            result_set = result_set_id + result_set_mobile + result_set_trainer
            if len(result_set) > 0:
                for row in result_set:
                    row_dict = {"id": row.id, "trainer_id": row.trainer_id, "f_name": row.f_name, "l_name": row.l_name,
                                "user_name": row.user_name,
                                "email": row.email, "mobile": row.mobile,
                                "join_date": row.join_date.strftime("%y-%m-%d"),
                                "is_blocked": row.is_blocked, "verify": row.verify}
                    data_list.append(row_dict)
                return data_list
            else:
                return None
        except:
            app_log.info(
                "|student_function - search_student| -> search value is not int or another error/ go to string search")
            data_list = []
            # Check string is email address
            if is_valid_email(search):
                app_log.info("|student_function - search_student| -> search without email")
                result_set_email = query.filter(models.User.email == search).all()
                if len(result_set_email) > 0:
                    for row in result_set_email:
                        row_dict = {"id": row.id, "trainer_id": row.trainer_id, "f_name": row.f_name,
                                    "l_name": row.l_name,
                                    "user_name": row.user_name,
                                    "email": row.email, "mobile": row.mobile,
                                    "join_date": row.join_date.strftime("%y-%m-%d"),
                                    "is_blocked": row.is_blocked, "verify": row.verify}
                        data_list.append(row_dict)
                    return data_list
                else:
                    return None
            else:
                app_log.info("|student_function - search_student| -> search without email")
                result_set1 = query.filter(models.User.trainer_id == search).all()
                result_set2 = query.filter(models.User.user_name == search).all()
                result_set3 = query.filter(models.User.f_name == search).all()
                result_set4 = query.filter(models.User.l_name == search).all()
                result_set = result_set1 + result_set2 + result_set3 + result_set4
                """
                if result_set is None:
                    result_set_like1_trainer_id = query.filter(models.User.trainer_id.like(f"%{search}%")).all()
                    result_set_like2_trainer_id = query.filter(models.User.trainer_id.like(f"%{search}")).all()
                    result_set_like3_trainer_id = query.filter(models.User.trainer_id.like(f"{search}%")).all()
                    result_set = result_set_like3_trainer_id + result_set_like2_trainer_id + result_set_like1_trainer_id
                else:
                    result_set_like1 = query.filter(models.User.user_name.like(f"{search}%")).all()
                    result_set_like2 = query.filter(models.User.user_name.like(f"%{search}%")).all()
                    result_set = result_set_like1 + result_set_like2
                """
                app_log.info(
                    "|student_function - search_student| -> search by string trainer_id/ user_name/ f_name/ l_name")
                if len(result_set) > 0:
                    for row in result_set:
                        row_dict = {"id": row.id, "trainer_id": row.trainer_id, "f_name": row.f_name,
                                    "l_name": row.l_name,
                                    "user_name": row.user_name,
                                    "email": row.email, "mobile": row.mobile,
                                    "join_date": row.join_date.strftime("%y-%m-%d"),
                                    "is_blocked": row.is_blocked, "verify": row.verify}
                        data_list.append(row_dict)
                    return data_list
                else:
                    return None
    except Exception as e:
        err_log.error(f"|student_function - search_student| -> {e}")
        return None


# Retrieve data in requested student
def get_requested_student(db: Session):
    try:
        result_set = db.query(models.User).filter(models.User.verify == False).all()
        app_log.info("|student_function - get_requested_student| -> get data from requested student detail")
        data_list = []
        if not (result_set is None):
            for row in result_set:
                row_dict = {"id": row.id, "trainer_id": row.trainer_id, "f_name": row.f_name,
                            "l_name": row.l_name,
                            "user_name": row.user_name,
                            "email": row.email, "mobile": row.mobile,
                            "join_date": row.join_date.strftime("%y-%m-%d"),
                            "is_blocked": row.is_blocked, "verify": row.verify}
                data_list.append(row_dict)
            return data_list
        else:
            return None
    except Exception as e:
        err_log.error(f"|student_function - get_requested_student| -> {e}")
        return None


# Approve student  -> update trainer_id and verify = True
def approve_student(db: Session, id: int, trainer_id: str) -> bool:
    try:
        query = update(models.User).where(models.User.id == id).values(trainer_id=trainer_id, verify=True)
        db.execute(query)
        db.commit()
        app_log.info("|student_function - approve_student| -> approve the student/ update database successfully")
        return True
    except Exception as e:
        err_log.error(f"|student_function - approve_student| -> {e}")
        return False


# Retrieve student detail
def get_student_data(db: Session, id: int):
    try:
        data_row = db.query(models.User).filter(models.User.id == id).first()
        row_dict = {"id": data_row.id, "trainer_id": data_row.trainer_id, "f_name": data_row.f_name,
                    "l_name": data_row.l_name,
                    "user_name": data_row.user_name,
                    "email": data_row.email, "mobile": data_row.mobile}
        app_log.info("|student_function - get_student_data| -> retrieve successfully")
        return row_dict
    except Exception as e:
        err_log.error(f"|student_function - get_student_data| -> {e}")
        return None


# Reject student request
def reject_student_request(db: Session, id: int) -> bool:
    try:
        query = delete(models.User).where(models.User.id == id)
        db.execute(query)
        db.commit()
        app_log.info("|student_function - reject_student_request| -> delete successfully")
        return True
    except Exception as e:
        err_log.error(f"|student_function reject_student_request| -> {e}")
        return False
