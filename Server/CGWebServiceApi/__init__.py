from flask import Flask
from errors import errors
import user
import store

app = Flask(__name__)


if __name__ == "__main__":
    app.debug = True
    app.register_blueprint(errors)
    app.register_blueprint(store.store_blueprint)
    app.register_blueprint(user.user_blueprint, url_prefix='/user')
    app.run()
