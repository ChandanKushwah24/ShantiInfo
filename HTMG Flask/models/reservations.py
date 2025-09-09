from datetime import datetime, date
from api_server import db

class Reservation(db.Model):
    __tablename__ = 'reservations'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    guest_id = db.Column(db.Integer, db.ForeignKey('guests.id'), nullable=False)
    room_id = db.Column(db.Integer, db.ForeignKey('rooms.id'), nullable=False)
    check_in = db.Column(db.Date, nullable=False)
    check_out = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='confirmed')
    created_at = db.Column(db.DateTime, default=datetime.now)

    # Relationships
    guest = db.relationship('Guest', backref=db.backref('reservations', lazy=True))
    room = db.relationship('Room', backref=db.backref('reservations', lazy=True))

    @staticmethod
    def create_reservation(data):
        """Create a new reservation with availability check"""
        try:
            from models.guests import Guest
            from models.rooms import Room
            
            guest = Guest.query.get(data.get('guest_id'))
            if not guest:
                return {'message': 'Guest not found', 'status_code': 2}, 404

            room = Room.query.get(data.get('room_id'))
            if not room:
                return {'message': 'Room not found', 'status_code': 2}, 404

            check_in = datetime.strptime(data.get('check_in'), '%Y-%m-%d').date()
            check_out = datetime.strptime(data.get('check_out'), '%Y-%m-%d').date()

            if check_in >= check_out:
                return {'message': 'Check-out must be after check-in', 'status_code': 2}, 400
            
            if check_in < date.today():
                return {'message': 'Check-in cannot be in the past', 'status_code': 2}, 400

            if not Room.check_room_availability(data.get('room_id'), check_in, check_out):
                return {'message': 'Room not available for selected dates', 'status_code': 2}, 409


            reservation = Reservation(
                guest_id=data.get('guest_id'),
                room_id=data.get('room_id'),
                check_in=check_in,
                check_out=check_out
            )

            db.session.add(reservation)
            db.session.commit()
            
            return {
                'message': 'Reservation created successfully',
                'status_code': 1,
                'data': {
                    'id': reservation.id,
                    'guest_name': guest.name,
                    'room_number': room.room_number,
                    'check_in': reservation.check_in.isoformat(),
                    'check_out': reservation.check_out.isoformat(),
                    'status': reservation.status
                }
            }, 201
        except Exception as ex:
            db.session.rollback()
            return {'message': f'Error: {str(ex)}', 'status_code': 2}, 500

    @staticmethod
    def get_guest_reservations(guest_id):
        """Get all reservations for a guest"""
        try:
            reservations = Reservation.query.filter_by(guest_id=guest_id).all()
            
            reservation_list = [{
                'id': r.id,
                'room_number': r.room.room_number,
                'room_type': r.room.room_type,
                'check_in': r.check_in.isoformat(),
                'check_out': r.check_out.isoformat(),
                'status': r.status,
                'created_at': r.created_at.isoformat()
            } for r in reservations]
            
            return {
                'message': 'Guest reservations retrieved successfully',
                'status_code': 1,
                'data': reservation_list
            }, 200
        except Exception as ex:
            return {'message': f'Error: {str(ex)}', 'status_code': 2}, 500

    @staticmethod
    def get_all_reservations():
        """Get all reservations"""
        try:
            reservations = Reservation.query.all()
            
            reservation_list = [{
                'id': r.id,
                'guest_name': r.guest.name,
                'guest_email': r.guest.email,
                'room_number': r.room.room_number,
                'room_type': r.room.room_type,
                'check_in': r.check_in.isoformat(),
                'check_out': r.check_out.isoformat(),
                'status': r.status,
                'created_at': r.created_at.isoformat()
            } for r in reservations]
            
            return {
                'message': 'Reservations retrieved successfully',
                'status_code': 1,
                'data': reservation_list
            }, 200
        except Exception as ex:
            return {'message': f'Error: {str(ex)}', 'status_code': 2}, 500
