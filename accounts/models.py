from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import Column, Integer, String, DateTime, Enum, ForeignKey
import enum
import uuid
from datetime import datetime

class BaseModel(DeclarativeBase):
    pass

class RolleEnum(enum.Enum):
    user_role = 'user'
    admin_role = 'admin'

class UserModel(BaseModel):
    __tablename__ = 'users'

    id = Column(Integer,primary_key=True, autoincrement=True, unique=True)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String, nullable=False)
    email = Column(String(50))
    role = Column(Enum(RolleEnum), nullable=False, default=RolleEnum.user_role)
    created_at = Column(DateTime, default=datetime.now())

    user_session = relationship("SessionModel", back_populates='user')
    user_notes = relationship("NotesModel", back_populates='user')

    def __str__(self):
        return self.username
    
class NotesModel(BaseModel):
    __tablename__ = 'notes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(30), nullable=False)
    description = Column(String)
    created_at = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)

    user = relationship("UserModel", back_populates='user_notes')

    def __str__(self):
        return self.title
    
class SessionModel(BaseModel):
    __tablename__ = 'session_table'

    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    token = Column(String, nullable=False, default=str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.now())
    user_id = Column(Integer, ForeignKey('users.id'), unique=True)


    user = relationship("UserModel", back_populates='user_session')
