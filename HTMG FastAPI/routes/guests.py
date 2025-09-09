from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from database import get_db
from models.guests import Guest
from schemas.guests import GuestCreate, GuestResponse
from schemas.base import BaseResponse

router = APIRouter(prefix="/guests", tags=["Guests"])

@router.post("", 
    response_model=BaseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new guest",
    responses={
        201: {"description": "Guest created successfully"},
        400: {"description": "Validation error"},
        409: {"description": "Guest already exists"},
        500: {"description": "Internal server error"}
    }
)
def create_guest(guest: GuestCreate, db: Session = Depends(get_db)):
    """
    Create a new guest with the following information:
    - **name**: Full name of the guest
    - **email**: Valid email address
    """
    try:
        # Check if guest already exists
        existing_guest = db.query(Guest).filter(Guest.email == guest.email).first()
        if existing_guest:
            return BaseResponse(
                status_code=2,
                message="Guest with this email already exists"
            )
        
        # Create new guest
        db_guest = Guest(**guest.dict())
        db.add(db_guest)
        db.commit()
        db.refresh(db_guest)
        
        return BaseResponse(
            status_code=1,
            message="Guest created successfully",
            data={
                "id": db_guest.id,
                "name": db_guest.name,
                "email": db_guest.email,
                "created_at": db_guest.created_at.isoformat()
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
    summary="Get all guests",
    responses={
        200: {"description": "List of guests"},
        500: {"description": "Internal server error"}
    }
)
def get_all_guests(db: Session = Depends(get_db)):
    """
    Get all guests from the database
    """
    try:
        guests = db.query(Guest).all()
        guest_list = [
            {
                "id": g.id,
                "name": g.name,
                "email": g.email,
                "created_at": g.created_at.isoformat()
            }
            for g in guests
        ]
        
        return BaseResponse(
            status_code=1,
            message="Guests retrieved successfully",
            data=guest_list
        )
    except Exception as ex:
        return BaseResponse(
            status_code=2,
            message=f"Internal Server Error: {ex}"
        )

@router.get("/{guest_id}", 
    response_model=BaseResponse,
    summary="Get guest details by ID",
    responses={
        200: {"description": "Guest details"},
        404: {"description": "Guest not found"},
        500: {"description": "Internal server error"}
    }
)
def get_guest_by_id(guest_id: int, db: Session = Depends(get_db)):
    """
    Get a specific guest by their ID
    """
    try:
        guest = db.query(Guest).filter(Guest.id == guest_id).first()
        if not guest:
            return BaseResponse(
                status_code=2,
                message="Guest not found"
            )
        
        return BaseResponse(
            status_code=1,
            message="Guest retrieved successfully",
            data={
                "id": guest.id,
                "name": guest.name,
                "email": guest.email,
                "created_at": guest.created_at.isoformat()
            }
        )
    except Exception as ex:
        return BaseResponse(
            status_code=2,
            message=f"Internal Server Error: {ex}"
        )
