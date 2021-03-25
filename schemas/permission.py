from ma import ma

from models.permission import PermissionModel


class PermissionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = PermissionModel
        load_only = ("roles",)
        dump_only = ("id",)
        include_fk = True
        load_instance = True
