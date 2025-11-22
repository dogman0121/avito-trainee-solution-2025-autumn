from marshmallow import Schema, fields


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
    pass

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
    pass

class PullRequestShortSchema(Schema):
    pass