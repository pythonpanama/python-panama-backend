from sqlalchemy import desc
from typing import List

from db import db
from models.meeting import MeetingModel
from models.model_mixin import ModelMixin
from models.speaker import SpeakerModel


class KeynoteModel(db.Model, ModelMixin):
    __tablename__ = "keynotes"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    speaker_id = db.Column(
        db.Integer, db.ForeignKey("speakers.id"), nullable=False
    )
    meeting_id = db.Column(
        db.Integer, db.ForeignKey("meetings.id"), nullable=False
    )
    speaker = db.relationship("SpeakerModel")
    meeting = db.relationship("MeetingModel")

    @classmethod
    def find_all(cls) -> List["KeynoteModel"]:
        return cls.query.order_by(desc(cls.meeting_id), cls.id).all()

    @classmethod
    def find_by_id(cls, id: int) -> "KeynoteModel":
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_meeting_id(cls, meeting_id: int) -> List["KeynoteModel"]:
        return (
            cls.query.filter_by(meeting_id=meeting_id).order_by(cls.id).all()
        )

    @classmethod
    def find_by_speaker_id(cls, speaker_id: int) -> List["KeynoteModel"]:
        return (
            cls.query.filter_by(speaker_id=speaker_id)
            .order_by(desc(cls.meeting_id), cls.id)
            .all()
        )
