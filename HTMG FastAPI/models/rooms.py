from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Room(Base):
    __tablename__ = 'rooms'
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    room_number = Column(String(10), nullable=False, unique=True, index=True)
    room_type = Column(String(50), nullable=False)  # single, double, suite
    status = Column(String(20), nullable=False, default='available')  # available, occupied, maintenance
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    reservations = relationship("Reservation", back_populates="room")
