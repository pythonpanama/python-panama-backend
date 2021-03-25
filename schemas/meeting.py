from ma import ma

from models.meeting import MeetingModel


class MeetingSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = MeetingModel
        load_only = ("creator",)
        dump_only = ("id",)
        include_fk = True
        load_instance = True
