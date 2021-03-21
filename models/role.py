from db import db
from models.model_mixin import ModelMixin

roles_permissions = db.Table(
    "roles_permissions",
    db.Column(
        "role_id", db.Integer, db.ForeignKey("roles.id"), nullable=False
    ),
    db.Column(
        "permission_id",
        db.Integer,
        db.ForeignKey("permissions.id"),
        nullable=False,
    ),
    db.PrimaryKeyConstraint("role_id", "permission_id"),
)


class RoleModel(db.Model, ModelMixin):
    __tablename__ = "roles"

    id = db.Column(db.Integer, primary_key=True)
    role_name = db.Column(db.String(20), unique=True, nullable=False)
    members = db.relationship("MemberModel", lazy="dynamic")
    permissions = db.relationship(
        "PermissionModel",
        secondary="roles_permissions",
        lazy="dynamic",
        backref=db.backref("roles", lazy="dynamic"),
    )

    @classmethod
    def find_by_id(cls, id: int) -> "RoleModel":
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, role_name: str) -> "RoleModel":
        return cls.query.filter_by(role_name=role_name).first()
