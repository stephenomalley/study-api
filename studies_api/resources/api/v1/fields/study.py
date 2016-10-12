from studies_api.api.v1.fields import link_fields
from flask_restful import fields

study_fields = {
    "id": fields.String(attribute="_id"),
    "name": fields.String,
    "available_places": fields.Integer,
    "user": fields.String
}

study_list_fields = {
    "links": fields.Nested(link_fields),
    "data": fields.List(fields.Nested(study_fields))
}
