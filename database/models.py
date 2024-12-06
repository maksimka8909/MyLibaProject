from sqlalchemy import Column, Integer, String, Enum, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
import enum
import datetime

Base = declarative_base()

class RoleEnum(enum.Enum):
    user = "user"
    librarian = "librarian"

class StatusEnum(enum.Enum):
    borrowed = "borrowed"
    returned = "returned"

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    author = Column(String(255))
    genre = Column(String(255))
    year = Column(Integer)
    quantity = Column(Integer, default=0)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    role = Column(Enum(RoleEnum), nullable=False)
    password = Column(String(255), nullable=False)

class BorrowRecord(Base):
    __tablename__ = "borrow_records"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    borrow_date = Column(DateTime, default=datetime.datetime.utcnow)
    return_date = Column(DateTime, nullable=True)
    status = Column(Enum(StatusEnum), default=StatusEnum.borrowed)

    user = relationship("User")
    book = relationship("Book")