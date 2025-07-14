from pydantic import BaseModel
from datetime import date, time
from typing import Optional, List
from datetime import date as dt_date

# ✅ Base schema for common fields
class AttendanceBase(BaseModel):
    date: date
    check_in: Optional[time] = None
    check_out: Optional[time] = None
    is_present: bool = False
    employee_id: int

# ✅ For create
class AttendanceCreate(AttendanceBase):
    class Config:
        extra = "forbid"

# ✅ For read/response
class Attendance(AttendanceBase):
    id: int

    class Config:
        from_attributes = True  # replaces orm_mode in Pydantic v2

# ✅ For paginated response
class PaginatedAttendances(BaseModel):
    count: int
    data: List[Attendance]

# ✅ For final API response
class AttendanceListResponse(BaseModel):
    status: str
    result: PaginatedAttendances

# ✅ For update
class AttendanceUpdate(BaseModel):
    date: Optional[dt_date] = None
    check_in: Optional[time] = None
    check_out: Optional[time] = None
    is_present: Optional[bool] = None
    employee_id: Optional[int] = None

    class Config:
        extra = "forbid"
