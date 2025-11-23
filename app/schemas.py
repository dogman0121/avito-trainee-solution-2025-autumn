from marshmallow import Schema, fields

from app.models import PULLREQUEST_STATUS


class TeamMemberSchema(Schema):
    user_id = fields.String()
    username = fields.String()
    is_active = fields.Boolean()

class TeamSchema(Schema):
    team_name = fields.String()
    members = fields.List(fields.Nested(TeamMemberSchema))

class TeamCreateSchema(Schema):
    team_name = fields.String()
    members = fields.List(fields.Nested(TeamMemberSchema))

class UserSchema(Schema):
    user_id = fields.String()
    username = fields.String()
    is_active = fields.Boolean()
    team_name = fields.String()

class UserActivitySchema(Schema):
    user_id = fields.String()
    is_active = fields.Boolean()

class PullRequestCreateSchema(Schema):
    pull_request_id = fields.String()
    pull_request_name = fields.String()
    author_id = fields.String()

class PullRequestMergeSchema(Schema):
    pull_request_id = fields.String()

class PullRequestReassignSchema(Schema):
    pull_request_id = fields.String()
    old_reviewer_id = fields.String()

class PullRequestSchema(Schema):
    pull_request_id = fields.String()
    pull_request_name = fields.String()
    status = fields.Enum(PULLREQUEST_STATUS, by_value=True)
    author_id = fields.Method("get_author_id")
    assigned_reviewers = fields.Method("get_assigned_reviewers")

    def get_author_id(self, obj):
        return obj.author.user_id
    
    def get_assigned_reviewers(self, obj):
        return [i.user_id for i in obj.assigned_reviewers]

class PullRequestShortSchema(Schema):
    pass