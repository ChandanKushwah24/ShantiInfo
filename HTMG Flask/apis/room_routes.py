from flask_restx import Resource, fields, Namespace, reqparse
from api_server import api
from flask import request
from models import Room

# Define namespace
room_ns = Namespace('Rooms', description='Room Management API')

# Base response model
base_response_model = api.model('Room Base Response Model', {
    'status_code': fields.Integer(description='Status Code (1=Success, 2=Error)'),
    'message': fields.String(description='Message'),
    'data': fields.Raw(description='Response data', required=False)
})

# Room input model
room_input_model = api.model('Room Input Model', {
    'room_number': fields.String(description='Room Number', required=True, example='101', min_length=1, max_length=10),
    'room_type': fields.String(description='Room Type', required=True, example='single', enum=['single', 'double', 'suite']),
})

# Room response model
room_response_model = api.model('Room Response Model', {
    'id': fields.Integer(description='Room ID'),
    'room_number': fields.String(description='Room Number'),
    'room_type': fields.String(description='Room Type'),
    'status': fields.String(description='Room Status'),
    'created_at': fields.String(description='Creation Date')
})

@room_ns.route('')
class RoomListApi(Resource):
    @api.expect(room_input_model, validate=True)
    @api.response(201, 'Room created successfully', base_response_model)
    @api.response(400, 'Validation error', base_response_model)
    @api.response(409, 'Room already exists', base_response_model)
    @api.response(500, 'Internal server error', base_response_model)
    def post(self):
        """
        Create a new room
        """
        try:
            payload = api.payload
            response, status = Room.create_room(payload)
            return response, status
        except Exception as ex:
            return {'message': f'Internal Server Error: {ex}', 'status_code': 2}, 500

    @api.response(200, 'List of rooms', base_response_model)
    @api.response(500, 'Internal server error', base_response_model)
    @api.doc(params={'status': 'Filter by room status (available, occupied, maintenance)'})
    def get(self):
        """
        Get all rooms with optional status filter
        """
        try:
            # Get status filter from query parameters
            parser = reqparse.RequestParser()
            parser.add_argument('status', type=str, location='args', 
                              choices=['available', 'occupied', 'maintenance'], 
                              help='Filter by room status')
            args = parser.parse_args()
            
            response, status = Room.get_all_rooms(status_filter=args.get('status'))
            return response, status
        except Exception as ex:
            return {'message': f'Internal Server Error: {ex}', 'status_code': 2}, 500

