class TeamAlreadyExistsException(Exception):
    pass

class TeamNotFoundException(Exception):
    pass

class UserNotFoundException(Exception):
    pass

class PullRequestAlreadyExists(Exception):
    pass

class PullRequestNotFound(Exception):
    pass

class PullRequestNoCandidatesException(Exception):
    pass

class PullRequestMergedException(Exception):
    pass

class PullRequestUserNotReviewerException(Exception):
    pass