from datetime import datetime
from api_server import db

class Staff(db.Model):
    __tablename__ = 'staff'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    department = db.Column(db.String(50), nullable=False)  # housekeeping, front_desk, maintenance
    position = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)

    @staticmethod
    def create_staff(data):
        """Create a new staff member"""
        try:
            existing_staff = Staff.query.filter_by(email=data.get('email')).first()
            if existing_staff:
                return {'message': 'Staff member with this email already exists', 'status_code': 2}, 409
            
            staff = Staff(**data)
            db.session.add(staff)
            db.session.commit()
            
            return {
                'message': 'Staff member created successfully',
                'status_code': 1,
                'data': {
                    'id': staff.id,
                    'name': staff.name,
                    'email': staff.email,
                    'department': staff.department,
                    'position': staff.position,
                    'created_at': staff.created_at.isoformat()
                }
            }, 201
        except Exception as ex:
            db.session.rollback()
            return {'message': f'Error: {str(ex)}', 'status_code': 2}, 500

    @staticmethod
    def get_all_staff(department_filter=None):
        """Get all staff with optional department filter"""
        try:
            if department_filter:
                staff_members = Staff.query.filter_by(department=department_filter).all()
            else:
                staff_members = Staff.query.all()
            
            staff_list = [{
                'id': s.id,
                'name': s.name,
                'email': s.email,
                'department': s.department,
                'position': s.position,
                'created_at': s.created_at.isoformat()
            } for s in staff_members]
            
            return {
                'message': 'Staff retrieved successfully',
                'status_code': 1,
                'data': staff_list
            }, 200
        except Exception as ex:
            return {'message': f'Error: {str(ex)}', 'status_code': 2}, 500
