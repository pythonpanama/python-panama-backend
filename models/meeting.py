from sqlalchemy import desc
from typing import List

from db import db
from models.model_mixin import ModelMixin


class MeetingModel(db.Model, ModelMixin):
    __tablename__ = "meetings"

    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(20), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    creator_id = db.Column(
        db.Integer, db.ForeignKey("members.id"), nullable=False
    )
    creator = db.relationship("MemberModel")

    @classmethod
    def find_all(cls) -> List["MeetingModel"]:
        return cls.query.order_by(desc(cls.datetime)).all()

    @classmethod
    def find_by_creator_id(cls, creator_id: int) -> List["MeetingModel"]:
        return (
            cls.query.filter_by(creator_id=creator_id)
            .order_by(desc(cls.datetime))
            .all()
        )

    @classmethod
    def find_by_id(cls, id: int) -> "MeetingModel":
        return cls.query.filter_by(id=id).first()
