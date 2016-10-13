from bson.errors import InvalidId
from flask_restful import Resource, marshal_with, abort
from flask_restful import reqparse
from flask_restful_swagger import swagger
from studies_api import api
from studies_api.rest.v1.helpers.study import get_all_studies, get_study_by_id, save_study
from studies_api.rest.v1.swagger_models.study import Study


class StudyResource(Resource):
    @marshal_with(Study.resource_fields)
    @swagger.operation(
        description='Returns an instance of the Study collection.',
        notes="id should be the ObjectId of the collection",
        responseClass=Study.__name__,
        nickname='study',
        summary='Returns an instance of the Study collection',
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
                "message": "Study not found"
            }
        ]
    )
    def get(self, id):
        try:
            study = get_study_by_id(id)
        except InvalidId as id_error:
            abort(400, message=id_error.message)
        else:
            return study if study else abort(404, message="Study not found")

    def post(self):
        raise NotImplementedError("Post not supported")

    def put(self):
        raise NotImplementedError("Update of study not supported")

    def delete(self):
        raise NotImplementedError("Delete of a study not supported")


class StudyListResource(Resource):
    query_parser = reqparse.RequestParser()
    query_parser.add_argument("user", type=str)

    parser = reqparse.RequestParser()
    parser.add_argument('name', type=str, help="The name of the Study. Should not be blank.", required=True)
    parser.add_argument("user", type=str, help="The ObjectId of the user that created the study.", required=True)
    parser.add_argument("available_places", type=int, help="The number of places available on the study.")

    @marshal_with(Study.study_list_fields)
    @swagger.operation(
        description='Returns a list of all studies.',
        notes="Optional parameter user can be past to return all Studies belonging to that user",
        responseClass=Study.__name__,
        nickname='studies',
        summary='Returns a list of all studies',
        responseMessages=[
            {
                "code": 200,
                "message": "Returns list of studies"
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
            "data": [study for study in get_all_studies(filter)],
            "links": {}
        }

    @marshal_with(Study.resource_fields)
    @swagger.operation(
        description="If the post request contains the correct fields (user, name or available_places) then a new object "
                    "will be created and returned as json. If name or user are missing then an error will be thrown."
                    "available places will default to 0 and must be a number",
        summary='Used to create a new instance of a Study',
        notes="No additional parameters other than user, name or available_places can be passed",
        responseClass=Study.__name__,
        nickname='study-post',
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
        study_data = self.parser.parse_args(strict=True)
        study = save_study(study_data)
        return study, 201

    def put(self):
        raise NotImplementedError("Update of study not supported")

    def delete(self):
        raise NotImplementedError("Delete of a study not supported")


api.add_resource(StudyListResource, '/api/v1/studies', endpoint="studies", methods=['GET', 'POST'])
api.add_resource(StudyResource, '/api/v1/studies/<string:id>', endpoint="study", methods=['GET'])
