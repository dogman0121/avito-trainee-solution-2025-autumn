from app.entities import Team, User, PullRequest
from app.exceptions import (
    TeamAlreadyExistsException, 
    TeamNotFoundException, 
    UserNotFoundException, 
    PullRequestNotFound, 
    PullRequestAlreadyExists,
    PullRequestMergedException,
    PullRequestUserNotReviewerException
)
from app.repositories import TeamRepository, UserRepository, PullRequestsRepository
from app.models import PULLREQUEST_STATUS


class TeamService:
    def create_team(self, team: Team):
        team_repository = TeamRepository()
        if team_repository.get_by_name(team.team_name):
            raise TeamAlreadyExistsException
        
        created_team = team_repository.create(team)

        return created_team
    
    def get_team(self, team_name: str):
        team = TeamRepository().get_by_name(team_name)

        if team is None:
            raise TeamNotFoundException
        
        return team

class UserService:
    def set_is_active(self, user: User, is_active: bool):
        user = UserRepository().set_is_active(user, is_active)

        return user

    def get_user_by_id(self, user_id: str):
        user = UserRepository().get_by_id(user_id)

        if user is None:
            raise UserNotFoundException
        return user

class PullRequestService:
    def create_pull_request(self, pull_request: PullRequest):
        if PullRequestsRepository().get_by_id(pull_request.pull_request_id):
            raise PullRequestAlreadyExists
        
        created_pull_request = PullRequestsRepository().create(pull_request)

        return created_pull_request

    def get_pull_request_by_id(self, pull_request_id: str):
        pull_request = PullRequestsRepository().get_by_id(pull_request_id)

        if pull_request is None:
            raise PullRequestNotFound
        
        return pull_request
    
    def get_user_pull_requests(self, user: User):
        pull_requests = PullRequestsRepository().get_by_user(user)

        return pull_requests

    def merge_pull_request(self, pull_request: PullRequest):
        merged_pull_request = PullRequestsRepository().merge(pull_request)

        return merged_pull_request

    def reassign_pull_request_reviewer(self, pull_request: PullRequest, old_reviewer: User):
        if pull_request.status == PULLREQUEST_STATUS.MERGED:
            raise PullRequestMergedException
        if old_reviewer not in pull_request.assigned_reviewers:
            raise PullRequestUserNotReviewerException
        reassigned_pull_request = PullRequestsRepository().reassign_reviewer(pull_request, old_reviewer)

        return reassigned_pull_request