from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from models.rooms import Room
from schemas.rooms import RoomCreate, RoomResponse
from schemas.base import BaseResponse

router = APIRouter(prefix="/rooms", tags=["Rooms"])

@router.post("", 
    response_model=BaseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new room",
    responses={
        201: {"description": "Room created successfully"},
        400: {"description": "Validation error"},
        409: {"description": "Room already exists"},
        500: {"description": "Internal server error"}
    }
)
def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    """
    Create a new room with the following information:
    - **room_number**: Unique room number
    - **room_type**: Type of room (single, double, suite)
    """
    try:
        # Check if room already exists
        existing_room = db.query(Room).filter(Room.room_number == room.room_number).first()
        if existing_room:
            return BaseResponse(
                status_code=2,
                message="Room number already exists"
            )
        
        # Create new room
        db_room = Room(**room.dict())
        db.add(db_room)
        db.commit()
        db.refresh(db_room)
        
        return BaseResponse(
            status_code=1,
            message="Room created successfully",
            data={
                "id": db_room.id,
                "room_number": db_room.room_number,
                "room_type": db_room.room_type,
                "status": db_room.status,
                "created_at": db_room.created_at.isoformat()
            }
        )
    except Exception as ex:
        db.rollback()
        return BaseResponse(
            status_code=2,
            message=f"Internal Server Error: {ex}"
        )

@router.get("", 
    response_model=BaseResponse,
    summary="Get all rooms with optional status filter",
    responses={
        200: {"description": "List of rooms"},
        500: {"description": "Internal server error"}
    }
)
def get_all_rooms(
    status_filter: Optional[str] = Query(None, description="Filter by room status (available, occupied, maintenance)"),
    db: Session = Depends(get_db)
):
    """
    Get all rooms from the database with optional status filtering
    """
    try:
        if status_filter:
            rooms = db.query(Room).filter(Room.status == status_filter).all()
        else:
            rooms = db.query(Room).all()
        
        room_list = [
            {
                "id": r.id,
                "room_number": r.room_number,
                "room_type": r.room_type,
                "status": r.status,
                "created_at": r.created_at.isoformat()
            }
            for r in rooms
        ]
        
        return BaseResponse(
            status_code=1,
            message="Rooms retrieved successfully",
            data=room_list
        )
    except Exception as ex:
        return BaseResponse(
            status_code=2,
            message=f"Internal Server Error: {ex}"
        )
