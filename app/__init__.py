from flask import Flask, Blueprint

# Blueprints are probably a little overkill for this app, but adding this
# so that I can call register_blueprint() in create_app was the only way I
# could get the test_client fixture to work.
app_blueprint = Blueprint('app', __name__)

def create_app():
    app = Flask(__name__)
    app.register_blueprint(app_blueprint)
    return app

from app import routes
