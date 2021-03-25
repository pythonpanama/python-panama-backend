from typing import List

from db import db
from models.model_mixin import ModelMixin

projects_members = db.Table(
    "projects_members ",
    db.Column(
        "project_id", db.Integer, db.ForeignKey("projects.id"), nullable=False
    ),
    db.Column(
        "member_id", db.Integer, db.ForeignKey("members.id"), nullable=False
    ),
    db.PrimaryKeyConstraint("project_id", "member_id"),
)


class ProjectModel(db.Model, ModelMixin):
    __tablename__ = "projects"

    id = db.Column(db.Integer, primary_key=True)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    goals = db.Column(db.String(500), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    admin_id = db.Column(
        db.Integer, db.ForeignKey("members.id"), nullable=False
    )

    @classmethod
    def find_all(cls) -> List["ProjectModel"]:
        return cls.query.order_by(cls.admin_id, cls.start_date).all()

    @classmethod
    def find_by_admin_id(cls, admin_id: int) -> List["ProjectModel"]:
        return (
            cls.query.filter_by(admin_id=admin_id)
            .order_by(cls.start_date)
            .all()
        )

    @classmethod
    def find_by_id(cls, id: int) -> "ProjectModel":
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_status(cls, status: str) -> List["ProjectModel"]:
        return (
            cls.query.filter_by(status=status)
            .order_by(cls.admin_id, cls.start_date)
            .all()
        )
