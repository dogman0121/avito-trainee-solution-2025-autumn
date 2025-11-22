from app import db
from app.models import TeamModel, UserModel
from app.entities import Team, User
from app.exceptions import TeamAlreadyExistsException

from typing import Optional

class TeamRepository:
    def convert_to_entity(self, team: Optional[TeamModel]):
        if team is None:
            return None
        
        members = [UserRepository().convert_to_entity(i) for i in team.members]

        return Team(
            team_name=team.team_name,
            members=members
        )

    def get_team_by_name(self, name: str):
        team_model = TeamModel.query.filter_by(team_name=name).scalar()

        return self.convert_to_entity(team_model)
    
    def create_team(self, team: Team):
        members = []

        for m in team.members:
            member = UserModel(
                user_id=m.user_id,
                username=m.username,
                is_active=m.is_active
            )
            member.append(member)

        team_model = TeamModel(
            team_name=team.team_name,
            members=members
        )

        db.session.add(team_model)
        db.session.commit()

        return self.convert_to_entity(team_model)

class UserRepository:
    def convert_to_entity(self, user: UserModel):
        return User(
            user_id=user.user_id,
            username=user.username,
            is_active=user.is_active
        )

class PullRequestsRepository:
    pass