from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Integer, String,Column, Enum, ForeignKey
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

    posts = relationship("PostModel", back_populates = "author", cascade = "all, delete")
    

class PostModel(Base):

    __tablename__ = "post"

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)

    author = relationship("UserModel", back_populates = "posts")