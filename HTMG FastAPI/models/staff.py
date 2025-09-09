from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from database import Base

class Staff(Base):
    __tablename__ = 'staff'
    
    id = Column(Integer, primary_key=True, autoincrement=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True, index=True)
    department = Column(String(50), nullable=False)  # housekeeping, front_desk, maintenance
    position = Column(String(50), nullable=False)
    created_at = Column(DateTime, default=datetime.now)
