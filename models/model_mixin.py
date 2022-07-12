from flask import abort
from sqlalchemy import exc

from db import db


# noinspection PyAttributeOutsideInit
class ModelMixin:
    def delete_from_db(self) -> None:
        """Delete a record"""
        try:
            db.session.delete(self)
            db.session.commit()
        except exc.SQLAlchemyError as e:  # pragma: no cover
            db.session.rollback()
            abort(500, description=e)

    def save_to_db(self) -> db.Model:
        """Save a record"""
        try:
            db.session.add(self)
            db.session.commit()
            return self
        except exc.SQLAlchemyError as e:  # pragma: no cover
            db.session.rollback()
            abort(500, description=e)
            
