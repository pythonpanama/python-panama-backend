from ma import ma

from models.member import MemberModel


class TokenSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MemberModel
        load_only = ("member",)
        dump_only = ("id",)
        include_fk = True
        load_instance = True
