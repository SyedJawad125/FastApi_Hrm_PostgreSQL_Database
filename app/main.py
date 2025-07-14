from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.models import attendance

from .database import engine, Base
from .routers import employee, department, auth, user, role, permission, rank, attendance, timesheet, leave, notification
from .models import User, Department  # All models, if needed
# from app.routers import employee

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
# app.include_router(employee.router, prefix="/employees", tags=["Employees"])
app.include_router(employee.router)
app.include_router(department.router)
app.include_router(role.router)
app.include_router(permission.router)
app.include_router(rank.router)
app.include_router(attendance.router)
app.include_router(timesheet.router)
app.include_router(leave.router)
app.include_router(notification.router)

@app.get("/")
def root():
    return {"message": "Welcome to HRM API"}

@app.get("/ping")
async def health_check():
    return {"status": "healthy"}

@app.get("/test")
def test():
    return {"status": "working"}