from .guests import router as guest_router
from .rooms import router as room_router
from .staff import router as staff_router
from .reservations import router as reservation_router

__all__ = ['guest_router', 'room_router', 'staff_router', 'reservation_router']
