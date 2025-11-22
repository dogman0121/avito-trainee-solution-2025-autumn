from app.entities import Team, User, PullRequest
from app.exceptions import TeamAlreadyExistsException, TeamNotFoundException
from app.repositories import TeamRepository


class TeamService:
    def create_team(self, team: Team):
        team_repository = TeamRepository()
        if team_repository.get_team_by_name(team.team_name):
            raise TeamAlreadyExistsException
        
        team = team_repository.create_team(team)

        return team
    
    def get_team(self, team_name: str):
        team = TeamRepository().get_team_by_name(team_name)

        if team is None:
            raise TeamNotFoundException
        
        return team

class UserService:
    def set_is_active(self, user: User, is_active: bool):
        pass

    def get_user_by_id(self, user_id: str):
        pass

    def get_pull_requests(self, user: User):
        pass

class PullRequestService:
    def create_pull_request(pull_request: PullRequest):
        pass

    def get_pull_request_by_id(pull_request_id: str):
        pass

    def merge_pull_request(pull_request: PullRequest):
        pass

    def reassign_pull_request_reviewer(pull_request: PullRequest, old_reviewer: User):
        pass