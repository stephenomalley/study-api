import os

from flask import Flask, Blueprint
from flask_restful import Api
from pymongo import MongoClient

app = Flask(__name__)
api_blueprint = Blueprint('api', __name__)

api = Api(app)
app.register_blueprint(api_blueprint)

if os.environ.get("MONGOHQ_URL", None):
    from pymongo import uri_parser

    client = MongoClient(os.environ.get("MONGOHQ_URL"))
    # Specify the database
    db = client[uri_parser.parse_uri(os.environ.get("MONGOHQ_URL"))['database']]
else:
    import mock
    db = mock.MagicMock()

import resources.study