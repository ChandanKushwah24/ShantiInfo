from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional

class GuestBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Full Name", example="John Doe")
    email: EmailStr = Field(..., description="Email", example="john.doe@example.com")

class GuestCreate(GuestBase):
    pass

class GuestResponse(GuestBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
