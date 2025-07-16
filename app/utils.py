from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime
from app import models
from sqlalchemy.orm import Query
from app import models, schemas 
from fastapi.responses import JSONResponse

 # ✅ Keep this if enums are in the same schemas file


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def paginate_data(data, request):
    try:
        page = int(request.query_params.get("page", 1))
        page_size = int(request.query_params.get("page_size", 20))
        start = (page - 1) * page_size
        end = start + page_size
        return data[start:end], len(data)
    except:
        return data, len(data)
    
from fastapi.responses import JSONResponse
def create_response(data, message, status_code):
    return JSONResponse(
        status_code=status_code,
        content={
            "status": message,
            "result": data
        }
    )
from app import models

def filter_departments(params, query):
    name = params.get("name")
    if name:
        query = query.filter(models.Department.name.ilike(f"%{name}%"))
    # Add more filters as needed
    return query



def filter_employees(params, query):
    name = params.get("name")
    if name:
        query = query.filter(models.Employee.name.ilike(f"%{name}%"))
    # Add more filters as needed
    return query

def filter_ranks(params, query):
    title = params.get("title")
    if title:
        query = query.filter(models.Rank.title.ilike(f"%{title}%"))
    # Add more filters as needed
    return query

def filter_attendances(params, query):
    is_present = params.get("is_present")
    date = params.get("date")
    employee_id = params.get("employee_id")

    # Handle is_present filter
    if is_present is not None:
        is_present = is_present.lower()
        if is_present in ["true", "1"]:
            query = query.filter(models.Attendance.is_present == True)
        elif is_present in ["false", "0"]:
            query = query.filter(models.Attendance.is_present == False)

    # Handle date filter
    if date:
        try:
            # Optional: Validate the date format
            from datetime import datetime
            datetime.strptime(date, "%Y-%m-%d")  # Will raise ValueError if invalid
            query = query.filter(models.Attendance.date == date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    # Handle employee_id filter
    if employee_id:
        try:
            query = query.filter(models.Attendance.employee_id == int(employee_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid employee_id. Must be an integer.")

    return query


def filter_timesheets(params, query):
    date = params.get("date")
    employee_id = params.get("employee_id")
    attendance_id = params.get("attendance_id")

    if date:
        try:
            from datetime import datetime
            datetime.strptime(date, "%Y-%m-%d")
            query = query.filter(models.Timesheet.date == date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    if employee_id:
        try:
            query = query.filter(models.Timesheet.employee_id == int(employee_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="employee_id must be an integer.")

    if attendance_id:
        try:
            query = query.filter(models.Timesheet.attendance_id == int(attendance_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="attendance_id must be an integer.")

    return query
    


def filter_leave(params: dict, query: Query):
    status = params.get("status")
    leave_type = params.get("leave_type")
    employee_id = params.get("employee_id")
    start_date = params.get("start_date")
    end_date = params.get("end_date")

    if status:
        if status not in [s.value for s in schemas.LeaveStatus]:  # ✅ Use schemas.LeaveStatus
            raise HTTPException(status_code=400, detail="Invalid leave status.")
        query = query.filter(models.Leave.status == status)

    if leave_type:
        if leave_type not in [lt.value for lt in schemas.LeaveType]:  # ✅ Use schemas.LeaveType
            raise HTTPException(status_code=400, detail="Invalid leave type.")
        query = query.filter(models.Leave.leave_type == leave_type)

    if employee_id:
        try:
            query = query.filter(models.Leave.employee_id == int(employee_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="employee_id must be an integer.")

    if start_date:
        try:
            datetime.strptime(start_date, "%Y-%m-%d")
            query = query.filter(models.Leave.start_date >= start_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid start_date format. Use YYYY-MM-DD.")

    if end_date:
        try:
            datetime.strptime(end_date, "%Y-%m-%d")
            query = query.filter(models.Leave.end_date <= end_date)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid end_date format. Use YYYY-MM-DD.")

    return query



def filter_employee_salaries(params, query):
    employee_id = params.get("employee_id")
    salary_month = params.get("salary_month")  # Format: YYYY-MM
    payment_status = params.get("payment_status")
    department_id = params.get("department_id")
    rank_id = params.get("rank_id")

    # Filter by employee_id
    if employee_id:
        try:
            query = query.filter(models.EmployeeSalary.employee_id == int(employee_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid employee_id. Must be an integer.")

    # Filter by salary_month (YYYY-MM)
    if salary_month:
        try:
            salary_month_date = datetime.strptime(salary_month, "%Y-%m")
            query = query.filter(models.EmployeeSalary.salary_month == salary_month_date.date())
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid salary_month format. Use YYYY-MM.")

    # Filter by payment_status
    if payment_status:
        allowed_statuses = ["pending", "paid", "cancelled"]
        if payment_status.lower() in allowed_statuses:
            query = query.filter(models.EmployeeSalary.payment_status == payment_status.lower())
        else:
            raise HTTPException(status_code=400, detail=f"Invalid payment_status. Allowed: {allowed_statuses}")

    # Filter by department_id
    if department_id:
        try:
            query = query.filter(models.EmployeeSalary.department_id == int(department_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid department_id. Must be an integer.")

    # Filter by rank_id
    if rank_id:
        try:
            query = query.filter(models.EmployeeSalary.rank_id == int(rank_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid rank_id. Must be an integer.")

    return query



def filter_salary_histories(params, query: Query):
    employee_id = params.get("employee_id")
    department_id = params.get("department_id")
    previous_rank_id = params.get("previous_rank_id")
    new_rank_id = params.get("new_rank_id")
    change_type = params.get("change_type")  # promotion, annual_raise, etc.
    effective_date = params.get("effective_date")  # format: YYYY-MM-DD

    # Filter by employee_id
    if employee_id:
        try:
            query = query.filter(models.SalaryHistory.employee_id == int(employee_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid employee_id. Must be an integer.")

    # Filter by department_id
    if department_id:
        try:
            query = query.filter(models.SalaryHistory.department_id == int(department_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid department_id. Must be an integer.")

    # Filter by previous_rank_id
    if previous_rank_id:
        try:
            query = query.filter(models.SalaryHistory.previous_rank_id == int(previous_rank_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid previous_rank_id. Must be an integer.")

    # Filter by new_rank_id
    if new_rank_id:
        try:
            query = query.filter(models.SalaryHistory.new_rank_id == int(new_rank_id))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid new_rank_id. Must be an integer.")

    # Filter by change_type
    if change_type:
        valid_types = [e.value for e in models.ChangeType]
        if change_type.lower() in valid_types:
            query = query.filter(models.SalaryHistory.change_type == change_type.lower())
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid change_type. Allowed: {valid_types}"
            )

    # Filter by effective_date
    if effective_date:
        try:
            parsed_date = datetime.strptime(effective_date, "%Y-%m-%d").date()
            query = query.filter(models.SalaryHistory.effective_date == parsed_date)
        except ValueError:
            raise HTTPException(
                status_code=400,
                detail="Invalid effective_date format. Use YYYY-MM-DD."
            )

    return query



def filter_permissions(params, query):
    name = params.get("name")
    if name:
        query = query.filter(models.Permission.name.ilike(f"%{name}%"))
    # Add more filters as needed
    return query


def filter_roles(params, query):
    name = params.get("name")
    if name:
        query = query.filter(models.Role.name.ilike(f"%{name}%"))
    # Add more filters as needed
    return query




import os
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()

def send_email_notification(to_email: str, subject: str, message: str):
    sender_email = os.getenv("EMAIL_USER", "default@gmail.com")
    sender_password = os.getenv("EMAIL_PASSWORD", "")
    email_host = os.getenv("EMAIL_HOST", "smtp.gmail.com")
    email_port = int(os.getenv("EMAIL_PORT", 465))

    print(f"Preparing to send email to: {to_email}")
    print(f"SMTP Server: {email_host}:{email_port}, From: {sender_email}")

    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP_SSL(email_host, email_port) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print(f"[SUCCESS] Email sent to {to_email}")
    except Exception as e:
        print("[ERROR] Failed to send email:", str(e))

import os
from datetime import datetime

LOG_FILE_PATH = "app/logs/leave_actions.log"  # You can customize the path

def log_action(message: str):
    print("📄 Writing log:", message)  # TEMP
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
    with open(LOG_FILE_PATH, "a") as log_file:
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {message}\n")


# EMAIL_HOST = "smtp.gmail.com"
# EMAIL_USE_SSL = True
# EMAIL_PORT = 465
# EMAIL_HOST_USER = "syedjawadali92@gmail.com"
# EMAIL_HOST_PASSWORD = "ctpgxfclwyucweni"


# app/utils/redis_client.py

import redis
from redis.exceptions import RedisError
import os

REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

try:
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    redis_client.ping()  # Try connecting to Redis
    print("✅ Redis connected successfully.")
except RedisError as e:
    print("❌ Redis connection failed:", e)
    redis_client = None

from fastapi import HTTPException
from sqlalchemy.orm import Query

def get_object_or_404(query: Query, id: int, name: str = "Object"):
    obj = query.filter_by(id=id).first()
    if not obj:
        raise HTTPException(status_code=404, detail=f"{name} with id {id} not found")
    return obj
