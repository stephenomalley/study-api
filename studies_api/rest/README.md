# Resources

Resources are the main part of Flask Restful c.f `http://flask-restful-cn.readthedocs.io/en/0.3.4/api.html#flask_restful.Resource`

The resource files have been structured to follow a versioned API approach. So all resources for version one of the api can be found in `api/v1/`. 
All helpers and files used for a version of an api are contained within the same directory and none of the resources make use of functions outside of the directory.
This is to ensure that if another version of the api comes along then we are not going to override behaviour in `v1`.

There are currently Two resources one for Studies and one for Submissions. I've separated the functionality in different files so that if these were to become 
separate repositories further down the line then it would be easy to extract the data and do so.

##Version 1 (v1)

Version 1 of the api uses pymongo to connect to the mongo db from python. Since we are using a MonogDB with simple collections there is really no need for an ORM. 
As such there are no models created as the resource itself can handle the validation of the data, and retrieving\storing of json is all we are essentially doing at this stage.

### Study

There are two resources in `study.py` as per the standard for Flask ResftFul:
* one for the retrieval of an individual study
* one for the post and retrival of all the studies.

The former resource can be accessed by hitting the uri `/api/v1/studies/<id>` where id is the ObjectId of the Mongo Collection item. This endpoint supports no other http operations, only get.
For example, requesting `/api/v1/studies/57fe76babf97430003f0aad3` would return

```
{"name": "Wee name", "available_places": 2, "id": "57fe76babf97430003f0aad3", "user": "738u5939r30"}
```


The latter resource returns a list of all studies in the database via the uri `/api/v1/studies`. The result of hitting the endpoint would be something like:
```
{
    "data": [
        {
            "name": "Wee name", 
            "available_places": 2, 
            "id": "57fe76babf97430003f0aad3", 
            "user": "738u5939r30"
        }, 
        {
            "name": "Rachael", 
            "available_places": 20, 
            "id": "57fe77f9bf97430003f0aad4", 
            "user": "567fbh4892ndnjd"
        }
    ], 
    "links": {
        "self": "/api/v1/studies"
    }
}
```

Alternatively, there is an option to filter the studies by user by passing the user id as a request parameter:
`/api/v1/studies/?user=567fbh4892ndnjd`. This would return a list of studies that a user has created, for instance, using `user=567fbh4892ndnjd` would return
```
{
    "data": [
        {
            "name": "Rachael", 
            "available_places": 20, 
            "id": "57fe77f9bf97430003f0aad4", 
            "user": "567fbh4892ndnjd"
        }
    ], 
    "links": {
        "self": "/api/v1/studies"
    }
}
```

## Submission

### Outstanding work
* Need improve the error messages to include more detail, especially the error code, in the returned json
* List endpoints should be paginated and the links section of the response json should also show next and last urls
* All json returned should also have an includes part which gives details of related models. c.f `http://jsonapi.org/` or `http://swagger.io/`
* Use of the `RequestParser` flask module needs to be changed as there are better solutions to this out there.