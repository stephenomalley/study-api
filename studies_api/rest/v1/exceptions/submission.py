class SubmissionLimitExceeded(Exception):
    """
    Exception thrown when the maximum number of places on a study already exists.
    """
    pass


class StudyNotCreated(Exception):
    """
    Exception type thrown when an attempt to create a submission with an invalid study id is made.
    """
    pass
