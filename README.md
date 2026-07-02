# 📋 Task Management System

A full-stack **Task Management System** built using **React.js** and **FastAPI** with **JWT Authentication**. This application helps users manage tasks efficiently with secure authentication, task tracking, search, filtering, comments, file uploads, and password reset functionality.

---

# 🚀 Live Demo

### 🌐 Frontend
https://task-management-frontend-git-main-tigers6.vercel.app

### ⚙️ Backend API
https://task-mangement-system-nrf1.onrender.com

---

# ✨ Features

- 🔐 User Registration
- 🔑 Secure Login using JWT Authentication
- 📋 Create New Tasks
- ✏️ Edit Existing Tasks
- 🗑 Delete Tasks
- 🔍 Search Tasks
- 🎯 Filter Tasks by Status
- 📊 Sort Tasks by Due Date
- 📈 Dashboard Statistics
- ⚠️ Overdue Task Highlight
- 💬 Task Comments
- 📁 File Upload
- 📤 Export Tasks to CSV
- 🔒 Forgot Password
- 🔄 Secure Password Reset using Token
- ☁️ Frontend Deployed on Vercel
- ☁️ Backend Deployed on Render

---

# 🛠 Tech Stack

## Frontend

- React.js
- React Router DOM
- Axios
- CSS

## Backend

- FastAPI
- SQLAlchemy
- SQLite
- JWT Authentication
- Passlib (Password Hashing)
- Pydantic
- Uvicorn

---

# 📂 Project Structure

```text
TaskManagementSystem
│
├── Frontend (React)
│
├── Backend (FastAPI)
│
├── Database (SQLite)
│
└── Deployment
    ├── Vercel (Frontend)
    └── Render (Backend)
```

---

# 🔐 Authentication

- JWT Token Authentication
- Password Hashing
- Protected Routes
- Secure Password Reset

---

# 📊 Dashboard

The dashboard provides:

- Total Tasks
- Completed Tasks
- Pending Tasks
- High Priority Tasks
- Overdue Tasks

---

# 📸 Screenshots

Screenshots can be added later.

Suggested screenshots:

- Login Page
- Register Page
- Dashboard
- Add Task
- Edit Task
- Forgot Password
- Reset Password

---

# ⚙️ Installation

## Backend

```bash
pip install -r requirements.txt

uvicorn app.main:app --reload
```

## Frontend

```bash
npm install

npm run dev
```

---

# 📬 API Endpoints

| Method | Endpoint |
|---------|----------|
| POST | /register |
| POST | /login |
| GET | /tasks |
| POST | /tasks |
| PUT | /tasks/{id} |
| DELETE | /tasks/{id} |
| POST | /forgot-password |
| POST | /reset-password |

---

# 👨‍💻 Author

**Rohith Kumar**

GitHub:
https://github.com/kumarrohith7888-creator

---

# 📄 License

This project is created for educational purposes.

---

⭐ If you like this project, please give it a Star.