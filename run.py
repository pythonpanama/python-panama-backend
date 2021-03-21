import os

from app import create_app
from db import db

app = create_app(os.getenv("FLASK_CONFIG") or "development")


# noinspection PyArgumentList
@app.before_first_request
def create_tables() -> None:
    db.drop_all()
    db.create_all()


if __name__ == "__main__":
    app.run()
