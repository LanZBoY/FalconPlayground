from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Table, Column
from sqlalchemy import Integer, String, Enum, ForeignKey
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


post_tag_relation_table = Table(
    "post_tag_relation",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("post.id"), primary_key = True),
    Column("tag_id", Integer, ForeignKey("tag.id"), primary_key = True)
)    

class PostModel(Base):

    __tablename__ = "post"

    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)

    author = relationship("UserModel", back_populates = "posts")
    tags = relationship("TagModel", secondary = post_tag_relation_table)



class TagModel(Base):

    __tablename__ = "tag"
    id = Column(Integer, primary_key = True)
    name = Column(String, nullable = False)