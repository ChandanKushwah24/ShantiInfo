from datetime import datetime
from api_server import db

class Room(db.Model):
    __tablename__ = 'rooms'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    room_number = db.Column(db.String(10), nullable=False, unique=True)
    room_type = db.Column(db.String(50), nullable=False)  # single, double, suite
    status = db.Column(db.String(20), nullable=False, default='available')  # available, occupied, maintenance
    created_at = db.Column(db.DateTime, default=datetime.now)

    @staticmethod
    def create_room(data):
        """Create a new room"""
        try:
            existing_room = Room.query.filter_by(room_number=data.get('room_number')).first()
            if existing_room:
                return {'message': 'Room number already exists', 'status_code': 2}, 409
            
            room = Room(**data)
            db.session.add(room)
            db.session.commit()
            
            return {
                'message': 'Room created successfully',
                'status_code': 1,
                'data': {
                    'id': room.id,
                    'room_number': room.room_number,
                    'room_type': room.room_type,
                    'status': room.status,
                    'created_at': room.created_at.isoformat()
                }
            }, 201
        except Exception as ex:
            db.session.rollback()
            return {'message': f'Error: {str(ex)}', 'status_code': 2}, 500

    @staticmethod
    def get_all_rooms(status_filter=None):
        """Get all rooms with optional status filter"""
        try:
            if status_filter:
                rooms = Room.query.filter_by(status=status_filter).all()
            else:
                rooms = Room.query.all()
            
            room_list = [{
                'id': r.id,
                'room_number': r.room_number,
                'room_type': r.room_type,
                'status': r.status,
                'created_at': r.created_at.isoformat()
            } for r in rooms]
            
            return {
                'message': 'Rooms retrieved successfully',
                'status_code': 1,
                'data': room_list
            }, 200
        except Exception as ex:
            return {'message': f'Error: {str(ex)}', 'status_code': 2}, 500

    @staticmethod
    def check_room_availability(room_id, check_in, check_out):
        """Check if room is available for given dates"""
        try:
            from models.reservations import Reservation
            
            room = Room.query.get(room_id)
            if not room or room.status != 'available':
                return False
            
            overlapping = Reservation.query.filter(
                Reservation.room_id == room_id,
                Reservation.status.in_(['confirmed', 'checked_in']),
                Reservation.check_out > check_in,
                Reservation.check_in < check_out
            ).first()

            return overlapping is None
        except Exception:
            return False
