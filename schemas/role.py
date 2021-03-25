from ma import ma

from models.role import RoleModel
from schemas.permission import PermissionSchema
from schemas.member import MemberSchema


class RoleSchema(ma.SQLAlchemyAutoSchema):
    permissions = ma.Nested(PermissionSchema, many=True)
    members = ma.Nested(MemberSchema, many=True)

    class Meta:
        model = RoleModel
        dump_only = ("id",)
        include_fk = True
        load_instance = True
