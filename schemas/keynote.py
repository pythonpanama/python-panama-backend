from ma import ma

from models.keynote import KeynoteModel


class KeynoteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = KeynoteModel
        load_only = ("speaker", "meeting")
        dump_only = ("id",)
        include_fk = True
        load_instance = True
