import re
from datetime import date
from sqlalchemy.orm import Session
from models.reservations import Reservation
from models.rooms import Room

class CommonFunctions:

    @staticmethod
    def validate_email(email: str) -> bool:
        """Custom email validation function"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def check_room_availability(db: Session, room_id: int, check_in: date, check_out: date) -> bool:
        """Check if room is available for given dates"""
        try:
            room = db.query(Room).filter(Room.id == room_id).first()
            if not room or room.status != 'available':
                return False
            
            overlapping = db.query(Reservation).filter(
                Reservation.room_id == room_id,
                Reservation.status.in_(['confirmed', 'checked_in']),
                Reservation.check_out > check_in,
                Reservation.check_in < check_out
            ).first()

            return overlapping is None
        except Exception:
            return False
