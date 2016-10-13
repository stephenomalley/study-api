from flask_restful import fields
from flask_restful_swagger import swagger
from studies_api.rest.v1.swagger_models import link_fields


@swagger.model
class Submission:
    """
    A Submission model. A submission must have a study and a user and the same user can't have a multiple submissions
    for a single study. Further there can only be study.available_places submissions for a study.

    """
    resource_fields = {
        "id": fields.String(attribute="_id"),
        "study": fields.String,
        "user": fields.String,
        "created": fields.Integer
    }

    submission_list_fields = {
        "links": fields.Nested(link_fields),
        "data": fields.List(fields.Nested(resource_fields))
    }
