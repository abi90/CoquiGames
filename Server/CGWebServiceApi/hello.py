from flask import Flask, request, Blueprint, jsonify
from authentication import requires_auth


app = Flask(__name__)
users = Blueprint('users', __name__)


@users.route("/me")
@requires_auth
def me():
    return "This is my Page", 200


@app.route("/")
def hello():
    return "Hello World!"


@app.route("/contact")
@requires_auth
def contact():
    return "You can contact me at 555-5555, or "" \
    "" email me at test@example.com"


if __name__ == "__main__":
    app.debug = True
    app.register_blueprint(users, url_prefix='/users')
    app.run()