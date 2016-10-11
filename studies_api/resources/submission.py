from flask_restful import Resource
from studies_api import api


class Submission(Resource):
    def get(self):
        pass

    def post(self):
        pass


api.add_resource(Submission, '/submissions/<string:id>')
