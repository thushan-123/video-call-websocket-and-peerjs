from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from Databases.redis_connection import redis_otp_client
from Functions.function import get_db, password_hash, get_OTP
from Loggers.log import app_log, err_log
from pydantic import BaseModel
from .functionAdmin import authenticate_admin, get_admin_data, verify_admin_reset_pwd, admin_password_change, \
    create_new_admin
from Authorized.auth import create_access_token, verify_token
from Mails.mail import Mail
from Mails.html import html_content_OTP
from .AdminLoged import admin_topic
from .AdminLoged.Student import student

router = APIRouter()


class AdminCreate(BaseModel):
    admin_name: str
    admin_email: str
    password: str


# Create schema -> admin login
class AdminLogin(BaseModel):
    username: str
    password: str


# Create schema -> forget password
class ForgotPassword(BaseModel):
    username: str
    email: str


# Create schema -> Otp
class Otp(BaseModel):
    email: str
    otp_code: int


# Create schema -> change admin password
class ChangePassword(BaseModel):
    password: str


@router.post("/adminLogin")
async def admin_login(admin: AdminLogin, db: Session = Depends(get_db)):
    try:
        password = password_hash(admin.password)
        bool_value = authenticate_admin(db, admin.username, password)
        if bool_value:
            dataset = get_admin_data(db, username=admin.username)
            if not (dataset is None):
                token = create_access_token(dataset, admin=True)
                app_log.info("/admin/adminLogin -> send response  status: success")
                return JSONResponse(status_code=200, content={"status": "success", "token": token})
        else:
            app_log.info("/admin/adminLogin - send response -> status: False (username|password incorrect)")
            return JSONResponse(status_code=401, content={"status": False, "detail": "username or password incorrect"})
    except Exception as e:
        err_log.error(f"/admin/adminLogin -> {e}")
        return JSONResponse(status_code=400, content={"status": False, "detail": "Bad request"})


# redis otp save -> { "test1@mail.com": 1234, "test2@gmail.com": 1234, .... }
@router.post("/forgetPassword")
async def admin_change_password(admin: ForgotPassword, db: Session = Depends(get_db)):
    try:
        dataset = verify_admin_reset_pwd(db, admin.username, admin.email)  # User verify -> username, email
        app_log.info("/admin/forgetPassword - check valued admin")
        if dataset:  # dataset is boolean value
            gen_otp = get_OTP()  # Generate new OTP
            mail = admin.email
            redis_otp_client.set(mail, gen_otp, ex=120)  # redis -> set OTP with 60s expiration
            mail = Mail(admin.email, "One Time Password", html_content_OTP(gen_otp))
            bool_value = mail.send()
            if bool_value:
                app_log.info(f"/admin/forgetPassword -> Email Send Success - receiver: {admin.email}")
                return JSONResponse(status_code=200, content={"status": True, "detail": "email send successfully"})
            else:
                err_log.error(f"/admin/forgetPassword SMTP server error")
                return JSONResponse(status_code=500, content={"status": False, "detail": "email not send"})
        else:
            return JSONResponse(status_code=401, content={"status": False, "detail": "username or email incorrect"})
    except Exception as e:
        err_log.error(f"/admin/forgetPassword -> {e}")
        return JSONResponse(status_code=400, content={"status": False, "detail": "Bad request"})


@router.post("/otp")
async def verify_otp(otp_data: Otp, db: Session = Depends(get_db)):
    try:
        value = redis_otp_client.get(otp_data.email)
        if int(value) == otp_data.otp_code:
            dataset = get_admin_data(db, email_=otp_data.email)
            print(dataset)
            temp_token = create_access_token(dataset, admin=True)
            redis_otp_client.delete(otp_data.email)
            app_log.info("/admin/otp -> OTP is equal | temp_token send to the user")
            return JSONResponse(status_code=200, content={"status": True, "temp_token": temp_token,
                                                          "message": "temp_token use case -> new password and temp_token send API endpoint"})
        else:
            app_log.info("/admin/otp -> OTP not equal ")
            return JSONResponse(status_code=401, content={"status": False, "detail": "otp error"})
    except Exception as e:
        err_log.error(f"/admin/otp -> {e}")
        return JSONResponse(status_code=400, content={"status": False, "detail": "Bad request"})


oauth2_schme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/addAdmin")
async def creating_admin(request: AdminCreate, token: str = Depends(oauth2_schme), db: Session = Depends(get_db)):
    try:
        data_set = verify_token(token, admin=True)
        if not (data_set is None):
            result = create_new_admin(db, request.admin_name, request.admin_email, request.password)
            app_log.info(f"/admin/addAdmin -> create new admin {request.admin_name}")
            if result:
                return JSONResponse(status_code=200, content={"status": True, "detail": "admin create successfully"})
            else:
                return JSONResponse(status_code=400, content={"status": False, "details": "Bad request"})
        else:
            app_log.warning("/admin/addAdmin ->unauthorized access")
            return JSONResponse(status_code=401, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"/admin/addAdmin -> {e}")
        return JSONResponse(status_code=400, content={"status": False, "detail": "Bad request"})


@router.put("/changePassword")
async def admin_update_password(request: ChangePassword, token: str = Depends(oauth2_schme),
                                db: Session = Depends(get_db)):
    try:
        deta_set = verify_token(token, admin=True)
        app_log.info("/admin/changePassword -> OTP is equal | verify the token")
        if not (deta_set is None):
            response_result = admin_password_change(db, deta_set["admin_name"], deta_set["admin_email"],
                                                    request.password)
            app_log.info("/admin/changePassword -> update to the admin password")
            if response_result:
                return JSONResponse(status_code=200, content={"status": True, "detail": "password update successfully"})
            else:
                return JSONResponse(status_code=500, content={"status": False, "detail": "database error"})
        else:
            app_log.warning("/admin/logged/student/addStudent -> unauthorized access")
            return JSONResponse(status_code=401, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"/admin/changePassword -> {e}")
        return JSONResponse(status_code=400, content={"status": False, "detail": "Bad request"})


@router.get("/verifyToken")
async def verify_admin_token(token: str = Depends(oauth2_schme)):
    try:
        data_set = verify_token(token,admin=True)
        app_log.info("/admin/verifyToken -> get dataset verified token")
        if not (data_set is None):
            return JSONResponse(status_code=200, content={"status": True, "detail": "token is verified"})
        else:
            app_log.warning("/admin/logged/student/addStudent -> unauthorized access")
            return JSONResponse(status_code=401, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"/admin/verifyToken -> {e}")
        return JSONResponse(status_code=400, content={"status": False, "detail": "Bad request"})


router.include_router(admin_topic.router, prefix="/logged")
router.include_router(student.router, prefix="/logged/manageStudent")
