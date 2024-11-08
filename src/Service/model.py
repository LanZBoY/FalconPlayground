from sqlalchemy.orm import declarative_base
from sqlalchemy import Integer, String,Column

Base = declarative_base()

class UserModel(Base):

    __tablename__ = "user"
    
    id = Column(Integer, primary_key = True)

    username = Column(String, nullable = False)
    password = Column(String, nullable = False)
