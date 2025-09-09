from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from datetime import date

from database import get_db
from models.reservations import Reservation
from models.guests import Guest
from models.rooms import Room
from schemas.reservations import ReservationCreate, ReservationResponse
from schemas.base import BaseResponse
from utils.common_functions import CommonFunctions

router = APIRouter(prefix="/reservations", tags=["Reservations"])

@router.post("", 
    response_model=BaseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new reservation (Book a room)",
    responses={
        201: {"description": "Reservation created successfully"},
        400: {"description": "Validation error"},
        404: {"description": "Guest or Room not found"},
        409: {"description": "Room not available"},
        500: {"description": "Internal server error"}
    }
)
def create_reservation(reservation: ReservationCreate, db: Session = Depends(get_db)):
    """
    Create a new reservation with the following information:
    - **guest_id**: ID of the guest making the reservation
    - **room_id**: ID of the room to be reserved
    - **check_in**: Check-in date (YYYY-MM-DD)
    - **check_out**: Check-out date (YYYY-MM-DD)
    """
    try:
        # Check if guest exists
        guest = db.query(Guest).filter(Guest.id == reservation.guest_id).first()
        if not guest:
            return BaseResponse(
                status_code=2,
                message="Guest not found"
            )

        # Check if room exists
        room = db.query(Room).filter(Room.id == reservation.room_id).first()
        if not room:
            return BaseResponse(
                status_code=2,
                message="Room not found"
            )

        # Validate dates
        if reservation.check_in >= reservation.check_out:
            return BaseResponse(
                status_code=2,
                message="Check-out must be after check-in"
            )
        
        if reservation.check_in < date.today():
            return BaseResponse(
                status_code=2,
                message="Check-in cannot be in the past"
            )

        # Check room availability
        if not CommonFunctions.check_room_availability(db, reservation.room_id, reservation.check_in, reservation.check_out):
            return BaseResponse(
                status_code=2,
                message="Room not available for selected dates"
            )

        # Create new reservation
        db_reservation = Reservation(**reservation.dict())
        db.add(db_reservation)
        db.commit()
        db.refresh(db_reservation)
        
        return BaseResponse(
            status_code=1,
            message="Reservation created successfully",
            data={
                "id": db_reservation.id,
                "guest_name": guest.name,
                "room_number": room.room_number,
                "check_in": db_reservation.check_in.isoformat(),
                "check_out": db_reservation.check_out.isoformat(),
                "status": db_reservation.status
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
    summary="Get all reservations",
    responses={
        200: {"description": "List of reservations"},
        500: {"description": "Internal server error"}
    }
)
def get_all_reservations(db: Session = Depends(get_db)):
    """
    Get all reservations from the database
    """
    try:
        reservations = db.query(Reservation).join(Guest).join(Room).all()
        
        reservation_list = [
            {
                "id": r.id,
                "guest_name": r.guest.name,
                "guest_email": r.guest.email,
                "room_number": r.room.room_number,
                "room_type": r.room.room_type,
                "check_in": r.check_in.isoformat(),
                "check_out": r.check_out.isoformat(),
                "status": r.status,
                "created_at": r.created_at.isoformat()
            }
            for r in reservations
        ]
        
        return BaseResponse(
            status_code=1,
            message="Reservations retrieved successfully",
            data=reservation_list
        )
    except Exception as ex:
        return BaseResponse(
            status_code=2,
            message=f"Internal Server Error: {ex}"
        )

@router.get("/guest/{guest_id}", 
    response_model=BaseResponse,
    summary="View guest reservations by guest ID",
    responses={
        200: {"description": "Guest reservations"},
        500: {"description": "Internal server error"}
    }
)
def get_guest_reservations(guest_id: int, db: Session = Depends(get_db)):
    """
    Get all reservations for a specific guest
    """
    try:
        reservations = db.query(Reservation).filter(Reservation.guest_id == guest_id).join(Room).all()
        
        reservation_list = [
            {
                "id": r.id,
                "room_number": r.room.room_number,
                "room_type": r.room.room_type,
                "check_in": r.check_in.isoformat(),
                "check_out": r.check_out.isoformat(),
                "status": r.status,
                "created_at": r.created_at.isoformat()
            }
            for r in reservations
        ]
        
        return BaseResponse(
            status_code=1,
            message="Guest reservations retrieved successfully",
            data=reservation_list
        )
    except Exception as ex:
        return BaseResponse(
            status_code=2,
            message=f"Internal Server Error: {ex}"
        )
