from bson.errors import InvalidId
from flask_restful import Resource, marshal_with, abort
from flask_restful import reqparse
from studies_api import api
from studies_api.common.study import get_all_studies, get_study_by_id, save_study
from studies_api.fields.study import study_list_fields, study_fields


class Study(Resource):

    @marshal_with(study_fields)
    def get(self, id):
        try:
            study = get_study_by_id(id)
        except InvalidId as id_error:
            abort(400, message=id_error.message)
        else:
            return study if study else abort(404, message="Study not found")

    def post(self):
        pass


class StudyList(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, help="The name of the Study. Should not be blank.", required=True)
    parser.add_argument("user", type=str, help="The ObjectId of the user that created the study.", required=True)
    parser.add_argument("available_places", type=int, help="The number of places available on the study.")

    @marshal_with(study_list_fields)
    def get(self):
        return {
            "data": [study for study in get_all_studies()],
            "links": {}
        }

    @marshal_with(study_fields)
    def post(self):
        study_data = self.parser.parse_args(strict=True)
        study = save_study(study_data)
        return study, 201


api.add_resource(StudyList, '/api/v1/studies', endpoint="studies", methods=['GET', 'POST'])
api.add_resource(Study, '/api/v1/studies/<string:id>', endpoint="study", methods=['GET', 'POST'])

