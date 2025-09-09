from datetime import datetime
from api_server import db

class Guest(db.Model):
    __tablename__ = 'guests'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.now)

    @staticmethod
    def create_guest(data):
        """Create a new guest"""
        try:
            existing_guest = Guest.query.filter_by(email=data.get('email')).first()
            if existing_guest:
                return {'message': 'Guest with this email already exists', 'status_code': 2}, 409
            
            guest = Guest(**data)
            db.session.add(guest)
            db.session.commit()
            
            return {
                'message': 'Guest created successfully',
                'status_code': 1,
                'data': {
                    'id': guest.id,
                    'name': guest.name,
                    'email': guest.email,
                    'created_at': guest.created_at.isoformat()
                }
            }, 201
        except Exception as ex:
            db.session.rollback()
            return {'message': f'Error: {str(ex)}', 'status_code': 2}, 500

    @staticmethod
    def get_all_guests():
        """Get all guests"""
        try:
            guests = Guest.query.all()
            guest_list = [{
                'id': g.id,
                'name': g.name,
                'email': g.email,
                'created_at': g.created_at.isoformat()
            } for g in guests]
            
            return {
                'message': 'Guests retrieved successfully',
                'status_code': 1,
                'data': guest_list
            }, 200
        except Exception as ex:
            return {'message': f'Error: {str(ex)}', 'status_code': 2}, 500

    @staticmethod
    def get_guest_by_id(guest_id):
        """Get guest by ID"""
        try:
            guest = Guest.query.get(guest_id)
            if not guest:
                return {'message': 'Guest not found', 'status_code': 2}, 404
            
            return {
                'message': 'Guest retrieved successfully',
                'status_code': 1,
                'data': {
                    'id': guest.id,
                    'name': guest.name,
                    'email': guest.email,
                    'created_at': guest.created_at.isoformat()
                }
            }, 200
        except Exception as ex:
            return {'message': f'Error: {str(ex)}', 'status_code': 2}, 500
