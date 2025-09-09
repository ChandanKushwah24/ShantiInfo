from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db
from models.staff import Staff
from schemas.staff import StaffCreate, StaffResponse
from schemas.base import BaseResponse

router = APIRouter(prefix="/staff", tags=["Staff"])

@router.post("", 
    response_model=BaseResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new staff member",
    responses={
        201: {"description": "Staff member created successfully"},
        400: {"description": "Validation error"},
        409: {"description": "Staff member already exists"},
        500: {"description": "Internal server error"}
    }
)
def create_staff(staff: StaffCreate, db: Session = Depends(get_db)):
    """
    Create a new staff member with the following information:
    - **name**: Full name of the staff member
    - **email**: Valid email address
    - **department**: Department (housekeeping, front_desk, maintenance)
    - **position**: Job position
    """
    try:
        # Check if staff already exists
        existing_staff = db.query(Staff).filter(Staff.email == staff.email).first()
        if existing_staff:
            return BaseResponse(
                status_code=2,
                message="Staff member with this email already exists"
            )
        
        # Create new staff member
        db_staff = Staff(**staff.dict())
        db.add(db_staff)
        db.commit()
        db.refresh(db_staff)
        
        return BaseResponse(
            status_code=1,
            message="Staff member created successfully",
            data={
                "id": db_staff.id,
                "name": db_staff.name,
                "email": db_staff.email,
                "department": db_staff.department,
                "position": db_staff.position,
                "created_at": db_staff.created_at.isoformat()
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
    summary="Get all staff members with optional department filter",
    responses={
        200: {"description": "List of staff members"},
        500: {"description": "Internal server error"}
    }
)
def get_all_staff(
    department: Optional[str] = Query(None, description="Filter by department (housekeeping, front_desk, maintenance)"),
    db: Session = Depends(get_db)
):
    """
    Get all staff members from the database with optional department filtering
    """
    try:
        if department:
            staff_members = db.query(Staff).filter(Staff.department == department).all()
        else:
            staff_members = db.query(Staff).all()
        
        staff_list = [
            {
                "id": s.id,
                "name": s.name,
                "email": s.email,
                "department": s.department,
                "position": s.position,
                "created_at": s.created_at.isoformat()
            }
            for s in staff_members
        ]
        
        return BaseResponse(
            status_code=1,
            message="Staff retrieved successfully",
            data=staff_list
        )
    except Exception as ex:
        return BaseResponse(
            status_code=2,
            message=f"Internal Server Error: {ex}"
        )
