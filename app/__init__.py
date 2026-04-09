from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    migrate.init_app(app,db)

    from app.routes import ALL_BLUEPRINTS
    from app import models

    for blueprint, prefixo in ALL_BLUEPRINTS:
        app.register_blueprint(blueprint=blueprint, url_prefix=prefixo)
        
    return app



