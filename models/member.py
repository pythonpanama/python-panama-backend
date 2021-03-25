from typing import List

from werkzeug.security import check_password_hash, generate_password_hash

from db import db
from models.model_mixin import ModelMixin


class MemberModel(db.Model, ModelMixin):
    __tablename__ = "members"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(94), nullable=False)
    mobile_phone = db.Column(db.String(15))
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    linkedin_profile = db.Column(db.String(75))
    github_profile = db.Column(db.String(75))
    twitter_profile = db.Column(db.String(75))
    profile_picture = db.Column(db.String(150))
    is_active = db.Column(db.Boolean, default=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), nullable=False)
    role = db.relationship("RoleModel")
    # tokens = db.relationship("TokenModel", lazy="dynamic")
    projects = db.relationship("ProjectModel", lazy="dynamic")

    @classmethod
    def find_all(cls) -> List["MemberModel"]:
        return cls.query.order_by(cls.first_name, cls.last_name).all()

    @classmethod
    def find_by_email(cls, email: str) -> "MemberModel":
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, id: int) -> "MemberModel":
        return cls.query.filter_by(id=id).first()

    def get_permissions(self) -> List[str]:
        return [
            permission.permission_name for permission in self.role.permissions
        ]

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute")

    @password.setter
    def password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)
