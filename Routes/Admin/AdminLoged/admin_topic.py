from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from Functions.function import get_db
from Loggers.log import app_log, err_log
from .schema import AddTopics, UpdateTopic, DeleteTopic, DailyCalls
from Authorized.auth import verify_token
from .panel_function import add_topics, get_topic_data, update_topic_data, delete_topic_data, get_call_logs

router = APIRouter()

oauth2_schme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/addTopics")
async def add_topic(request: AddTopics, token: str = Depends(oauth2_schme), db: Session = Depends(get_db)):
    try:
        data_set = verify_token(token,admin=True)
        if not (data_set is None):
            for row in request.data_set:
                result = add_topics(db, row.topic_name, row.criteria, data_set["admin_id"])
                if result:
                    app_log.info("/admin/logged/addTopics -> data_set insert successfully")
                    continue
                else:
                    app_log.info("/admin/logged/addTopics -> data_set insert fail")
                    break
            return JSONResponse(status_code=200, content={"status": True, "detail": "data_set insert successfully"})
        else:
            app_log.warning("/admin/logged/addTopics -> unauthorized access")
            return JSONResponse(status_code=401, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"/admin/logged/addTopics -> {e}")
        return JSONResponse(status_code=400, content={"status": False, "detail": "Bad request"})


@router.get("/todayTopics")
async def get_today_topics(token: str = Depends(oauth2_schme), db: Session = Depends(get_db)):
    try:
        data_set = verify_token(token,admin=True)
        if not (data_set is None):
            data_list = get_topic_data(db, select_date=True)
            app_log.info(f"/admin/logged/addTopics -> data_list is send {data_set['admin_name']}")
            if not (data_list is None):
                return JSONResponse(status_code=200, content={"status": True, "data": data_list})
            else:
                return JSONResponse(status_code=200, content={"status": True, "data": {}, "message": "no today topics"})
        else:
            app_log.warning("/admin/logged/todayTopics -> unauthorized access")
            return JSONResponse(status_code=401, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"/admin/logged/todayTopics -> {e}")
        return JSONResponse(status_code=400, content={"status": False, "detail": "Bad request"})


@router.put("/updateTopic")
async def update_topic(request: UpdateTopic, token: str = Depends(oauth2_schme), db: Session = Depends(get_db)):
    try:
        data_set = verify_token(token,admin=True)
        if not (data_set is None):
            update_result = update_topic_data(db, request.topic_id, request.topic_name, request.criteria)
            if update_result:
                app_log.info(
                    f"/admin/logged/updateTopic -> {request.topic_name} is updated by {data_set['admin_name']}")
                return JSONResponse(status_code=200, content={"status": True, "detail": "update successfully"})
            else:
                app_log.info(f"/admin/logged/updateTopic -> {request.topic_name} is not updated ")
                return JSONResponse(status_code=200, content={"status": False, "detail": "update fail"})
        else:
            app_log.warning("/admin/logged/updateTopic -> unauthorized access")
            return JSONResponse(status_code=401, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"/admin/logged/updateTopic -> {e}")
        return JSONResponse(status_code=400, content={"status": False, "detail": "Bad request"})


@router.delete("/deleteTopic")
async def delete_topic(request: DeleteTopic, token: str = Depends(oauth2_schme), db: Session = Depends(get_db)):
    try:
        data_set = verify_token(token,admin=True)
        if not (data_set is None):
            delete_result = delete_topic_data(db, request.topic_id)
            if delete_result:
                app_log.info(f"/admin/logged/deleteTopic ->  is deleted ")
                return JSONResponse(status_code=200, content={"status": True, "detail": "delete successfully"})
            else:
                app_log.info(f"/admin/logged/deleteTopic -> {request.topic_id} is not deleted ")
                return JSONResponse(status_code=200, content={"status": False, "detail": "delete fail"})
        else:
            app_log.warning("/admin/logged/deleteTopic -> unauthorized access")
            return JSONResponse(status_code=401, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"/admin/logged/deleteTopic -> {e}")
        return JSONResponse(status_code=400, content={"status": False, "detail": "Bad request"})

@router.post("/callLogs")
async def get_daily_call_logs(request: DailyCalls, token: str = Depends(oauth2_schme)):
    try:
        data_set = verify_token(token, admin=True)
        if not (data_set is None):
            result = get_call_logs(request.date)
            app_log.info("/admin/logged/callLogs -> get a data in file")
            if result is not None:
                return JSONResponse(status_code=200, content={"status": True , "data": result})
            else:
                return JSONResponse(status_code=400, content={"status": False, "data": "not found"})
        else:
            app_log.warning("/admin/logged/callLogs -> unauthorized access")
            return JSONResponse(status_code=401, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"/admin/logged/callLogs -> {e}")
        return JSONResponse(status_code=400, content={"status": False, "detail": "Bad request"})

