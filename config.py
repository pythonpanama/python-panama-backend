import os

from datetime import timedelta


class Config:
    SECRET_KEY = os.urandom(32)
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or os.urandom(32)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("SQLALCHEMY_DATABASE_URI")
        or "postgresql://ppty:pass@localhost:5432/ppty_dev"
    )
    PROPAGATE_EXCEPTIONS = os.environ.get("PROPAGATE_EXCEPTIONS") or True
    POPULATE_DB = os.environ.get("POPULATE_DB") or True
    TESTING = os.environ.get("TESTING") or False
    DEBUG = os.environ.get("DEBUG") or True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "postgresql://ppty:pass@localhost:5432/ppty_test"


class ProductionConfig(Config):
    pass


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
