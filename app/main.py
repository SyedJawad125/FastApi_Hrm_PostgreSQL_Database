from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Enable SQLAlchemy logging
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)

# Import Base and engine from database (use absolute import)
from app.database import engine, Base

# Import all models explicitly (make sure these use Base from database.py)
from app.models.user import User
from app.models.department import Department
from app.models.role import Role
from app.models.permission import Permission
from app.models.rank import Rank
from app.models.attendance import Attendance
from app.models.timesheet import Timesheet
from app.models.leave import Leave
from app.models.notification import Notification

# Import routers
from app.routers import (
    employee, department, auth, user, 
    role, permission, rank, attendance, 
    timesheet, leave, notification
)

app = FastAPI(
    title="HRM System",
    version="1.0.0",
    description="An API for managing HRM features",
    openapi_tags=[
        {
            "name": "Departments",
            "description": "Operations related to leave creation, approval, and management"
        },
        {
            "name": "Employees",
            "description": "Employee profile management"
        },
        {
            "name": "Users",
            "description": "User login and registration"
        },
        {
            "name": "Ranks",
            "description": "Rank profile management"
        },
        {
            "name": "Roles",
            "description": "Roles profile management"
        },
        {
            "name": "Notifications",
            "description": "User notifications management"
        }
    ]
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(employee.router)
app.include_router(department.router)
app.include_router(role.router)
app.include_router(permission.router)
app.include_router(rank.router)
app.include_router(attendance.router)
app.include_router(timesheet.router)
app.include_router(leave.router)
app.include_router(notification.router)

@app.on_event("startup")
def startup_event():
    print("Creating database tables...")
    print(f"Engine URL: {engine.url}")
    print(f"Tables in metadata: {Base.metadata.tables.keys()}")
    Base.metadata.create_all(bind=engine)
    print("Database tables created.")


@app.get("/")
def root():
    return {"message": "Welcome to HRM API"}

@app.get("/ping")
async def health_check():
    return {"status": "healthy"}

@app.get("/test")
def test():
    return {"status": "working"}
