# study-api

Simple Flask app that makes use of the Flask-Restful frame work and pymongo 
to query the database.

## Run instructions
Set up mongodb then create new database. 

run `db.submissions.createIndex( { study: 1, user: 1}, { unique: true })`
This will stop a submission for a study having same users.


Set env variable `MONGOHQ_URL=<mongo-db-connection>`
then run `python runserver.py`

## TroubleShooting

Any issues connecting to the database then make sure the mongod
process is up and running and you are pointing to the correct database


## End-points

The end points that are available are listed below. 
Since swagger has been implemented a more detailed description of the
end points can be found at `api/spec`.

Method | URI                    | Data | HTTP Code | Response (in JSON) |
| -----| ---                    | ---- | --------- | ------------------ |
| GET  | /api/v1/studies/id     |      | 200       | {"id": "efw9331","name": "test", "user":"8jdiejof", "available_places": 20} |
| GET  | /api/v1/studies        |      | 200       | ["data": [{"id": "efw9331","name": "test", "user":"8jdiejof", "available_places": 20}], "links": {self: "path/studies"}} |
| POST | /api/v1/studies        |      | 201       | {"id": "efw9331","name": "test", "user":1, "available_places": 20} |
| GET  | /api/v1/submissions/id |      | 200       | {"id": "fkffvfkv","study": "ju78sjall89", "user":"kio72dk3", "created": 12930202 } |
| GET  | /api/v1/submissions    |      | 200       | ["data": [{"id": "fkffvfkv","study": "ju78sjall89", "user":"kio72dk3", "created": 12930202}], "links": {self: "path/submissions"}} |
| POST | /api/v1/submissions    |      | 201       | {"id": "fkffvfkv","study": "ju78sjall89", "user":"kio72dk3", "created": 12930202 } |


##TODO
* Set up mongo db
* Complete tests
* Comment all code
* Add details to ReadMe
