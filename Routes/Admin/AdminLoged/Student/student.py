from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from fastapi.responses import JSONResponse
from Functions.function import get_db, get_gen_password, generate_unique_username
from Loggers.log import err_log, app_log
from Authorized.auth import verify_token
from Mails.mail import Mail
from Mails.html import html_content_username_password, html_content_approve_mail
from .student_schema import AddStudent, UpdateStudent, BlockStudent, DeleteStudent, SearchStudent, ApproveStudent, \
    RejectStudent
from .student_function import add_student, update_student, block_student, delete_student, get_student_detail, \
    search_student, get_requested_student, approve_student, get_student_data, reject_student_request

router = APIRouter()

oauth2_schme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("/addStudent")
async def adding_student(request: AddStudent, token: str = Depends(oauth2_schme), db: Session = Depends(get_db)):
    try:
        data_set = verify_token(token,admin=True)
        if not (data_set is None):
            username = generate_unique_username(request.f_name)
            password = get_gen_password()
            get_result = add_student(db, request.trainer_id, request.f_name, request.l_name, username, request.email,
                                     request.mobile, password)
            if get_result:
                mail_ = Mail(request.email, "Exdeme Login Details",
                             html_content_username_password(request.f_name, request.l_name, username, password))
                mail_.send()
                app_log.info("/admin/logged/student/addStudent -> email send and student data add successfully")
                return JSONResponse(status_code=200,
                                    content={"status": True, "detail": "data added and email send to student"})
            else:
                app_log.info("/admin/logged/student/addStudent -> data adding is fail")
                return JSONResponse(status_code=400, content={"status": False, "detail": "Bad request"})
        else:
            app_log.warning("/admin/logged/student/addStudent -> unauthorized access")
            return JSONResponse(status_code=401, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"/admin/logged/student/addStudent -> {e}")
        return JSONResponse(status_code=400, content={"status": False, "detail": "Bad request"})


@router.put("/updateStudent")
async def updating_student(request: UpdateStudent, token: str = Depends(oauth2_schme), db: Session = Depends(get_db)):
    try:
        data_set = verify_token(token,admin=True)
        if not (data_set is None):
            get_result = update_student(db, request.id, request.f_name, request.l_name, request.email, request.mobile)
            if get_result:
                app_log.info("/admin/logged/student/updateStudent -> update successfully")
                return JSONResponse(status_code=200, content={"status": True, "detail": "update successfully"})
            else:
                return JSONResponse(status_code=400,
                                    content={"status": False, "detail": "email or mobile already taken"})
        else:
            app_log.warning("/admin/logged/student/updateStudent -> unauthorized access")
            return JSONResponse(status_code=401, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"/admin/logged/student/updateStudent -> {e}")
        return JSONResponse(status_code=400, content={"status": False, "detail": "Bad request"})


@router.put("/blockStudent")
async def blocking_student(request: BlockStudent, token: str = Depends(oauth2_schme), db: Session = Depends(get_db)):
    try:
        data_set = verify_token(token,admin=True)
        if not (data_set is None):
            if request.is_blocked:
                block_student(db, request.id, blocked=True)
                app_log.info("/admin/logged/student/blockStudent -> successfully blocked")
                return JSONResponse(status_code=200, content={"status": True, "detail": "successfully blocked"})
            else:
                block_student(db, request.id, blocked=False)
                app_log.info("/admin/logged/student/blockStudent -> successfully unblocked")
                return JSONResponse(status_code=200, content={"status": True, "detail": "successfully unblocked"})
        else:
            app_log.warning("/admin/logged/student/updateStudent -> unauthorized access")
            return JSONResponse(status_code=401, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"/admin/logged/student/updateStudent -> {e}")
        return JSONResponse(status_code=400, content={"status": False, "detail": "Bad request"})


@router.delete("/deleteStudent")
async def deleting_student(request: DeleteStudent, token: str = Depends(oauth2_schme), db: Session = Depends(get_db)):
    try:
        data_set = verify_token(token,admin=True)
        if not (data_set is None):
            get_result = delete_student(db, request.id)
            app_log.info("/admin/logged/student/deleteStudent -> delete student")
            if get_result:
                return JSONResponse(status_code=200, content={"status": True, "detail": "delete successfully"})
            else:
                return JSONResponse(status_code=400, content={"status": False, "detail": "Bad request"})
        else:
            app_log.warning("/admin/logged/student/updateStudent -> unauthorized access")
            return JSONResponse(status_code=401, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"/admin/logged/student/deleteStudent -> {e}")
        return JSONResponse(status_code=400, content={"status": False, "detail": "Bad request"})


@router.get("/getAllVerifyStudent")
async def retrieve_all_student(token: str = Depends(oauth2_schme), db: Session = Depends(get_db)):
    try:
        data_set = verify_token(token,admin=True)
        if not (data_set is None):
            data_list = get_student_detail(db)
            app_log.info("/admin/logged/student/getAllStudent -> get all student details")
            if not (data_list is None):
                return JSONResponse(status_code=200, content={"status": True, "data": data_list})
            else:
                return JSONResponse(status_code=200,
                                    content={"status": True, "data": {}, "message": "no student details"})
        else:
            app_log.warning("/admin/logged/student/getAllStudent -> unauthorized access")
            return JSONResponse(status_code=401, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"/admin/logged/student/getAllStudent -> {e}")
        return JSONResponse(status_code=400, content={"status": False, "detail": "Bad request"})


@router.post("/searchVerifyStudent")
async def searching_student(request: SearchStudent, token: str = Depends(oauth2_schme), db: Session = Depends(get_db)):
    try:
        data_set = verify_token(token,admin=True)
        if not (data_set is None):
            data_list = search_student(db, request.search)
            app_log.info("/admin/logged/student/searchStudent -> get search result in students")
            if not (data_list is None):
                return JSONResponse(status_code=200, content={"status": True, "data": data_list})
            else:
                return JSONResponse(status_code=200,
                                    content={"status": True, "data": {}, "message": "result is not found"})
        else:
            app_log.warning("/admin/logged/student/getAllStudent -> unauthorized access")
            return JSONResponse(status_code=401, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"/admin/logged/student/searchStudent -> {e}")
        return JSONResponse(status_code=400, content={"status": False, "detail": "Bad request"})


@router.get("/request/requestedStudent")
async def get_requested_student_detail(token: str = Depends(oauth2_schme), db: Session = Depends(get_db)):
    try:
        data_set = verify_token(token,admin=True)
        if not (data_set is None):
            data_list = get_requested_student(db)
            app_log.info("/admin/logged/student/request/requestedStudent -> retrieve requested student detail")
            if not (data_list is None):
                return JSONResponse(status_code=200, content={"status": True, "data": data_list})
            else:
                return JSONResponse(status_code=200,
                                    content={"status": True, "data": {}, "message": "no requested student"})
        else:
            app_log.warning("/admin/logged/student/getAllStudent -> unauthorized access")
            return JSONResponse(status_code=401, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"/admin/logged/student/request/requestedStudent -> {e}")
        return JSONResponse(status_code=400, content={"status": False, "detail": "Bad request"})


@router.put("/request/approveStudent")
async def approving_student(request: ApproveStudent, token: str = Depends(oauth2_schme), db: Session = Depends(get_db)):
    try:
        data_set = verify_token(token,admin=True)
        if not (data_set is None):
            result = approve_student(db, request.id, request.trainer_id)
            if result:
                app_log.info("/admin/logged/student/approveStudent -> account approved")
                data = get_student_data(db, request.id)
                if not (data is None):
                    mail_ = Mail(data["email"], "Account Approved",
                                 html_content_approve_mail(data["f_name"], data["l_name"]))
                    mail_.send()
                    return JSONResponse(status_code=200, content={"status": True, "detail": "approved success"})
            else:
                app_log.warning("/admin/logged/student/approveStudent -> Bad request")
                return JSONResponse(status_code=400, content={"status": False, "detail": "approved fail"})
        else:
            app_log.warning("/admin/logged/student/request/approveStudent -> unauthorized access")
            return JSONResponse(status_code=401, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"/admin/logged/student/request/requestedStudent -> {e}")
        return JSONResponse(status_code=400, content={"status": False, "detail": "Bad request"})


@router.delete("/request/rejectStudent")
async def rejecting_student(request: RejectStudent, token: str = Depends(oauth2_schme), db: Session = Depends(get_db)):
    try:
        data_set = verify_token(token,admin=True)
        if not (data_set is None):
            result = reject_student_request(db, request.id)
            app_log.info("/admin/logged/student/request/rejectStudent -> student is rejected")
            if result:
                return JSONResponse(status_code=200,
                                    content={"status": True, "detail": "account rejected successfully"})
            else:
                return JSONResponse(status_code=400, content={"status": False, "detail": "rejected fail"})
        else:
            app_log.warning("/admin/logged/student/request/rejectStudent -> unauthorized access")
            return JSONResponse(status_code=401, content={"status": False, "detail": "unauthorized access"})
    except Exception as e:
        err_log.error(f"/admin/logged/student/request/rejectStudent -> {e}")
        return JSONResponse(status_code=400, content={"status": False, "detail": "Bad request"})
