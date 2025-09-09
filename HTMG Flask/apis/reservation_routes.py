from flask_restx import Resource, fields, Namespace, reqparse
from api_server import api
from flask import request
from models import Reservation

# Define namespace
reservation_ns = Namespace('Reservations', description='Reservation Management API')

# Base response model
base_response_model = api.model('Reservation Base Response Model', {
    'status_code': fields.Integer(description='Status Code (1=Success, 2=Error)'),
    'message': fields.String(description='Message'),
    'data': fields.Raw(description='Response data', required=False)
})

# Reservation input model
reservation_input_model = api.model('Reservation Input Model', {
    'guest_id': fields.Integer(description='Guest ID', required=True, example=1),
    'room_id': fields.Integer(description='Room ID', required=True, example=1),
    'check_in': fields.String(description='Check-in Date (YYYY-MM-DD)', required=True, example='2024-03-01'),
    'check_out': fields.String(description='Check-out Date (YYYY-MM-DD)', required=True, example='2024-03-05')
})

# Reservation response model
reservation_response_model = api.model('Reservation Response Model', {
    'id': fields.Integer(description='Reservation ID'),
    'guest_name': fields.String(description='Guest Name'),
    'guest_email': fields.String(description='Guest Email'),
    'room_number': fields.String(description='Room Number'),
    'room_type': fields.String(description='Room Type'),
    'check_in': fields.String(description='Check-in Date'),
    'check_out': fields.String(description='Check-out Date'),
    'status': fields.String(description='Reservation Status'),
    'created_at': fields.String(description='Creation Date')
})

@reservation_ns.route('')
class ReservationApi(Resource):
    @api.expect(reservation_input_model, validate=True)
    @api.response(201, 'Reservation created successfully', base_response_model)
    @api.response(400, 'Validation error', base_response_model)
    @api.response(404, 'Guest or Room not found', base_response_model)
    @api.response(409, 'Room not available', base_response_model)
    @api.response(500, 'Internal server error', base_response_model)
    def post(self):
        """
        Create a new reservation (Book a room)
        """
        try:
            payload = api.payload
            response, status = Reservation.create_reservation(payload)
            return response, status
        except Exception as ex:
            return {'message': f'Internal Server Error: {ex}', 'status_code': 2}, 500

    @api.response(200, 'List of reservations', base_response_model)
    @api.response(500, 'Internal server error', base_response_model)
    def get(self):
        """
        Get all reservations
        """
        try:
            response, status = Reservation.get_all_reservations()
            return response, status
        except Exception as ex:
            return {'message': f'Internal Server Error: {ex}', 'status_code': 2}, 500

@reservation_ns.route('/guest/<int:guest_id>')
class GuestReservationsApi(Resource):
    @api.response(200, 'Guest reservations', base_response_model)
    @api.response(500, 'Internal server error', base_response_model)
    def get(self, guest_id):
        """
        View guest reservations by guest ID
        """
        try:
            response, status = Reservation.get_guest_reservations(guest_id)
            return response, status
        except Exception as ex:
            return {'message': f'Internal Server Error: {ex}', 'status_code': 2}, 500
