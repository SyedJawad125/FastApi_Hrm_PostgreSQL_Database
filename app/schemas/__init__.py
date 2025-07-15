# user schemas
from .user import (
    UserBase,
    UserCreate,
    LoginRequest,
    UserUpdate,
    UserOut,
    Token,
    TokenData,
    TokenResponse
)

# employee schemas
from .employee import (
    Employee,
    EmployeeCreate,
    PaginatedEmployees,
    EmployeeListResponse,
    EmployeeUpdate
)

# department schemas
from .department import (
    DepartmentBase,
    DepartmentCreate,
    Department,
    DepartmentUpdate,
    PaginatedDepartments,
    DepartmentListResponse
)
from .rank import (
    RankBase,
    RankCreate,
    Rank,
    RankUpdate,
    PaginatedRanks,
    RankListResponse
)
from .attendance import (
    AttendanceBase,
    AttendanceCreate,
    Attendance,
    AttendanceUpdate,
    PaginatedAttendances,
    AttendanceListResponse
)
from .timesheet import (
    TimesheetBase,
    TimesheetCreate,
    Timesheet,
    TimesheetUpdate,
    PaginatedTimesheets,
    TimesheetListResponse
)

from .leave import (
    LeaveStatus,
    LeaveType,
    LeaveBase,
    LeaveCreate,
    LeaveUpdate,
    LeaveResponse,
    CreateLeaveResponse,
    LeaveList,
    GetAllLeaveListResponse,
    LeaveListResult,
    MyLeaveListResponse
)

from .permission import (
    PermissionBase,
    PermissionCreate,
    PermissionUpdate,
    Permission,
    PaginatedPermissions,
    PermissionListResponse
)
from .role import (
    RoleBase,
    RoleCreate,
    RoleUpdate,
    Role,
    PaginatedRoles,
    RoleListResponse
)

from .notification import (
    NotificationBase,
    NotificationCreate,
    NotificationUpdate,
    Notification,
    NotificationResponse,
    PaginatedNotifications,
    NotificationListResponse
)
from .employee_salary import (
    EmployeeSalaryBase,
    EmployeeSalaryCreate,
    EmployeeSalaryUpdate,
    EmployeeSalaryOut,
    EmployeeSalaryListResponse
)
from .salary_structure import (
    PaymentFrequency,
    SalaryStructureBase,
    SalaryStructureCreate,
    SalaryStructureUpdate,
    SalaryStructureOut,
    SalaryStructureListResponse
) 
from .payslip import (
    PayslipStatus,
    PayslipBase,
    PayslipCreate,
    PayslipUpdate,
    PayslipOut,
    PayslipListResponse
)
from .salary_history import (
    ChangeType,
    SalaryHistoryBase,
    SalaryHistoryCreate,
    SalaryHistoryUpdate,
    SalaryHistoryOut,
    SalaryHistoryListResponse
)
# define what will be exported on `from schemas import *`
__all__ = [
    'UserBase', 'UserCreate', 'LoginRequest', 'UserUpdate', 'UserOut',
    'Token', 'TokenData', 'TokenResponse',
    'Employee', 'EmployeeCreate','PaginatedEmployees','EmployeeListResponse','EmployeeUpdate',
    'DepartmentBase', 'DepartmentCreate', 'Department', 'DepartmentUpdate',
    'PaginatedDepartments', 'DepartmentListResponse',
    'RankBase', 'RankCreate', 'Rank', 'RankUpdate', 'PaginatedRanks', 'RankListResponse',
    'AttendanceBase', 'AttendanceCreate', 'Attendance', 'AttendanceUpdate', 'PaginatedAttendances', 'AttendanceListResponse',
    'TimesheetBase', 'TimesheetCreate', 'Timesheet', 'TimesheetUpdate', 'PaginatedTimesheets', 'TimesheetListResponse',
    'LeaveStatus', 'LeaveType', 'LeaveBase', 'LeaveCreate', 'LeaveUpdate', 'LeaveResponse', 'CreateLeaveResponse',
    'LeaveList', 'GetAllLeaveListResponse',
    'LeaveListResult', 'MyLeaveListResponse',   
    'PermissionBase', 'PermissionCreate' ,'PermissionUpdate','Permission', 'PaginatedPermissions', 'PermissionListResponse',
    'RoleBase', 'RoleCreate', 'RoleUpdate', 'Role', 'PaginatedRoles', 'RoleListResponse',
    'NotificationBase', 'NotificationCreate', 'NotificationUpdate', 'Notification', 'NotificationResponse', 'PaginatedNotifications', 'NotificationListResponse',
    'EmployeeSalaryBase', 'EmployeeSalaryCreate', 'EmployeeSalaryUpdate', 'EmployeeSalaryOut', 'EmployeeSalaryListResponse',
    'PaymentFrequency', 'SalaryStructureBase', 'SalaryStructureCreate', 'SalaryStructureUpdate', 'SalaryStructureOut', 'SalaryStructureListResponse',
    'PayslipStatus', 'PayslipBase', 'PayslipCreate', 'PayslipUpdate', 'PayslipOut', 'PayslipListResponse',
    'ChangeType', 'SalaryHistoryBase', 'SalaryHistoryCreate', 'SalaryHistoryUpdate', 'SalaryHistoryOut', 'SalaryHistoryListResponse'
]

