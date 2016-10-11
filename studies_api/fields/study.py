from flask_restful import fields

study_link_fields = {
    'self': fields.Url(absolute=True)
}

study_fields = {
    "id": fields.String(attribute="_id"),
    "name": fields.String,
    "available_places": fields.Integer,
    "user": fields.Integer
}

study_list_fields = {
    "links": fields.Nested(study_link_fields),
    "data": fields.List(fields.Nested(study_fields))
}
