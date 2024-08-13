from sqlalchemy import Column, Integer, String, Boolean, Date, ForeignKey
from Databases.database import Base


# create a table -> user

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    trainer_id = Column(String(20), unique=True, index=True, default="")
    f_name = Column(String(20), nullable=False)
    l_name = Column(String(20), nullable=False)
    user_name = Column(String(20), unique=True, nullable=False, index=True)
    email = Column(String(60), unique=True, nullable=False, index=True)
    mobile = Column(Integer, unique=True, nullable=False, index=True)
    password = Column(String(100), nullable=False)
    join_date = Column(Date, index=True, nullable=False)
    is_blocked = Column(Boolean, nullable=False, default=False)
    verify = Column(Boolean, nullable=False, default=False)


# create a table -> admin

class Admin(Base):
    __tablename__ = "admin"

    admin_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    admin_name = Column(String(20),unique=True, nullable=False)
    admin_email = Column(String(60), unique=True, nullable=False, index=True)
    password = Column(String(100), nullable=False)


# create a table -> topic  criteria is stored JSON format {criteria:['msg1','msg2']}

class Topic(Base):
    __tablename__ = "topic"

    topic_id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    topic_name = Column(String(50), nullable=False)
    created = Column(Date, nullable=False, index=True)
    criteria = Column(String(100))
    admin_id = Column(Integer, ForeignKey("admin.admin_id"))
