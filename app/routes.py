from flask import Blueprint

bp = Blueprint("main", __name__)


@bp.route("/team/add", methods=["POST"])
def create_team_route():
    pass


@bp.route("/team/get", methods=["GET"])
def get_team_route():
    pass


@bp.route("/users/setIsActive", methods=["POST"])
def set_user_active_route():
    pass

@bp.route("/users/getReview", methods=["GET"])
def get_user_reviews_route():
    pass


@bp.route("/pullRequests/create", methods=["POST"])
def create_pull_request_route():
    pass

@bp.route("/pullRequests/metge", methods=["POST"])
def merge_pull_requests_route():
    pass

@bp.route("/pullRequests/reassign", methods=["POST"])
def reassign_pull_requests_route():
    pass

@bp.route("/stats", methods=["GET"])
def get_stats_route():
    pass