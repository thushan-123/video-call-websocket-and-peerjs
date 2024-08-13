from pydantic import BaseModel

# Create schema -> update student details
class UpdateStudent(BaseModel):
    f_name: str
    l_name: str
    email: str
    mobile: int