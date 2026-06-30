from fastapi import APIRouter, Depends
from fastapi import UploadFile, File
import shutil
import os
import secrets
from fastapi import HTTPException
from app import models
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import date
from fastapi import Depends
from app.database import get_db
import csv
from fastapi.responses import FileResponse
from app.models import User,Task,Comment
from app.schemas import UserCreate, UserLogin, TaskCreate, TaskResponse, TaskUpdate, CommentCreate, CommentResponse
from app.utils import hash_password, verify_password
from app.auth import create_access_token, get_current_user
from typing import Optional
from fastapi import Query
router = APIRouter()
password_reset_tokens = {}

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):

    existing_email = db.query(User).filter(
        User.email == user.email
    ).first()

    if existing_email:
        return {
            "message": "Email already registered"
        }

    existing_username = db.query(User).filter(
        User.username == user.username
    ).first()

    if existing_username:
        return {
            "message": "Username already exists"
        }

    hashed_password = hash_password(user.password)

    new_user = User(
        username=user.username,
        email=user.email,
        password=hashed_password,
        role="user"
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "User Registered Successfully"
    }
    
@router.post("/login")
def login( 
          form_data: OAuth2PasswordRequestForm = Depends(),
          db: Session = Depends(get_db)
):

    db_user = db.query(User).filter(
        User.email == form_data.username
    ).first()

    if not db_user:
        return {
            "message": "User not found"
        }

    if not verify_password(
        form_data.password,
        db_user.password
    ):
        return {
            "message": "Invalid password"
        }
    access_token = create_access_token(
        data={"sub": db_user.email,
              "user_id": db_user.id,
              "role": db_user.role
        }
)

    return {
        "access_token": access_token,
        "token_type": "bearer"
}

@router.get("/profile")
def profile(current_user: dict = Depends(get_current_user)):

    return {
        "message": "Welcome",
        "email": current_user["email"],
        "user_id": current_user["user_id"]
    }
    
@router.post("/tasks")
def create_task(task: TaskCreate, 
                db: Session = Depends(get_db),
                current_user: dict = Depends(get_current_user)
            ):

    new_task = Task(
        title=task.title,
        description=task.description,
        status=task.status,
        category=task.category,
        priority=task.priority,
        due_date=task.due_date,
        user_id=current_user["user_id"],
        assigned_to=task.assigned_to
    )
        
    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return {
        "message": "Task Created Successfully"
    }
@router.get("/tasks", response_model=list[TaskResponse])
def get_tasks(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user),
    search: Optional[str] = Query(None),
    status: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    priority: Optional[str] = Query(None),
    sort_by: Optional[str] = Query(None),
    skip: int = Query(0),
    limit: int = Query(10)
):
    
    query = db.query(Task).filter(
        Task.user_id == current_user["user_id"]
    )

    if search:
        query = query.filter(
            Task.title.ilike(f"%{search}%")
        )

    if status:
        query = query.filter(
            Task.status == status
        )
    if category:
        query = query.filter(
            Task.category == category
        )
    if priority:
        query = query.filter(
            Task.priority == priority
        )
    if sort_by == "due_date":
        query = query.order_by(Task.due_date)

    if sort_by == "priority":
        query = query.order_by(Task.priority)

    tasks = query.offset(skip).limit(limit).all()

    return tasks
@router.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    task: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    db_task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user["user_id"]
    ).first()

    if not db_task:
        return {
            "message": "Task not found"
        }

    db_task.title = task.title
    db_task.description = task.description
    db_task.status = task.status
    db_task.category = task.category
    db_task.priority = task.priority
    db_task.due_date = task.due_date
    db_task.assigned_to = task.assigned_to

    db.commit()
    db.refresh(db_task)

    return {
        "message": "Task Updated Successfully"
    }
@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    db_task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user["user_id"]
    ).first()

    if not db_task:
        return {
            "message": "Task not found"
        }

    db.delete(db_task)
    db.commit()

    return {
        "message": "Task Deleted Successfully"
    }
@router.delete("/tasks/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    db_task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user["user_id"]
    ).first()

    if not db_task:
        return {
            "message": "Task not found"
        }

    db.delete(db_task)
    db.commit()

    return {
        "message": "Task Deleted Successfully"
    }
@router.get("/dashboard")
def dashboard(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    total = db.query(Task).filter(
        Task.user_id == current_user["user_id"]
    ).count()

    completed = db.query(Task).filter(
        Task.user_id == current_user["user_id"],
        Task.status == "Completed"
    ).count()

    pending = db.query(Task).filter(
        Task.user_id == current_user["user_id"],
        Task.status == "Pending"
    ).count()
    high_priority = db.query(Task).filter(
    Task.user_id == current_user["user_id"],
    Task.priority == "High"
).count()

    return {
        "total_tasks": total,
        "completed_tasks": completed,
        "pending_tasks": pending,
        "high_priority_tasks": high_priority
    }
@router.get("/admin/users")
def get_all_users(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    if current_user["role"] != "admin":
        return {
            "message": "Access Denied"
        }

    users = db.query(User).all()

    result = []

    for user in users:
        result.append({
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "role": user.role
        })

    return result
@router.post("/tasks/{task_id}/comments")
def add_comment(
    task_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user["user_id"]
    ).first()

    if not task:
        return {"message": "Task not found"}

    new_comment = Comment(
        text=comment.text,
        task_id=task_id,
        user_id=current_user["user_id"]
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return {
        "message": "Comment Added Successfully"
    }
@router.get("/tasks/{task_id}/comments", response_model=list[CommentResponse])
def get_comments(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == current_user["user_id"]
    ).first()

    if not task:
        return []

    comments = db.query(Comment).filter(
        Comment.task_id == task_id
    ).all()

    return comments
@router.get("/tasks/overdue", response_model=list[TaskResponse])
def get_overdue_tasks(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):

    tasks = db.query(Task).filter(
        Task.user_id == current_user["user_id"],
        Task.due_date < date.today(),
        Task.status != "Completed"
    ).all()

    return tasks
@router.get("/tasks/progress")
def task_progress(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    total = db.query(Task).filter(
        Task.user_id == current_user["user_id"]
    ).count()

    completed = db.query(Task).filter(
        Task.user_id == current_user["user_id"],
        Task.status == "Completed"
    ).count()

    percentage = 0

    if total > 0:
        percentage = round((completed / total) * 100, 2)

    return {
        "total_tasks": total,
        "completed_tasks": completed,
        "completion_percentage": percentage
    }
@router.get("/tasks/export")
def export_tasks(
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    tasks = db.query(Task).filter(
        Task.user_id == current_user["user_id"]
    ).all()

    filename = "tasks.csv"

    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        writer.writerow([
            "ID",
            "Title",
            "Description",
            "Status",
            "Category",
            "Priority",
            "Due Date",
            "Assigned To"
        ])

        for task in tasks:
            writer.writerow([
                task.id,
                task.title,
                task.description,
                task.status,
                task.category,
                task.priority,
                task.due_date,
                task.assigned_to
            ])

    return FileResponse(
        path=filename,
        filename="tasks.csv",
        media_type="text/csv"
    )
@router.post("/upload")
def upload_file(file: UploadFile = File(...)):
    os.makedirs("uploads", exist_ok=True)

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "message": "File uploaded successfully",
        "filename": file.filename
    }
    
@router.post("/tasks/{task_id}/comments", response_model=CommentResponse)
def add_comment(
    task_id: int,
    comment: CommentCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    task = db.query(models.Task).filter(models.Task.id == task_id).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    new_comment = models.Comment(
        text=comment.text,
        task_id=task_id,
        user_id=current_user.id
    )

    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)

    return new_comment

from fastapi import Body
from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from dotenv import load_dotenv
import os
from pydantic import BaseModel

class ForgotPasswordRequest(BaseModel):
    email: str

load_dotenv()

conf = ConnectionConfig(
    MAIL_USERNAME=os.getenv("EMAIL_USER"),
    MAIL_PASSWORD=os.getenv("EMAIL_PASSWORD"),
    MAIL_FROM=os.getenv("EMAIL_USER"),
    MAIL_PORT=int(os.getenv("EMAIL_PORT")),
    MAIL_SERVER=os.getenv("EMAIL_HOST"),
    MAIL_STARTTLS=True,
    MAIL_SSL_TLS=False,
    USE_CREDENTIALS=True,
)

@router.post("/forgot-password")
async def forgot_password(
    request: ForgotPasswordRequest,
    db: Session = Depends(get_db)
):
    email = request.email
    user = db.query(models.User).filter(models.User.email == email).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = secrets.token_urlsafe(32)
    password_reset_tokens[token] = user.id

    message = MessageSchema(
        subject="Password Reset",
        recipients=[email],
        body=f"Use this token to reset your password:\n\n{token}",
        subtype="plain",
    )

    fm = FastMail(conf)
    await fm.send_message(message)

    return {"message": "Reset email sent"}

@router.post("/reset-password")
async def reset_password(
    request: models.ResetPasswordRequest,
    db: Session = Depends(get_db)
):
    user_id = password_reset_tokens.get(request.token)

    if not user_id:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    user = db.query(models.User).filter(models.User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.password = hash_password(request.new_password)

    db.commit()

    del password_reset_tokens[request.token]

    return {"message": "Password reset successful"}