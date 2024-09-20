# database pydantic schema set up
from pydantic import BaseModel
from typing import Optional
from datetime import date

class JobApplicationBase(BaseModel):
    company_name: str
    position: str
    date_applied: date
    status: Optional[str] = "Applied"
    notes: Optional[str]

class JobApplicationCreate(JobApplicationBase):
    pass

class JobApplication(JobApplicationBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        # changed from orm_mode in pydantic v2
        from_attributes = True
