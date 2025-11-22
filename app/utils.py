from flask import jsonify

def create_not_found_response():
    return jsonify({
        "error":{
            "code": "NOT_FOUND",
            "message": "resource not found"
        }
    })

def create_pr_exists_response():
    return jsonify({
        "error": {
            "code": "PR_EXISTS",
            "message": "PR id already exists"
        }
    })

def create_pr_no_candidates_response():
    return jsonify({
        "error": {
            "code": "NO_CANDIDATE",
            "message": "no active replacement candidate in team"
        }
    })

def create_pr_merged_response():
    return jsonify({
        "error": {
            "code": "PR_MERGED",
            "message": "cannot reassign on merged PR"
        }
    })

def create_pr_user_not_reviewer_response():
    return jsonify({
        "error": {
            "code": "NOT_ASSIGNED",
            "message": "reviewer is not assigned to this PR"
        }
    })