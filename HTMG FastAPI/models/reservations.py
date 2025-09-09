from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Reservation(Base):
    __tablename__ = 'reservations'
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    guest_id = Column(Integer, ForeignKey('guests.id'), nullable=False)
    room_id = Column(Integer, ForeignKey('rooms.id'), nullable=False)
    check_in = Column(Date, nullable=False)
    check_out = Column(Date, nullable=False)
    status = Column(String(20), nullable=False, default='confirmed')
    created_at = Column(DateTime, default=datetime.now)

    # Relationships
    guest = relationship("Guest", back_populates="reservations")
    room = relationship("Room", back_populates="reservations")
