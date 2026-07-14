from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .routes import main

db = SQLAlchemy()

def create_app():
    app = Flask(__name__,
                template_folder='../templates',
                static_folder='../static')
    app.config.from_object('config.Config')

    db.init_app(app)

    with app.app_context():
        from . import models
        db.create_all()

    app.register_blueprint(main)

    return app