from pydantic import BaseModel
from datetime import date
from typing import Optional, List
from datetime import date as dt_date


# ✅ Base schema with shared fields
class TimesheetBase(BaseModel):
    date: date
    hours_worked: float
    overtime_hours: Optional[float] = 0.0
    notes: Optional[str] = None
    attendance_id: int
    employee_id: int

# ✅ For creation
class TimesheetCreate(TimesheetBase):
    class Config:
        extra = "forbid"

# ✅ For update
class TimesheetUpdate(BaseModel):
    date: Optional[dt_date] = None
    hours_worked: Optional[float] = None
    overtime_hours: Optional[float] = None
    notes: Optional[str] = None
    attendance_id: Optional[int] = None
    employee_id: Optional[int] = None

    class Config:
        extra = "forbid"

# ✅ For response
class Timesheet(TimesheetBase):
    id: int

    class Config:
        from_attributes = True  # Same as orm_mode = True in Pydantic v1

# ✅ For paginated response
class PaginatedTimesheets(BaseModel):
    count: int
    data: List[Timesheet]

# ✅ For API response
class TimesheetListResponse(BaseModel):
    status: str
    result: PaginatedTimesheets
