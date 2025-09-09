from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from database import Base

class Guest(Base):
    __tablename__ = 'guests'
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.now)
    
    # Relationships
    reservations = relationship("Reservation", back_populates="guest")
