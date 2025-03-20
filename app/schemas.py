from pydantic import BaseModel
from typing import Optional

class LookupSchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True

class UserSchema(BaseModel):
    email: str
    password: str

class FileSchema(BaseModel):
    id: int
    file_name: str
    file_path: str

    class Config:
        orm_mode = True
