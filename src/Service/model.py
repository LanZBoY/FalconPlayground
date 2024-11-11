from sqlalchemy.orm import declarative_base
from sqlalchemy import Integer, String,Column, Enum
from utils.role import UserRole
Base = declarative_base()

class UserModel(Base):

    __tablename__ = "user"
    
    id = Column(Integer, primary_key = True)

    username = Column(String, nullable = False)
    password = Column(String, nullable = False)
    email = Column(String)
    address = Column(String)
    role = Column(Enum(UserRole), nullable = False)
    