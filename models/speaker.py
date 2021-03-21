from typing import List

from db import db
from models.model_mixin import ModelMixin


class SpeakerModel(db.Model, ModelMixin):
    __tablename__ = "speakers"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    linkedin_profile = db.Column(db.String(75))
    github_profile = db.Column(db.String(75))
    twitter_profile = db.Column(db.String(75))
    bio = db.Column(db.String(500), nullable=False)
    profile_picture = db.Column(db.String(150))
    keynotes = db.relationship("KeynoteModel", lazy="dynamic")

    @classmethod
    def find_all(cls) -> List["SpeakerModel"]:
        return cls.query.order_by(cls.first_name, cls.last_name).all()

    @classmethod
    def find_by_id(cls, id: int) -> "SpeakerModel":
        return cls.query.filter_by(id=id).first()
