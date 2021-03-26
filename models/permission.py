from typing import List

from db import db
from models.model_mixin import ModelMixin


class PermissionModel(db.Model, ModelMixin):
    __tablename__ = "permissions"

    id = db.Column(db.Integer, primary_key=True)
    permission_name = db.Column(db.String(50), nullable=False, unique=True)

    @classmethod
    def find_all(cls) -> List["PermissionModel"]:
        return cls.query.order_by(cls.permission_name).all()

    @classmethod
    def find_by_id(cls, id: int) -> "PermissionModel":
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, permission_name: str) -> "PermissionModel":
        return cls.query.filter_by(permission_name=permission_name).first()
