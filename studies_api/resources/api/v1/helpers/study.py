from bson.objectid import ObjectId
from studies_api import db


def get_all_studies():
    """
    Retrieves all the study objects within the collection

    :return: a list of dictionaries [empty dictionary if no data in that collections
    """
    return db.studies.find()


def get_study_by_id(id):
    """
    A study is returned based on the id provided.

    If the id does not match the standards of a MongoDb
    objectId then an InvalidId error will be thrown

    :param id: id representing the object _id of the collection.
    :return: a dictionary
    :exception bson.Errors.InvalidId
    """
    return db.studies.find_one({"_id": ObjectId(id)})

def save_study(study):
    """
    Takes a dictionary representing a study document and persists the data to the studies collection in the
    database

    :param study: dictionary containing the object data to be saved
    :return: the persisted object with ObjectId
    """

    id = db.studies.insert(study)
    study.update({"_id": id})
    return study

