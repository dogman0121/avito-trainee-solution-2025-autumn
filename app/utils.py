from flask import jsonify

def create_not_found_response():
    response =  jsonify({
        "error":{
            "code": "NOT_FOUND",
            "message": "resource not found"
        }
    })

    response.status_code = 404

    return response

def create_team_exists_response():
    response = jsonify({
        "error": {
            "code": "TEAM_EXISTS",
            "message": "team_name already exists"
        }
    })

    response.status_code = 400

    return response

def create_pr_exists_response():
    response = jsonify({
        "error": {
            "code": "PR_EXISTS",
            "message": "PR id already exists"
        }
    })

    response.status_code = 409

    return response

def create_pr_no_candidates_response():
    response = jsonify({
        "error": {
            "code": "NO_CANDIDATE",
            "message": "no active replacement candidate in team"
        }
    })

    response.status_code = 409

    return response

def create_pr_merged_response():
    response =  jsonify({
        "error": {
            "code": "PR_MERGED",
            "message": "cannot reassign on merged PR"
        }
    })

    response.status_code = 409

    return response

def create_pr_user_not_reviewer_response():
    response = jsonify({
        "error": {
            "code": "NOT_ASSIGNED",
            "message": "reviewer is not assigned to this PR"
        }
    })

    response.status_code = 409

    return response