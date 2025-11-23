from flask import Blueprint, request, jsonify

from datetime import datetime

from app.schemas import (
    TeamSchema, 
    TeamCreateSchema,
    UserActivitySchema, 
    UserSchema, 
    PullRequestShortSchema,
    PullRequestCreateSchema,
    PullRequestSchema,
    PullRequestMergeSchema,
    PullRequestReassignSchema
)
from app.entities import Team, User, PullRequest
from app.services import TeamService, UserService, PullRequestService
from app.exceptions import (
    TeamNotFoundException, 
    UserNotFoundException, 
    PullRequestAlreadyExists,
    PullRequestNotFound,
    PullRequestMergedException,
    PullRequestNoCandidatesException,
    PullRequestUserNotReviewerException,
    TeamAlreadyExistsException
)
from app.utils import (
    create_not_found_response, 
    create_pr_exists_response,
    create_pr_merged_response,
    create_pr_no_candidates_response,
    create_pr_user_not_reviewer_response,
    create_team_exists_response
)
from app.models import PULLREQUEST_STATUS

bp = Blueprint("main", __name__)

@bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'ok'}), 200

@bp.route("/team/add", methods=["POST"])
def create_team_route():
    try:
        create_schema = TeamCreateSchema()

        create_data = create_schema.load(request.json)

        team_members = []

        for i in create_data.get("members"):
            member = User(
                user_id=i.get("user_id"),
                username=i.get("username"),
                is_active=i.get("is_active")
            )

            team_members.append(member)

        team_data = Team(
            team_name=create_data.get("team_name"),
            members=team_members
        )

        team = TeamService().create_team(team_data)

        get_schema = TeamSchema()

        return jsonify({
            "team": get_schema.dump(team)
        }), 201
    except TeamAlreadyExistsException:
        return create_team_exists_response()

@bp.route("/team/get", methods=["GET"])
def get_team_route():
    try:
        team_name = request.args.get("team_name")

        team = TeamService().get_team(team_name)

        get_schema = TeamSchema()

        return jsonify({
            "team": get_schema.dump(team)
        })
    except TeamNotFoundException:
        return create_not_found_response()


@bp.route("/users/setIsActive", methods=["POST"])
def set_user_active_route():
    try:
        user_activity_schema = UserActivitySchema()

        user_activity_data = user_activity_schema.load(request.json)

        user_id = user_activity_data.get("user_id")
        activity = user_activity_data.get("is_active")

        user = UserService().get_user_by_id(user_id)

        updated_user = UserService().set_is_active(user, activity)

        get_schema = UserSchema()

        return jsonify({
            "user": get_schema.dump(updated_user)
        })
    except UserNotFoundException:
        return create_not_found_response()


@bp.route("/users/getReview", methods=["GET"])
def get_user_reviews_route():
    try:
        user_id = request.args.get("user_id")

        user = UserService().get_user_by_id(user_id)

        pull_requests = PullRequestService().get_user_pull_requests(user)

        get_pull_requests_schema = PullRequestShortSchema()

        return jsonify({
            "user_id": user.user_id,
            "pull_requests": get_pull_requests_schema.dump(pull_requests, many=True) 
        })
    except UserNotFoundException:
        return create_not_found_response()


@bp.route("/pullRequest/create", methods=["POST"])
def create_pull_request_route():
    try:
        create_schema = PullRequestCreateSchema()

        create_data = create_schema.load(request.json)

        author = UserService().get_user_by_id(create_data.get("author_id"))

        pull_request_id = create_data.get("pull_request_id")
        pull_request_name = create_data.get("pull_request_name")

        pull_request_data = PullRequest(
            pull_request_id=pull_request_id,
            pull_request_name=pull_request_name,
            author=author,
            status=PULLREQUEST_STATUS.OPEN,
            created_at=datetime.now(),
            assigned_reviewers=[],
            merged_at=None
        )

        pull_request = PullRequestService().create_pull_request(pull_request_data)

        get_schema = PullRequestSchema()

        return jsonify({
            "pr": get_schema.dump(pull_request)
        })
    except UserNotFoundException:
        return create_not_found_response()
    except PullRequestAlreadyExists:
        return create_pr_exists_response()
    

@bp.route("/pullRequest/merge", methods=["POST"])
def merge_pull_requests_route():
    try:
        pr_merge_schema = PullRequestMergeSchema()

        pr_merge_data = pr_merge_schema.load(request.json)

        pull_request_id = pr_merge_data.get("pull_request_id")

        pull_request = PullRequestService().get_pull_request_by_id(pull_request_id)

        updated_pull_request = PullRequestService().merge_pull_request(pull_request)

        get_schema = PullRequestSchema()

        return jsonify({
            "pr": get_schema.dump(updated_pull_request)
        })
    except PullRequestNotFound:
        return create_not_found_response()

@bp.route("/pullRequest/reassign", methods=["POST"])
def reassign_pull_requests_route():
    try:
        pr_reassign_schema = PullRequestReassignSchema()

        pr_reassign_data = pr_reassign_schema.load(request.json)

        old_reviewer_id = pr_reassign_data.get("old_reviewer_id")
        pull_request_id = pr_reassign_data.get("pull_request_id")

        old_reviewer = UserService().get_user_by_id(old_reviewer_id)

        pull_request = PullRequestService().get_pull_request_by_id(pull_request_id)

        updated_pr = PullRequestService().reassign_pull_request_reviewer(pull_request, old_reviewer)

        get_schema = PullRequestSchema()

        return jsonify({
            "pr": get_schema.dump(updated_pr),
            "replaced_by": old_reviewer_id
        })
    except PullRequestUserNotReviewerException:
        return create_pr_user_not_reviewer_response()
    except PullRequestNoCandidatesException:
        return create_pr_no_candidates_response()
    except PullRequestMergedException:
        return create_pr_merged_response()
    except UserNotFoundException:
        return create_not_found_response()
    except PullRequestNotFound:
        return create_not_found_response()

@bp.route("/stats", methods=["GET"])
def get_stats_route():
    pass