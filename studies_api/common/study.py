from studies_api.app import db


def get_all_studies():
    """
    Retrieves all the study objects within the collection
    :return: a list of dictionaries [empty dictionary if no data in that collections
    """
    return db.studies.find()


def get_study_by_id(id):
    """
    A study is returned based on the id provided
    :param id: id representing the object _id of the collection
    :return: a dictionary
    """
    return db.study.find({"_id": id})
