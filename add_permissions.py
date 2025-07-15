from sqlalchemy.orm import Session
from app.database import SessionLocal  # assuming SessionLocal returns a DB session
from app.models.permission import Permission

permissions = [
    {"name": "Create Role", "code": "create_role", "module_name": "Role", "description": "User can create role"},
    {"name": "Read Role", "code": "read_role", "module_name": "Role", "description": "User can read role"},
    {"name": "Update Role", "code": "update_role", "module_name": "Role", "description": "User can update role"},
    {"name": "Delete Role", "code": "delete_role", "module_name": "Role", "description": "User can delete role"},
    
    {"name": "Create Department", "code": "create_department", "module_name": "Department", "description": "User can create Department"},
    {"name": "Read Department", "code": "read_department", "module_name": "Department", "description": "User can read Department"},
    {"name": "Update Department", "code": "update_department", "module_name": "Department", "description": "User can update Department"},
    {"name": "Delete Department", "code": "delete_department", "module_name": "Department", "description": "User can delete Department"},

    {"name": "Create Employee", "code": "create_employee", "module_name": "Employee", "description": "User can create Employee"},
    {"name": "Read Employee", "code": "read_employee", "module_name": "Employee", "description": "User can read Employee"},
    {"name": "Update Employee", "code": "update_employee", "module_name": "Employee", "description": "User can update Employee"},
    {"name": "Delete Employee", "code": "delete_employee", "module_name": "Employee", "description": "User can delete Employee"},

    {"name": "Create Rank", "code": "create_rank", "module_name": "Rank", "description": "User can create Rank"},
    {"name": "Read Rank", "code": "read_rank", "module_name": "Rank", "description": "User can read Rank"},
    {"name": "Update Rank", "code": "update_rank", "module_name": "Rank", "description": "User can update Rank"},
    {"name": "Delete Rank", "code": "delete_rank", "module_name": "Rank", "description": "User can delete Rank"},

    {"name": "Create Leave", "code": "create_leave", "module_name": "Leave", "description": "User can create Leave"},
    {"name": "Read Leave", "code": "read_leave", "module_name": "Leave", "description": "User can read Leave"},
    {"name": "Update Leave", "code": "update_leave", "module_name": "Leave", "description": "User can update Leave"},
    {"name": "Delete Leave", "code": "delete_leave", "module_name": "Leave", "description": "User can delete Leave"},

    {"name": "Create Notification", "code": "create_notification", "module_name": "Notification", "description": "User can create Notification"},
    {"name": "Read Notification", "code": "read_notification", "module_name": "Notification", "description": "User can read Notification"},
    {"name": "Update Notification", "code": "update_notification", "module_name": "Notification", "description": "User can update Notification"},
    {"name": "Delete Notification", "code": "delete_notification", "module_name": "Notification", "description": "User can delete Notification"},

    {"name": "Create Employee Salary", "code": "create_employee_salary", "module_name": "Employee Salary", "description": "User can create Employee Salary"},
    {"name": "Read Employee Salary", "code": "read_employee_salary", "module_name": "Employee Salary", "description": "User can read Employee Salary"},
    {"name": "Update Employee Salary", "code": "update_employee_salary", "module_name": "Employee Salary", "description": "User can update Employee Salary"},
    {"name": "Delete Employee Salary", "code": "delete_employee_salary", "module_name": "Employee Salary", "description": "User can delete Employee Salary"},

    {"name": "Create Salary Structure", "code": "create_salary_structure", "module_name": "Salary Structure", "description": "User can create Salary Structure"},
    {"name": "Read Salary Structure", "code": "read_salary_structure", "module_name": "Salary Structure", "description": "User can read Salary Structure"},
    {"name": "Update Salary Structure", "code": "update_salary_structure", "module_name": "Salary Structure", "description": "User can update Salary Structure"},
    {"name": "Delete Salary Structure", "code": "delete_salary_structure", "module_name": "Salary Structure", "description": "User can delete Salary Structure"},

    {"name": "Create Payslip", "code": "create_payslip", "module_name": "Payslip", "description": "User can create Payslip"},
    {"name": "Read Payslip", "code": "read_payslip", "module_name": "Payslip", "description": "User can read Payslip"},
    {"name": "Update Payslip", "code": "update_payslip", "module_name": "Payslip", "description": "User can update Payslip"},
    {"name": "Delete Payslip", "code": "delete_payslip", "module_name": "Payslip", "description": "User can delete Payslip"},

    {"name": "Create Salary History", "code": "create_salary_history", "module_name": "Salary History", "description": "User can create Salary History"},
    {"name": "Read Salary History", "code": "read_salary_history", "module_name": "Salary History", "description": "User can read Salary History"},
    {"name": "Update Salary History", "code": "update_salary_history", "module_name": "Salary History", "description": "User can update Salary History"},
    {"name": "Delete Salary History", "code": "delete_salary_history", "module_name": "Salary History", "description": "User can delete Salary History"},
]


def add_permissions_to_db(db: Session):
    for perm in permissions:
        existing = db.query(Permission).filter_by(code=perm["code"]).first()
        if not existing:
            new_perm = Permission(**perm)
            db.add(new_perm)
            print(f"✅ Added: {perm['name']}")
        else:
            print(f"⏩ Skipped (already exists): {perm['name']}")
    db.commit()


if __name__ == "__main__":
    print("🚀 Populating permissions...")
    db = SessionLocal()
    try:
        add_permissions_to_db(db)
    finally:
        db.close()
