from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Table, Column
from sqlalchemy import Integer, String, Enum, ForeignKey
from utils.role import UserRole

Base = declarative_base()


class UserModel(Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)

    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    email = Column(String)
    address = Column(String)
    role = Column(Enum(UserRole), nullable=False)

    posts = relationship("PostModel", back_populates="author", cascade="all, delete")


class PostModel(Base):

    __tablename__ = "post"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)

    author = relationship("UserModel", back_populates="posts")
    tags = relationship("TagModel", secondary="post_tag_relation")


class PostTagRelation(Base):

    __tablename__ = "post_tag_relation"

    post_id = Column(Integer, ForeignKey("post.id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tag.id"), primary_key=True)


class TagModel(Base):

    __tablename__ = "tag"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
