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
    
        # {"name": "Create Booking", "code": "create_booking", "module_name": "Booking", "description": "User can create Booking"},
    # {"name": "Read Booking", "code": "read_booking", "module_name": "Booking", "description": "User can read Booking"},
    # {"name": "Update Booking", "code": "update_booking", "module_name": "Booking", "description": "User can update Booking"},
    # {"name": "Delete Booking", "code": "delete_booking", "module_name": "Booking", "description": "User can delete Booking"},

    # {"name": "Create Images", "code": "create_images", "module_name": "Images", "description": "User can create Images"},
    # {"name": "Read Images", "code": "read_images", "module_name": "Images", "description": "User can read Images"},
    # {"name": "Update Images", "code": "update_images", "module_name": "Images", "description": "User can update Images"},
    # {"name": "Delete Images", "code": "delete_images", "module_name": "Images", "description": "User can delete Images"},
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
