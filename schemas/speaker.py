from ma import ma

from models.speaker import SpeakerModel


class SpeakerSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SpeakerModel
        dump_only = ("id",)
        include_fk = True
        load_instance = True
