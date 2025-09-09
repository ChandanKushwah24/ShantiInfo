from flask_restx import Resource, fields, Namespace
from api_server import api
from flask import request
from models import Guest
from .common_functions import CommonFunctions

# Define namespace
guest_ns = Namespace('Guests', description='Guest Management API')

# Base response model
base_response_model = api.model('Guest Base Response Model', {
    'status_code': fields.Integer(description='Status Code (1=Success, 2=Error)'),
    'message': fields.String(description='Message'),
    'data': fields.Raw(description='Response data', required=False)
})

# Guest input model
guest_input_model = api.model('Guest Input Model', {
    'name': fields.String(description='Full Name', required=True, example='John Doe', min_length=1, max_length=100),
    'email': fields.String(description='Email', required=True, example='john.doe@example.com')
})

# Guest response model
guest_response_model = api.model('Guest Response Model', {
    'id': fields.Integer(description='Guest ID'),
    'name': fields.String(description='Full Name'),
    'email': fields.String(description='Email'),
    'created_at': fields.String(description='Creation Date')
})

@guest_ns.route('')
class GuestListApi(Resource):
    @api.expect(guest_input_model, validate=True)
    @api.response(201, 'Guest created successfully', base_response_model)
    @api.response(400, 'Validation error', base_response_model)
    @api.response(409, 'Guest already exists', base_response_model)
    @api.response(500, 'Internal server error', base_response_model)
    def post(self):
        """
        Create a new guest
        """
        try:
            payload = api.payload
            
            # Validate email
            if not CommonFunctions.validate_email(payload.get('email')):
                return {'message': 'Please enter a valid email address', 'status_code': 2}, 400
            
            response, status = Guest.create_guest(payload)
            return response, status
        except Exception as ex:
            return {'message': f'Internal Server Error: {ex}', 'status_code': 2}, 500

    @api.response(200, 'List of guests', base_response_model)
    @api.response(500, 'Internal server error', base_response_model)
    def get(self):
        """
        Get all guests
        """
        try:
            response, status = Guest.get_all_guests()
            return response, status
        except Exception as ex:
            return {'message': f'Internal Server Error: {ex}', 'status_code': 2}, 500

@guest_ns.route('/<int:guest_id>')
class GuestDetailApi(Resource):
    @api.response(200, 'Guest details', base_response_model)
    @api.response(404, 'Guest not found', base_response_model)
    @api.response(500, 'Internal server error', base_response_model)
    def get(self, guest_id):
        """
        Get guest details by ID
        """
        try:
            response, status = Guest.get_guest_by_id(guest_id)
            return response, status
        except Exception as ex:
            return {'message': f'Internal Server Error: {ex}', 'status_code': 2}, 500
