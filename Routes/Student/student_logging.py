from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse
from Functions.function import get_db, get_OTP, get_sl_DateTime, password_hash, is_valid_email, \
    generate_unique_username, get_gen_password
from Authorized.auth import verify_token, create_access_token
from Databases.redis_connection import redis_otp_client
from Loggers.log import app_log, err_log
from Mails.mail import Mail
from Mails.html import student_waite_mail, html_content_OTP
from .student_logging_schema import StudentLogin, RegisterStudent, ResetPassword, GetOtp, ChangePassword
from .student_logging_function import check_registered_student, check_email_mobile, insert_student_data, check_student, \
    get_student_data, update_password
from .StudentLogged import authStudent

router = APIRouter()


@router.post("/studentLogin")
async def loging_student(request: StudentLogin, db: Session = Depends(get_db)):
    try:
        data_dict = check_registered_student(db, request.username, password_hash(request.password))
        if not (data_dict is None):
            app_log.info(f"/user/studentLogin -> login success {request.username}")
            access_token = create_access_token(data_dict)
            return JSONResponse(status_code=200, content={"status": "success", "token": access_token})
        else:
            app_log.warning(f"/user/studentLogin -> login fail {request.username} {request.password}")
            return JSONResponse(status_code=400, content={"status": False, "detail": "invalid username or password"})
    except Exception as e:
        err_log.error(f"/user/studentLogin -> {e}")
        return JSONResponse(status_code=400, content={"status": False, "detail": "Bad request"})


@router.post("/registerStudent")
async def registering_student(request: RegisterStudent, db: Session = Depends(get_db)):
    try:
        if is_valid_email(request.email):
            if not check_email_mobile(db, request.email, request.mobile):
                user_name = generate_unique_username(request.f_name)
                password = get_gen_password()
                hash_password = password_hash(password)
                result = insert_student_data(db, request.f_name, request.l_name, user_name, request.email,
                                             request.mobile, hash_password)
                app_log.info("/user/registerStudent -> insert data successfully")
                if result:
                    mail_ = Mail(request.email, "Exdeme Username and Password",
                                 student_waite_mail(request.f_name, request.l_name, user_name, password))
                    mail_.send()
                    app_log.info(f"/user/registerStudent -> email send successfully {request.email}")
                    return JSONResponse(status_code=200,
                                        content={"status": True, "detail": "data insert success, email is send"})
                else:
                    return JSONResponse(status_code=400, content={"status": False, "detail": "data insert fail"})
            else:
                return JSONResponse(status_code=400,
                                    content={"status": False, "detail": "email or mobile already taken"})
        else:
            return JSONResponse(status_code=400, content={"status": False, "detail": "email is invalid"})
    except Exception as e:
        err_log.error(f"/user/registerStudent -> {e}")
        return JSONResponse(status_code=400, content={"status": False, "detail": "Bad request"})


@router.post("/forgetPassword")
async def student_change_password(request: ResetPassword, db: Session = Depends(get_db)):
    try:
        if is_valid_email(request.email):
            if check_student(db, request.username, request.email):
                OTP = get_OTP()
                redis_otp_client.set(request.email, OTP, ex=120)
                mail_ = Mail(request.email, "Edexme One Time Password", html_content_OTP(OTP))
                mail_.send()
                app_log.info("/user/forgetPassword -> send otp to email successfully")
                return JSONResponse(status_code=200, content={"status": True, "detail": "OTP sent to email"})
            else:
                return JSONResponse(status_code=400, content={"status": False, "detail": "invalid username or email"})
        else:
            return JSONResponse(status_code=400, content={"status": False, "detail": "email is invalid"})
    except Exception as e:
        err_log.error(f"/user/forgetPassword -> {e}")
        return JSONResponse(status_code=400, content={"status": False, "detail": "Bad request"})


@router.post("/otp")
async def verify_otp(request: GetOtp, db: Session = Depends(get_db)):
    try:
        value = redis_otp_client.get(request.email)
        if int(value) == request.otp_code:
            redis_otp_client.delete(request.email)
            data_dict = get_student_data(db, request.email)
            app_log.info("/user/otp -> OTP is equal generate token")
            if not (data_dict is None):
                tem_token = create_access_token(data_dict)
                return JSONResponse(status_code=200, content={"status": True, "temp_token": tem_token})
            else:
                return JSONResponse(status_code=400, content={"status": False, "detail": "request error"})
        else:
            return JSONResponse(status_code=400, content={"status": False, "detail": "OTP is invalid"})
    except Exception as e:
        err_log.error(f"/user/otp -> {e}")
        return JSONResponse(status_code=400, content={"status": False, "detail": "Bad request"})


oauth2_schme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/changePassword")
async def changing_password(request: ChangePassword, token: str = Depends(oauth2_schme), db: Session = Depends(get_db)):
    try:
        data_set = verify_token(token)
        if not (data_set is None):
            app_log.info("/user/changePassword -> verified token , go to update password")
            result = update_password(db, data_set["id"], data_set["user_name"], password_hash(request.password))
            if result:
                return JSONResponse(status_code=200, content={"status": True, "detail": "password change successfully"})
            else:
                return JSONResponse(status_code=400, content={"status": False, "detail": "password change fail"})
        else:
            app_log.warning("/user/changePassword -> unauthorized access")
            return JSONResponse(status_code=401, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"/user/changePassword -> {e}")
        return JSONResponse(status_code=400, content={"status": False, "detail": "Bad request"})


@router.get("/verifyStudentToken")
async def user_verify_token(token: str = Depends(oauth2_schme)):
    try:
        result = verify_token(token)
        if not (result is None):
            return JSONResponse(status_code=200, content={"status": True, "data": result})
        else:
            return JSONResponse(status_code=401, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"/user/verifyStudentToken -> {e}")
        return JSONResponse(status_code=400, content={"status": False, "detail": "Bad request"})


router.include_router(authStudent.router, prefix="/logged")
