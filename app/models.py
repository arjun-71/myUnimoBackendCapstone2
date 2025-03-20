from sqlalchemy import Column, Integer, String
from .database import Base

class LookupData(Base):
    __tablename__ = "lookup_data"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class FileData(Base):
    __tablename__ = "file_data"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, index=True)
    file_path = Column(String)
