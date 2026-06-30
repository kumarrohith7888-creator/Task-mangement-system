from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str



class TaskCreate(BaseModel):
    title: str
    description: str
    status: str
    category: str
    priority: str
    due_date: date
    assigned_to: Optional[int] = None
    
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    status: str
    category: str
    priority: str
    due_date: date
    assigned_to: Optional[int]

    class Config:
        from_attributes = True

class TaskUpdate(BaseModel):
    title: str
    description: str
    status: str
    category: str
    priority: str
    due_date: date
    assigned_to: Optional[int] = None

class CommentCreate(BaseModel):
    text: str


class CommentResponse(BaseModel):
    id: int
    text: str
    task_id: int
    user_id: int

    class Config:
        from_attributes = True
class ForgotPasswordRequest(BaseModel):
    email: EmailStr