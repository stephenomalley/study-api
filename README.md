# study-api

Simple Flask app 

## Study end-points

 Method | URI | Data | HTTP Code | Response (in JSON) |
| ------ | --- | ---- | --------- | ------------------ |
| GET  | /studies/id |  | 200 | {"id": 1,"name": "test", "user":1} |
| GET  | /studies/   |  | 200 | ["data": [{"id": 1,"name": "test", "user":1}, "links": {self: "path/studies"}] |


## Submission end-points


##TODO
* Add post for study
* Add get, list, post for submission
* Add filter params on some urls
* Order project correctly
* set up mongo db
* create run script to launch app
