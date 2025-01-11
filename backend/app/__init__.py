from flask import Flask
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app import db
    db.init_app(app)

    from app.api import bp as api_bp
    app.register_blueprint(api_bp)

    return app

app = create_app()

from app import routes