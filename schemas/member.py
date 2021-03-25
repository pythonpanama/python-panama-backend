from typing import Dict

from marshmallow import pre_load
from werkzeug.security import generate_password_hash

from ma import ma
from models.member import MemberModel
from schemas.token import TokenSchema


class MemberSchema(ma.SQLAlchemyAutoSchema):
    tokens = ma.Nested(TokenSchema, many=True)

    @pre_load
    def set_password_hash(self, member_data: Dict, **kwargs) -> Dict:
        member_data["password_hash"] = generate_password_hash(
            member_data.pop("password")
        )
        return member_data

    class Meta:
        model = MemberModel
        load_only = ("password_hash", "role")
        dump_only = ("id",)
        include_fk = True
        load_instance = True
