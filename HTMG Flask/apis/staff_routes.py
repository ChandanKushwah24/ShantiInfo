from flask_restx import Resource, fields, Namespace, reqparse
from api_server import api
from flask import request
from models import Staff
from .common_functions import CommonFunctions
from datetime import datetime

# Define namespace
staff_ns = Namespace('Staff', description='Staff Management API')

# Base response model
base_response_model = api.model('Staff Base Response Model', {
    'status_code': fields.Integer(description='Status Code (1=Success, 2=Error)'),
    'message': fields.String(description='Message'),
    'data': fields.Raw(description='Response data', required=False)
})

# Staff input model
staff_input_model = api.model('Staff Input Model', {
    'name': fields.String(description='Full Name', required=True, example='Jane Smith', min_length=1, max_length=100),
    'email': fields.String(description='Email', required=True, example='jane.smith@hotel.com'),
    'department': fields.String(description='Department', required=True, example='housekeeping', 
                               enum=['housekeeping', 'front_desk', 'maintenance']),
    'position': fields.String(description='Position', required=True, example='Housekeeper', min_length=1, max_length=50)
})

# Staff response model
staff_response_model = api.model('Staff Response Model', {
    'id': fields.Integer(description='Staff ID'),
    'name': fields.String(description='Full Name'),
    'email': fields.String(description='Email'),
    'department': fields.String(description='Department'),
    'position': fields.String(description='Position'),
    'created_at': fields.String(description='Creation Date')
})

@staff_ns.route('')
class StaffListApi(Resource):
    @api.expect(staff_input_model, validate=True)
    @api.response(201, 'Staff member created successfully', base_response_model)
    @api.response(400, 'Validation error', base_response_model)
    @api.response(409, 'Staff member already exists', base_response_model)
    @api.response(500, 'Internal server error', base_response_model)
    def post(self):
        """
        Create a new staff member
        """
        try:
            payload = api.payload
            
            # Validate email
            if not CommonFunctions.validate_email(payload.get('email')):
                return {'message': 'Please enter a valid email address', 'status_code': 2}, 400
            
            response, status = Staff.create_staff(payload)
            return response, status
        except Exception as ex:
            return {'message': f'Internal Server Error: {ex}', 'status_code': 2}, 500

    @api.response(200, 'List of staff members', base_response_model)
    @api.response(500, 'Internal server error', base_response_model)
    @api.doc(params={'department': 'Filter by department (housekeeping, front_desk, maintenance)'})
    def get(self):
        """
        Get all staff members with optional department filter
        """
        try:
            # Get department filter from query parameters
            parser = reqparse.RequestParser()
            parser.add_argument('department', type=str, location='args', 
                              choices=['housekeeping', 'front_desk', 'maintenance'], 
                              help='Filter by department')
            args = parser.parse_args()
            
            response, status = Staff.get_all_staff(department_filter=args.get('department'))
            return response, status
        except Exception as ex:
            return {'message': f'Internal Server Error: {ex}', 'status_code': 2}, 500
