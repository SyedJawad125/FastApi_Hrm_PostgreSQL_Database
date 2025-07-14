from typing import Optional, List
from pydantic import BaseModel

# Shared base schema
class RankBase(BaseModel):
    title: str
    salary_range_min: Optional[float] = None
    salary_range_max: Optional[float] = None
    department_id: Optional[int] = None

# For creating a rank
class RankCreate(RankBase):
    class Config:
        extra = "forbid"

# For updating a rank
class RankUpdate(BaseModel):
    title: Optional[str] = None
    salary_range_min: Optional[float] = None
    salary_range_max: Optional[float] = None
    department_id: Optional[int] = None

    class Config:
        extra = "forbid"

# For reading a rank (e.g., in responses)
class Rank(RankBase):
    id: int
    created_by_user_id: int

    class Config:
        from_attributes = True

# Paginated response schema
class PaginatedRanks(BaseModel):
    count: int
    data: List[Rank]

# Final API response wrapper
class RankListResponse(BaseModel):
    status: str
    result: PaginatedRanks
