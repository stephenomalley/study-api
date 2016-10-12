from studies_api.resources.api.v1.exceptions.submission import SubmissionLimitExceeded, StudyNotCreated
from bson.objectid import ObjectId
from studies_api import db


def get_all_submissions():
    """
    Retrieves all the submission objects within the collection

    :return: a list of dictionaries [empty dictionary if no data in that collections
    """

    return db.submissions.find()


def get_submission_by_id(id):
    """
    A submission is returned based on the id provided.

    If the id does not match the standards of a MongoDb
    objectId then an InvalidId error will be thrown

    :param id: id representing the object _id of the collection.
    :return: a dictionary
    :exception bson.Errors.InvalidId
    """
    return db.submissions.find_one({"_id": ObjectId(id)})

def save_submission(submission):
    """
    Takes a dictionary representing a submission document and persists the data to the submissions collection in the
    database

    :param study: dictionary containing the object data to be saved
    :return: the persisted object with ObjectId
    @:exception SubmissionLimitExceeded if there are no places available on the study
    """
    if check_submissions(submission["study"]):
        id = db.submissions.insert(submission)
        submission.update({"_id": id})
        return submission

    raise SubmissionLimitExceeded("All places on study are filled")



def check_submissions(study_id):
    """
    Check that a study exists and if it does check that there are places available on the study
    :param study_id:
    :return: boolean which denotes whether a place on the study is available
    :exception StudyNotCreated if the study can't be found
    """
    study = db.studies.find_one({"_id": ObjectId(study_id)})
    if study:
        existing_submissions = db.submissions.count({"study": study_id})
        return existing_submissions < study["available_places"]

    raise StudyNotCreated("Study {0} does not exist. Please check submission is for this study".format(study_id))




