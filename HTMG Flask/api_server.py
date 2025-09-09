from flask import Flask, Blueprint
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

from config import Config

api_blueprint = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_blueprint, title='Hotel Management API', doc='/docs')

db = SQLAlchemy()   

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)

    with app.app_context():
        app.register_blueprint(api_blueprint)

        from apis import guest_ns, room_ns, staff_ns, reservation_ns
        # Register namespaces (removed auth_ns)
        api.add_namespace(guest_ns, path='/guests')
        api.add_namespace(room_ns, path='/rooms')
        api.add_namespace(staff_ns, path='/staff')
        api.add_namespace(reservation_ns, path='/reservations')

        # Create all tables
        # db.drop_all()
        db.create_all()

        return app
