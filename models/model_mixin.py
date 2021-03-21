from flask import abort
from sqlalchemy import exc

from db import db


# noinspection PyAttributeOutsideInit
class ModelMixin:
    def activate(self) -> db.Model:
        """Make a record active"""
        self.is_active = True
        return self.save_to_db()

    def deactivate(self) -> db.Model:
        """Make a record inactive"""
        self.is_active = False
        return self.save_to_db()

    def delete_from_db(self) -> None:
        """Delete a record"""
        try:
            db.session.delete(self)
            db.session.commit()
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            abort(500, description=e)

    def save_to_db(self) -> db.Model:
        """Save a record"""
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except exc.SQLAlchemyError as e:
            db.session.rollback()
            abort(500, description=e)
