from api.v1.fields import link_fields
from flask_restful import fields

submission_fields = {
    "id": fields.String(attribute="_id"),
    "study": fields.String,
    "user": fields.String,
    "created": fields.Integer
}

submission_list_fields = {
    "links": fields.Nested(link_fields),
    "data": fields.List(fields.Nested(submission_fields))
}
