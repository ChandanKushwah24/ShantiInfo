from pydantic import BaseModel, Field
from datetime import datetime
from typing import Literal

class RoomBase(BaseModel):
    room_number: str = Field(..., min_length=1, max_length=10, description="Room Number", example="101")
    room_type: Literal["single", "double", "suite"] = Field(..., description="Room Type", example="single")

class RoomCreate(RoomBase):
    pass

class RoomResponse(RoomBase):
    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True
