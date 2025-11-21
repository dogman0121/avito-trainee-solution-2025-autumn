from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.routes import bp

db = SQLAlchemy()

def create_app(config):
    app = Flask(__name__)

    db.init_app(app)

    app.register_blueprint(bp)

    return app