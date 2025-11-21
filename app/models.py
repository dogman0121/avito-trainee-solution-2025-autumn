from app import db

from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import ENUM
from datetime import datetime
import enum

class PULLREQUEST_STATUS(enum.Enum):
    MERGED = "MERGED"
    OPEN = "OPEN"

class User(db.Model):
    __tablename__ = "users"

    user_id: Mapped[str] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column()
    team_name: Mapped[str] = mapped_column(ForeignKey("teams.team_name"))

    team: Mapped["Team"] = relationship(back_populates="members")

class Team(db.Model):
    __tablename__ = "teams"

    team_name: Mapped[str] = mapped_column(primary_key=True)

    members: Mapped["User"] = relationship(back_populates="team")

assigned_users_table = Table(
    "assigned_users",
    db.metadata,
    Column("user_id", ForeignKey("users.user_id")),
    Column("pull_request_id", ForeignKey("pull_requests.pull_request_id"))
)

class PullRequest(db.Model):
    __tablename__ = "pull_requests"

    pull_request_id: Mapped[str] = mapped_column(primary_key=True)
    pull_request_name: Mapped[str] = mapped_column() 
    author_id: Mapped[str] = mapped_column(ForeignKey("users.user_id"))
    status: Mapped[PULLREQUEST_STATUS] = mapped_column(
        ENUM(PULLREQUEST_STATUS, name="list_visibility", create_type=False), 
        default=PULLREQUEST_STATUS.OPEN
    )
    created_at: Mapped[datetime] = mapped_column(default=lambda x: datetime.now())
    merged_at: Mapped[datetime] = mapped_column()

    assigned_users: Mapped["User"] = relationship(secondary=assigned_users_table)



