# study-api

Simple Flask app that makes use of the Flask-Restful frame work and pymongo 
to query the database.

## Run instructions
Set env variable `MONGOHQ_URL=<mongo-db-connection>`
then run `python runserver.py`

## TroubleShooting

Any issues connecting to the database then make sure the mongod
process is up and running and you are pointing to the correct database



## Study end-points

 Method | URI | Data | HTTP Code | Response (in JSON) |
| ------ | --- | ---- | --------- | ------------------ |
| GET  | /api/v1/studies/id |  | 200 | {"id": 1,"name": "test", "user":1} |
| GET  | api/v1/studies/   |  | 200 | ["data": [{"id": 1,"name": "test", "user":1}, "links": {self: "path/studies"}] |


## Submission end-points


##TODO
* Add post for study
* Add get, list, post for submission
* Add filter params on some urls
* Order project correctly
* set up mongo db
