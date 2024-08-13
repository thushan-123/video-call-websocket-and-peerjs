from pydantic import BaseModel


# Create schema -> student login
class StudentLogin(BaseModel):
    username: str
    password: str


# Create schema -> register student
class RegisterStudent(BaseModel):
    f_name: str
    l_name: str
    email: str
    mobile: int


# Create schema -> reset password
class ResetPassword(BaseModel):
    username: str
    email: str


# Create schema -> get OTP
class GetOtp(BaseModel):
    email: str
    otp_code: int


# Create schema -> change password
class ChangePassword(BaseModel):
    password: str
