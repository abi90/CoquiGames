from flask import Flask
from errors import errors
import user
import store

app = Flask(__name__)


@app.route("/")
def hello():
    return "Welcome to CoquiGames Web Service API!"


def create_app():
    app.register_blueprint(errors)
    app.register_blueprint(store.store_blueprint, url_prefix='/store')
    app.register_blueprint(user.user_blueprint, url_prefix='/user')
    return app
