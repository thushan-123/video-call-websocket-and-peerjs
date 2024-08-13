from Databases import models
from sqlalchemy import update
from sqlalchemy.orm import Session
from Functions.function import verify_password, password_hash
from Loggers.log import err_log, app_log


# Authenticate the admin
def authenticate_admin(db: Session, username: str, password: str):
    try:
        result = db.query(models.Admin).filter(models.Admin.admin_name == username).first()
        print(result.password)
        app_log.info("|authAdmin -> authenticate_admin| - compare a password [True, False]")
        if result:
            return verify_password(result.password, password)
        else:
            return False
    except Exception as e:
        err_log.error(f"|authAdmin -> authenticate_admin| - {e}")
        return False


# Get a admin data function
def get_admin_data(db: Session, username: str = None, email_: str = None):
    try:
        result = db.query(models.Admin)
        if not (username is None):
            result = result.filter(models.Admin.admin_name == username).first()
        if not (email_ is None):
            result = result.filter(models.Admin.admin_email == email_).first()
        app_log.info("|authAdmin - authenticate_admin| -> get result from admin db using username")
        if result:
            return {"admin_id": result.admin_id, "admin_name": result.admin_name, "admin_email": result.admin_email}
        else:
            return None
    except Exception as e:
        err_log.error(f"|authAdmin -> get_admin_data| - {e}")
        return None


# Verify the admin -> check username,password [admin_name, admin_email]
def verify_admin_reset_pwd(db: Session, username: str, email: str) -> bool:
    try:
        result = db.query(models.Admin)
        result = result.filter(models.Admin.admin_name == username).filter(models.Admin.admin_email == email).first()
        app_log.info("|authAdmin - verify_admin_password| -> get result from admin db using username, email")
        if not (result is None):
            return True
        else:
            return False
    except Exception as e:
        err_log.error(f"|authAdmin - verify_admin_reset_pwd| -> {e}")
        return False


# Verified admin password change
def admin_password_change(db: Session, username: str, email: str, new_password: str) -> bool:
    try:
        query = update(models.Admin).where(models.Admin.admin_name == username,
                                           models.Admin.admin_email == email).values(
            password=password_hash(new_password))
        db.execute(query)
        db.commit()
        app_log.info(f"|authAdmin - admin_password_change| -> {username} update password ")
        return True
    except Exception as e:
        err_log.error(f"|authAdmin - admin_password_change| -> {e}")
        return False


# Create a new admin
def create_new_admin(db: Session, admin_name: str, admin_email: str, password: str):
    try:
        query = models.Admin(admin_name=admin_name, admin_email=admin_email, password=password_hash(password))
        db.add(query)
        db.commit()
        db.refresh(query)
        app_log.info(f"|functionAdmin - create_new_admin| -> create a new admin successfully")
        return True
    except Exception as e:
        err_log.error(f"|functionAdmin - create_new_admin| -> {e}")
        return False
