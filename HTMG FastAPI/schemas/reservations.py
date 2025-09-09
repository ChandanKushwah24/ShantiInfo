from pydantic import BaseModel, Field
from datetime import datetime, date
from typing import Optional

class ReservationBase(BaseModel):
    guest_id: int = Field(..., description="Guest ID", example=1)
    room_id: int = Field(..., description="Room ID", example=1)
    check_in: date = Field(..., description="Check-in Date", example="2024-03-01")
    check_out: date = Field(..., description="Check-out Date", example="2024-03-05")

class ReservationCreate(ReservationBase):
    pass

class ReservationResponse(BaseModel):
    id: int
    guest_name: str
    guest_email: str
    room_number: str
    room_type: str
    check_in: date
    check_out: date
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
