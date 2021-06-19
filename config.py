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

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    PROPAGATE_EXCEPTIONS = True


class TestingConfig(Config):
    DEBUG = False
    TESTING = True
    PROPAGATE_EXCEPTIONS = True
    SQLALCHEMY_DATABASE_URI = "postgresql://ppty:pass@localhost:5432/ppty_test"


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    PROPAGATE_EXCEPTIONS = False


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
