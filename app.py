from flask import Flask, jsonify
from marshmallow import ValidationError

from config import config
from db import db
from ma import ma

from resources.keynote import keynotes
from resources.meeting import meetings
from resources.permission import permissions
from resources.role import roles


def create_app(config_name: str = "development") -> Flask:
    """
    Factory for the creation of a Flask app.
    :param config_name: the key for the config setting to use
    :type config_name: str
    :return: app: a Flask app instance
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    db.init_app(app)
    ma.init_app(app)

    @app.errorhandler(ValidationError)
    def handle_marshmallow_validation_error(err):
        return jsonify(error=str(err)), 400

    @app.errorhandler(404)
    def resource_not_found(err):
        return jsonify(error=str(err)), 404

    @app.errorhandler(409)
    def resource_not_found(err):
        return jsonify(error=str(err)), 409

    app.register_blueprint(keynotes, url_prefix="/keynotes")
    app.register_blueprint(meetings, url_prefix="/meetings")
    app.register_blueprint(permissions, url_prefix="/permissions")
    app.register_blueprint(roles, url_prefix="/roles")

    return app
