from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from Mails.mail import Mail
from Mails.html import html_content_change_username
from Authorized.auth import verify_token, create_access_token
from Functions.function import get_db, generate_unique_username
from Loggers.log import err_log, app_log
from .authStudent_function import get_today_topic, update_student
from .authStudent_schema import UpdateStudent

router = APIRouter()

oauth2_schme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/todayTopics")
async def getting_today_topics(token: str = Depends(oauth2_schme), db: Session = Depends(get_db)):
    try:
        data_set = verify_token(token)
        if not (data_set is None):
            data = get_today_topic(db)
            if not (data is None):
                return JSONResponse(status_code=200, content={"status": True, "data": data})
            else:
                return JSONResponse(status_code=400, content={"status": False, "data": "not add today topic"})
        else:
            app_log.warning("/user/logged/todayTopics -> unauthorized access")
            return JSONResponse(status_code=401, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"/user/logged/todayTopics -> {e}")
        return JSONResponse(status_code=400, content={"status": False, "detail": "Bad request"})


@router.put("/updateStudent")
async def update_student_details(request:UpdateStudent, token: str = Depends(oauth2_schme), db: Session = Depends(get_db)):
    global username
    try:
        data_set = verify_token(token)
        if not (data_set is None):
            if request.f_name != data_set["f_name"]:
                username = generate_unique_username(request.f_name)
                result = update_student(db,data_set["id"],request.f_name,request.l_name,request.email,request.mobile,username)
            else:
                result = update_student(db,data_set["id"],request.f_name,request.l_name,request.email,request.mobile)
            if result:
                app_log.info(f"/user/logged/updateStudent -> update success {request.email} ")
                app_log.info("/user/logged/updateStudent -> new username send to email successfully")
                data_dict ={"id": data_set["id"], "f_name": request.f_name, "l_name": request.l_name, "email": request.email, "mobile": request.mobile}
                return JSONResponse(status_code=200, content={"status": True, "detail": "update successfully", "token": create_access_token(data_dict)})
            else:
                app_log.warning(f"/user/logged/updateStudent -> update fail {request.email}")
                return JSONResponse(status_code=400, content={"status": False, "detail": "update fail"})
        else:
            app_log.warning("/user/logged/updateStudent -> unauthorized access")
            return JSONResponse(status_code=401, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"/user/logged/updateStudent -> {e}")
        return JSONResponse(status_code=400, content={"status": False, "detail": "Bad request"})

'''
                    if request.f_name != data_set["f_name"]:
                    mail_ = Mail(request.email,"Your New Username",html_content_change_username(request.f_name,request.l_name,username))
                    mail_.send()
'''







