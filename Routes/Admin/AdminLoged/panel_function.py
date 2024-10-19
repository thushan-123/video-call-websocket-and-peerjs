from sqlalchemy import update, delete
from Databases import models
from sqlalchemy.orm import Session
from Functions.function import get_sl_DateTime
from Loggers.log import err_log, app_log


# Insert topic data in the database
def add_topics(db: Session, topic_name: str, criteria: str, admin_id: int) -> bool:
    query = models.Topic(topic_name=topic_name, created=get_sl_DateTime(Date_=True), criteria=criteria,
                         admin_id=admin_id)
    try:
        db.add(query)
        db.commit()
        db.refresh(query)
        app_log.info(f"|panel_function - add_topics| -> data add successfully {topic_name}")
        return True
    except Exception as e:
        err_log.error(f"|panel_function - add_topics| -> data adding fail {e}")
        return False


# Retrieve topic data
def get_topic_data(db: Session, select_date=True):
    result = db.query(models.Topic)
    try:
        if select_date:
            now_date = get_sl_DateTime(Date_=True)  # Ensure this returns a datetime object
            result = result.filter(models.Topic.created == now_date).all()
        app_log.info("|panel_function - get_topic_data| -> data retrieve success")
        if not (result is None):
            list_ = []
            for row in result:
                row_dict = {"topic_id": row.topic_id, "topic_name": row.topic_name, "criteria": row.criteria,
                            "created": row.created.strftime("%Y-%m-%d")}
                list_.append(row_dict)
            return list_
        else:
            return None
    except Exception as e:
        err_log.error(f"|panel_function - get_topic_data| -> data retrieve fail {e}")
        return None


# Update topic data
def update_topic_data(db: Session, topic_id: int, topic_name: str, criteria: str):
    query = update(models.Topic).where(models.Topic.topic_id == topic_id).values(topic_name=topic_name,
                                                                                 criteria=criteria)
    try:
        db.execute(query)
        db.commit()
        app_log.info("|panel_function - update_topic_data| -> data update success")
        return True
    except Exception as e:
        err_log.error(f"|panel_function - update_topic_data| -> data update error {e}")
        return False


def delete_topic_data(db: Session, topic_id: int):
    query = delete(models.Topic).where(models.Topic.topic_id == topic_id)
    try:
        db.execute(query)
        db.commit()
        app_log.info("|panel_function - delete_topic_data| -> data is deleted")
        return True
    except Exception as e:
        err_log.error(f"|panel_function - delete_topic_data| -> {e}")

def get_call_logs(date: str):
    try:
        logs_list = []
        with open("logs/daily_conference_logs/"+ str(date)+".log", "r") as file:
            for line in file:
                logs_list.append(line.strip())
        app_log.info(f"|panel_function - get_call_logs| -> file read successfully: Date {date}")
        return logs_list
    except Exception as e:
        err_log.error(f"|panel_function - get_call_logs| -> {e}")
        return None
