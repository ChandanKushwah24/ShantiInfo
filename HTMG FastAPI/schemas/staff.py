from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Literal

class StaffBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Full Name", example="Jane Smith")
    email: EmailStr = Field(..., description="Email", example="jane.smith@hotel.com")
    department: Literal["housekeeping", "front_desk", "maintenance"] = Field(..., description="Department", example="housekeeping")
    position: str = Field(..., min_length=1, max_length=50, description="Position", example="Housekeeper")

class StaffCreate(StaffBase):
    pass

class StaffResponse(StaffBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
