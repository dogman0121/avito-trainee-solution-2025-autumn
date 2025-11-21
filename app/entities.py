from dataclasses import dataclass
from typing import List
from datetime import datetime

from app.models import PULLREQUEST_STATUS

@dataclass
class User:
    user_id: str
    username: str
    is_active: bool

@dataclass
class Team:
    team_name: str
    members: List[User]

@dataclass
class PullRequest:
    pull_request_id: str
    pull_request_name: str
    status: PULLREQUEST_STATUS
    author: User
    assigned_reviewers: List[User]
    created_at: datetime
    merged_at: datetime