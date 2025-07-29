#!/usr/bin/env python3

from flask import Flask, jsonify, request, make_response
from flask_migrate import Migrate
from flask_restful import Api, Resource
from models import db, Plant

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///plants.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = True

db.init_app(app)
migrate = Migrate(app, db)
api = Api(app)

class Plants(Resource):
    def get(self):
        plants = Plant.query.all()
        response_dict_list = [plant.to_dict() for plant in plants]
        return make_response(jsonify(response_dict_list), 200)

    def post(self):
        # Check if request has JSON data
        if not request.is_json:
            return make_response(jsonify({"error": "Request must be JSON"}), 400)

        data = request.get_json()

        # Validate required fields
        if 'name' not in data:
            return make_response(jsonify({"error": "Name is required"}), 400)

        try:
            new_plant = Plant(
                name=data['name'],
                image=data.get('image'),  # Optional field
                price=data.get('price')   # Optional field
            )

            db.session.add(new_plant)
            db.session.commit()

            return make_response(jsonify(new_plant.to_dict()), 201)

        except Exception as e:
            db.session.rollback()
            return make_response(jsonify({"error": str(e)}), 400)

api.add_resource(Plants, '/plants')

class PlantByID(Resource):
    def get(self, id):
        plant = db.session.get(Plant, id)  # Updated to recommended SQLAlchemy 2.0 style
        if plant is None:
            return make_response(jsonify({"error": "Plant not found"})), 404
        return make_response(jsonify(plant.to_dict()), 200)

api.add_resource(PlantByID, '/plants/<int:id>')

if __name__ == '__main__':
    app.run(port=5555, debug=True)
