import os
from datetime import timedelta

class Config:
    SECRET_KEY = 'hotel-management-secret-key-2024'
    
    SQLALCHEMY_DATABASE_URI = 'sqlite:///hotelDB.db'

