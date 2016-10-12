# study-api

Simple Flask app that makes use of the Flask-Restful frame work and pymongo 
to query the database.

## Run instructions
Set up mongodb then create new database. 

run `db.submissions.createIndex( { study: 1, user: 1}, { unique: true } )`
This will stop a submission for a study having same users.


Set env variable `MONGOHQ_URL=<mongo-db-connection>`
then run `python runserver.py`

## TroubleShooting

Any issues connecting to the database then make sure the mongod
process is up and running and you are pointing to the correct database



## Study end-points

 Method | URI | Data | HTTP Code | Response (in JSON) |
| ------ | --- | ---- | --------- | ------------------ |
| GET  | /api/v1/studies/id |  | 200 | {"id": 1,"name": "test", "user":1} |
| GET  | /api/v1/studies  |  | 200 | ["data": [{"id": 1,"name": "test", "user":1}, "links": {self: "path/studies"}] |
| GET  | /api/v1/submissions/id |  | 200 | {"id": "fkffvfkv","name": "test", "user":1} |
| GET  | /api/v1/submissions  |  | 200 | ["data": [{"id": "fkffvfkv","study": "23243", "user":1}, "links": {self: "path/submissions"}] |

## Submission end-points


##TODO
* Add filter params on some urls
* Set up mongo db
* Complete tests
* Comment all code
* Add details to ReadMe
