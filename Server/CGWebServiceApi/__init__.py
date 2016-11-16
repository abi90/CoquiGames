from flask import Flask
from flask_cors import CORS
import errors
import user
import store
import admin

app = Flask(__name__)
cors = CORS(app)

app.config['SECRET_KEY'] = 'ALS"KDSA(D*D^AUCHNJcYAS*^%S^FsaYTF^&As'


@app.route("/")
def hello():
    return "Welcome to CoquiGames Web Service API!"


def get_key():
    return app.config['SECRET_KEY']


def create_app():
    app.register_blueprint(errors.errors)
    app.register_blueprint(store.store_blueprint, url_prefix='/store')
    app.register_blueprint(user.user_blueprint, url_prefix='/user')
    app.register_blueprint(admin.admin_blueprint, url_prefix='/admin')
    return app
