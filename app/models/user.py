from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from app.database import Base
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.sql import func
from datetime import datetime
from sqlalchemy.orm import relationship
from app.models.permission import Permission, user_permission

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, index=True, nullable=True)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, server_default='TRUE', nullable=False)
    is_superuser = Column(Boolean, server_default='FALSE', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, default=datetime.utcnow)

    role_id = Column(Integer, ForeignKey("roles.id"))

    # Specify FK to avoid ambiguity
    role = relationship("Role", back_populates="users", foreign_keys=[role_id])

    created_departments = relationship("Department", back_populates="creator")
    created_roles = relationship("Role", back_populates="creator", foreign_keys="Role.created_by_user_id")
    created_permissions = relationship("Permission", back_populates="creator")
    created_ranks = relationship("Rank", back_populates="creator")

    # Add notifications relationship
    notifications = relationship("Notification", back_populates="user", foreign_keys="Notification.user_id")

    permissions = relationship("Permission",secondary=user_permission,back_populates="users")
    
    # Add relationship for created employee salaries
    created_employee_salaries = relationship("EmployeeSalary", back_populates="creator")
    created_salary_structures = relationship("SalaryStructure", back_populates="creator")
    created_salary_histories = relationship("SalaryHistory", back_populates="creator")
    
    # Add relationships for created and approved payslips
    created_payslips = relationship("Payslip", back_populates="creator", foreign_keys="Payslip.created_by_user_id")
    approved_payslips = relationship("Payslip", back_populates="approver", foreign_keys="Payslip.approved_by_user_id")