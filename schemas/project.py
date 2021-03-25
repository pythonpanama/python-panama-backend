from ma import ma

from models.project import ProjectModel


class ProjectSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ProjectModel
        load_only = ("admin",)
        dump_only = ("id",)
        include_fk = True
        load_instance = True
