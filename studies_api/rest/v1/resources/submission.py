import time

from bson.errors import InvalidId
from flask_restful import Resource, marshal_with, abort
from flask_restful import reqparse
from flask_restful_swagger import swagger
from pymongo.errors import DuplicateKeyError
from studies_api import api
from studies_api.rest.v1.exceptions.submission import SubmissionLimitExceeded, StudyNotCreated
from studies_api.rest.v1.helpers.submission import get_all_submissions, save_submission, get_submission_by_id
from studies_api.rest.v1.swagger_models.submission import Submission


class SubmissionResource(Resource):
    @marshal_with(Submission.resource_fields)
    @swagger.operation(
        description='Returns an instance of the Submission collection.',
        notes="id should be the ObjectId of the collection",
        responseClass=Submission.__name__,
        nickname='submission',
        summary='Returns an instance of the Submission collection',
        responseMessages=[
            {
                "code": 200,
                "message": "OK"
            },
            {
                "code": 400,
                "message": "Invalid input"
            },
            {
                "code": 404,
                "message": "Submission not found"
            }
        ]
    )
    def get(self, id):
        try:
            submission = get_submission_by_id(id)
        except InvalidId as id_error:
            abort(400, message=id_error.message)
        else:
            return submission if submission else abort(404, message="Submission not found")

    def post(self):
        raise NotImplementedError("Post not supported")

    def put(self):
        raise NotImplementedError("Update of submission not supported")

    def delete(self):
        raise NotImplementedError("Delete of a submission not supported")


class SubmissionListResource(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('study', type=str, help="The study the submission is for.", required=True)
    parser.add_argument("user", type=str, help="The ObjectId of the user that created the study.", required=True)
    parser.add_argument("created", type=int, help="The time submission was created")

    query_parser = reqparse.RequestParser()
    query_parser.add_argument('study', type=str, )
    query_parser.add_argument("user", type=str, )

    @marshal_with(Submission.submission_list_fields)
    @swagger.operation(
        description='Returns a list of all submissions.',
        notes="Optional parameters user and/or study can be past to return all submission for a user/study.",
        responseClass=Submission.__name__,
        nickname='submissions',
        summary='Returns a list of all submissions',
        responseMessages=[
            {
                "code": 200,
                "message": "Returns list of submissions"
            },
        ]
    )
    def get(self):
        args = self.query_parser.parse_args()
        filter = {}
        for key, value in args.iteritems():
            if value:
                filter.update({key: value})

        return {
            "data": [study for study in get_all_submissions(filter)],
            "links": {}
        }

    @marshal_with(Submission.resource_fields)
    @swagger.operation(
        description="If the post request contains the correct fields (user and study both required) then a new object "
                    "will be created and returned as json. Failure to provide user and study will result in a 400 error."
                    "If the study provided is not a valid study or if the number of submissions allowed has been exceeded then"
                    " no submission will be created and the api will return a bad request response",
        summary='Used to create a new instance of a Study',
        notes="No additional parameters other than user, name or available_places can be passed",
        responseClass=Submission.__name__,
        nickname='submission-post',
        responseMessages=[
            {
                "code": 201,
                "message": "Ok Created"
            },
            {
                "code": 400,
                "message": "Invalid input"
            },
        ]
    )
    def post(self):

        submission_data = self.parser.parse_args(strict=True)
        submission_data.update({'created': time.time()})

        try:
            submission = save_submission(submission_data)
        except (DuplicateKeyError, SubmissionLimitExceeded, StudyNotCreated) as save_down_error:
            return abort(400, message=save_down_error.message)

        return submission, 201

    def put(self):
        raise NotImplementedError("Update of submission not supported")

    def delete(self):
        raise NotImplementedError("Delete of a submission not supported")


api.add_resource(SubmissionListResource, '/api/v1/submissions', endpoint="submissions", methods=['GET', 'POST'])
api.add_resource(SubmissionResource, '/api/v1/submissions/<string:id>', endpoint="submission", methods=['GET'])
