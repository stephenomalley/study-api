from flask_restful import Resource
from studies_api.app import api


class User(Resource):
    def get(self):
        pass

    def post(self):
        pass


api.add_resource(User, '/users/<string:id>')
