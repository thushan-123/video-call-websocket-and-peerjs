from dns.resolver import query

from Databases import models
from sqlalchemy import update
from sqlalchemy.orm import Session
from Functions.function import get_sl_DateTime
from Loggers.log import err_log, app_log

# Retrieve a today topics in database
def get_today_topic(db: Session):
    try:
        data = db.query(models.Topic).filter(models.Topic.created == get_sl_DateTime(Date_=True)).all()
        app_log.info("|authStudent_function - get_today_topic| -> retrieve data successfully")
        if not (data is None):
            list_ =[]
            for row in data:
                data_dict = {"topic_name": row.topic_name, "criteria": row.criteria}
                list_.append(data_dict)
            return list_
        else:
            return None
    except Exception as e:
        err_log.error(f"|authStudent_function - get_today_topic| -> {e}")
        return None

# Update student detail
def update_student(db: Session,id: int, f_name: str,l_name: str, email: str, mobile: int, user_name: str = None):
    try:
        if user_name is None:
            query1 = update(models.User).where(models.User.id == id).values(f_name=f_name,l_name=l_name,email=email,mobile=mobile)
        else:
            query1 = update(models.User).where(models.User.id == id).values(f_name=f_name,l_name=l_name,user_name=user_name,email=email,mobile=mobile)
        db.execute(query1)
        db.commit()
        app_log.info("|authStudent_function - update_student| -> student data update successfully")
        return True
    except Exception as e:
        err_log.error(f"|authStudent_function - update_student| -> {e}")
        return False