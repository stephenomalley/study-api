from flask_restful import Resource, marshal_with, abort
from studies_api import api
from studies_api.common.study import get_all_studies, get_study_by_id
from studies_api.fields.study import study_list_fields, study_fields


class Study(Resource):
    @marshal_with(study_fields)
    def get(self, id):
        study = get_study_by_id(id)
        if study:
            return study
        return abort(404, message="Study not found")

    def post(self):
        pass


class StudyList(Resource):
    @marshal_with(study_list_fields)
    def get(self):
        return {
            "data": [study for study in get_all_studies()],
            "links": {}
        }

    def post(self):
        pass


api.add_resource(StudyList, '/studies', endpoint="studies", methods=['GET', 'POST'])
api.add_resource(Study, '/studies/<int:id>', endpoint="study", methods=['GET', 'POST'])

