from flask_restful import fields

link_fields = {
    'self': fields.Url(absolute=True)
}
