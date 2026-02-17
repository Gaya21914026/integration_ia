from sqlalchemy import  Column, String,Integer,Enum
from app.db.database import Base
import enum 

class UserRole(str,enum.Enum):
    user = "user"
    admin = "admin"


class Users(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String(50))
    password = Column(String(255))
    role = Column(Enum(UserRole), default=UserRole.user, nullable=False)
