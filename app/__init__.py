from flask import Flask
from .routes import bp
from .indexer import build_index
from .config import SECRET_KEY

def create_app():
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.secret_key = SECRET_KEY
    build_index()
    app.register_blueprint(bp)
    return app
