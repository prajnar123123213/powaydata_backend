from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from model.disaster import DisasterModel  # Import the DisasterModel class

disaster_api = Blueprint('disaster_api', __name__, url_prefix='/api/disaster')
api = Api(disaster_api)

class DisasterAPI:
    class _Predict(Resource):
        def post(self):
            # Get disaster data from the request
            data = request.get_json()

            # Get the singleton instance of DisasterModel
            model = DisasterModel.get_instance()

            # Predict survival outcome
            response = model.predict(data)

            # Return response as JSON
            return jsonify(response)

    api.add_resource(_Predict, '/predict')