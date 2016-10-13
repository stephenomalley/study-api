import os

from flask import Flask, Blueprint
from flask_restful import Api
from pymongo import MongoClient

# Creating Flask app and removing strict slashes
app = Flask(__name__)
api_blueprint = Blueprint('api', __name__)
app.register_blueprint(api_blueprint)
app.url_map.strict_slashes = False

# Initialising the flask restful API c.f http://flask-restful-cn.readthedocs.io/en/0.3.4/api.html#id1
api = Api(app)


# Checking that the environment variable is set if it isn't then we just use a mock db
# The mock db part was simply so that I could set things up quickly for testing without to much extra config, etc
# TODO get rid of the mock database it is just a hack to get tests setup quickly
if os.environ.get("MONGOHQ_URL", None):
    from pymongo import uri_parser

    client = MongoClient(os.environ.get("MONGOHQ_URL"))
    # Specify the database
    db = client[uri_parser.parse_uri(os.environ.get("MONGOHQ_URL"))['database']]
else:
    import mock
    db = mock.MagicMock()


# importing the resources so that the endpoints for the api are registered
from studies_api.resources.api.v1.study import Study, StudyList
from studies_api.resources.api.v1.submission import Submission, SubmissionList

