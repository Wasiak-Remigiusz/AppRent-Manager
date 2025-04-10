import os

from dotenv import load_dotenv
from flask import Flask, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy

import models
from blueprints.admin import admin as AdminBlueprint
from blueprints.apartment_manager import apartment_manager as ApartmentManagerBlueprint
from blueprints.auth import auth as AuthBlueprint
from blueprints.dash import dash as DashboardBlueprint
from blueprints.main import main as MainBlueprint
from db import db


def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()
    

    app.config.from_pyfile('config.cfg')
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['KIT_FONTAWESOME'] = os.getenv('KIT_FONTAWESOME')
    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(MainBlueprint)
    app.register_blueprint(AdminBlueprint)
    app.register_blueprint(AuthBlueprint)
    app.register_blueprint(DashboardBlueprint)
    app.register_blueprint(ApartmentManagerBlueprint)


    return app


# if __name__ == '__main__':
#     app.run()