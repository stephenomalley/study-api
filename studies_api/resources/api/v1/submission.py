import time

from api.v1.exceptions.submission import SubmissionLimitExceeded, StudyNotCreated
from api.v1.fields.submission import submission_list_fields, submission_fields
from api.v1.helpers.submission import get_all_submissions, save_submission, get_submission_by_id
from bson.errors import InvalidId
from flask_restful import Resource, marshal_with, abort
from flask_restful import reqparse
from pymongo.errors import DuplicateKeyError
from studies_api import api

class Submission(Resource):

    @marshal_with(submission_fields)
    def get(self, id):
        try:
            study = get_submission_by_id(id)
        except InvalidId as id_error:
            abort(400, message=id_error.message)
        else:
            return study if study else abort(404, message="Submission not found")

    def post(self):
        pass

class SubmissionList(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('study', type=str, help="The study the submission is for.", required=True)
    parser.add_argument("user", type=str, help="The ObjectId of the user that created the study.", required=True)
    parser.add_argument("created", type=int, help="The time study was created")

    @marshal_with(submission_list_fields)
    def get(self):
        return {
            "data": [study for study in get_all_submissions()],
            "links": {}
        }

    @marshal_with(submission_fields)
    def post(self):

        study_data = self.parser.parse_args(strict=True)
        study_data.update({'created': time.time()})

        try:
            study = save_submission(study_data)
        except (DuplicateKeyError, SubmissionLimitExceeded, StudyNotCreated) as save_down_error:
            return abort(400, message=save_down_error.message)

        return study, 201

    def put(self):
        raise NotImplementedError("Update of study not supported")

    def delete(self):
        raise NotImplementedError("Delete of a study not supported")


api.add_resource(SubmissionList, '/api/v1/submissions', endpoint="submissions", methods=['GET', 'POST'])
api.add_resource(Submission, '/api/v1/submissions/<string:id>', endpoint="submission", methods=['GET', 'POST'])
