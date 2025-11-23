from app import db
from app.models import TeamModel, UserModel, PullRequestModel, assigned_users_table, PULLREQUEST_STATUS
from app.entities import Team, User, PullRequest
from app.exceptions import PullRequestNoCandidatesException

from typing import Optional
from datetime import datetime
from sqlalchemy import update


class TeamRepository:
    def convert_to_entity(self, team: Optional[TeamModel]):
        if team is None:
            return None
        
        members = [UserRepository().convert_to_entity(i) for i in team.members]

        return Team(
            team_name=team.team_name,
            members=members
        )

    def get_by_name(self, name: str):
        team_model = TeamModel.query.filter_by(team_name=name).scalar()

        return self.convert_to_entity(team_model)
    
    def create(self, team: Team):
        members = []

        for m in team.members:
            member = UserModel(
                user_id=m.user_id,
                username=m.username,
                is_active=m.is_active
            )
            members.append(member)

        team_model = TeamModel(
            team_name=team.team_name,
            members=members
        )

        db.session.add(team_model)

        team_model.members = members

        db.session.commit()

        return self.convert_to_entity(team_model)

class UserRepository:
    def convert_to_entity(self, user: Optional[UserModel]):
        if user is None:
            return None
        
        return User(
            user_id=user.user_id,
            username=user.username,
            is_active=user.is_active
        )
    
    def set_is_active(self, user: User, is_active: bool):
        UserModel.query.update({"is_active": is_active})

        db.session.commit()

        user.is_active = is_active

        return user
    
    def get_by_id(self, user_id: str):
        user_model = UserModel.query.filter_by(user_id=user_id).scalar()

        return self.convert_to_entity(user_model)

class PullRequestsRepository:
    def convert_to_entity(self, pull_request_model: Optional[PullRequestModel]):
        if pull_request_model is None:
            return None
        
        reviewers = []

        for i in pull_request_model.assigned_reviewers:
            reviewers.append(UserRepository().convert_to_entity(i))

        author = UserRepository().convert_to_entity(pull_request_model.author)

        return PullRequest(
            pull_request_id=pull_request_model.pull_request_id,
            pull_request_name=pull_request_model.pull_request_name,
            status=pull_request_model.status,
            author=author,
            assigned_reviewers=reviewers,
            created_at=pull_request_model.created_at,
            merged_at=pull_request_model.merged_at
        )

    def create(self, pull_request: PullRequest):
        reviewers = UserModel.query.filter(UserModel.is_active==True, UserModel.user_id!=pull_request.author.user_id).limit(2).all()
        
        pull_request_model = PullRequestModel(
            pull_request_id=pull_request.pull_request_id,
            pull_request_name=pull_request.pull_request_name,
            author_id=pull_request.author.user_id,
            status=PULLREQUEST_STATUS.OPEN,
            created_at=pull_request.created_at,
            assigned_reviewers=reviewers
        )

        db.session.add(pull_request_model)

        db.session.commit()

        return self.convert_to_entity(pull_request_model)

    def get_by_user(self, user: User):
        pull_request_models = PullRequestModel.query.join(
            assigned_users_table, 
            assigned_users_table.c.pull_request_id == PullRequestModel.pull_request_id
        ).filter(assigned_users_table.c.user_id==user.user_id).all()

        return [self.convert_to_entity(pr) for pr in pull_request_models]

    def get_by_id(self, pull_request_id: str):
        pull_request = PullRequestModel.query.filter_by(pull_request_id=pull_request_id).scalar()

        return self.convert_to_entity(pull_request)

    def merge(self, pull_request: PullRequest):
        timestamp = datetime.now()

        PullRequestModel.query.filter_by(pull_request_id=pull_request.pull_request_id).update({
                "status": PULLREQUEST_STATUS.MERGED,
                "merged_at": timestamp
            }
        )

        db.session.commit()

        pull_request.status = PULLREQUEST_STATUS.MERGED
        pull_request.merged_at = timestamp

        return pull_request

    def reassign_reviewer(self, pull_request: PullRequest, old_reviewer: User):
        new_reviewer = UserModel.query.except_(
            UserModel.query.join(
                assigned_users_table, 
                assigned_users_table.c.user_id==UserModel.user_id
            ).filter(
                UserModel.is_active==True,
                assigned_users_table.c.pull_request_id==pull_request.pull_request_id
            )
        ).filter(UserModel.user_id!=pull_request.author.user_id,).limit(1).first()

        if new_reviewer is None:
            raise PullRequestNoCandidatesException
        
        db.session.execute(update(assigned_users_table).filter(
            assigned_users_table.c.pull_request_id==pull_request.pull_request_id,
            assigned_users_table.c.user_id==old_reviewer.user_id
        ).values(user_id=new_reviewer.user_id))

        reviewers = []
        for r in pull_request.assigned_reviewers:
            if r.user_id != old_reviewer.user_id:
                reviewers.append(r)

        reviewers = [UserRepository().convert_to_entity(new_reviewer)]

        pull_request.assigned_reviewers = reviewers

        return pull_request

