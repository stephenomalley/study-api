from flask_restful import fields
from flask_restful_swagger import swagger
from studies_api.rest.v1.swagger_models import link_fields


@swagger.model
class Study:
    """
    Model representing a Study. A study should have a name and be linked to the user who created it.
    A study should also have an available_places option that determines how many submissions a study can have.
    """
    resource_fields = {
        "id": fields.String(attribute="_id"),
        "name": fields.String,
        "available_places": fields.Integer,
        "user": fields.String
    }

    study_list_fields = {
        "links": fields.Nested(link_fields),
        "data": fields.List(fields.Nested(resource_fields))
    }
