from typing import Dict, List, Union

from db import db
from .model_mixin import ModelMixin
from resources.message import MEMBER_LOGOUT, MEMBER_400


class TokenModel(db.Model, ModelMixin):
    __tablename__ = "tokens"

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False)
    token_type = db.Column(db.String(10), nullable=False)
    revoked = db.Column(db.Boolean, nullable=False)
    expires = db.Column(db.DateTime, nullable=False)
    member_id = db.Column(
        db.Integer, db.ForeignKey("members.id"), nullable=False
    )
    member = db.relationship("MemberModel")

    def __init__(self, **kwargs):
        super(TokenModel, self).__init__(**kwargs)

    @classmethod
    def find_by_member_id(cls, member_id: int) -> List["TokenModel"]:
        return (
            cls.query.filter_by(member_id=member_id)
            .order_by(cls.token_type)
            .all()
        )

    @classmethod
    def revoke(
        cls, member_id: int, token_type: str = None
    ) -> Dict[str, Union[str, int]]:
        if token_type:
            tokens = cls.query.filter_by(
                member_id=member_id, revoked=False, token_type=token_type
            ).all()
        else:
            tokens = cls.query.filter_by(
                member_id=member_id, revoked=False
            ).all()

        if len(tokens) == 0:
            return {"message": MEMBER_400, "status": 400}

        for token in tokens:
            token.revoked = True
            token.save_to_db()

        return {"message": MEMBER_LOGOUT, "status": 200}
