from pydantic import BaseModel


# Create schema -> add student
class AddStudent(BaseModel):
    trainer_id: str
    f_name: str
    l_name: str
    email: str
    mobile: int


# Create schema -> update student
class UpdateStudent(BaseModel):
    id: int
    f_name: str
    l_name: str
    email: str
    mobile: int


# Create schema -> blocked student
class BlockStudent(BaseModel):
    id: int
    is_blocked: bool


# Create schema -> delete student
class DeleteStudent(BaseModel):
    id: int


# Create schema -> search student
class SearchStudent(BaseModel):
    search: str


# Create schema -> approve student
class ApproveStudent(BaseModel):
    id: int
    trainer_id: str


# Create schema -> reject student
class RejectStudent(BaseModel):
    id: int



