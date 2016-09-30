from flask import Flask, request, Blueprint

app = Flask(__name__)
users = Blueprint('users',__name__)

@users.route("/me")
def me():
    return "This is my Page", 200

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/contact")
def contact():
    return "You can contact me at 555-5555, or "" \
    "" email me at test@example.com"

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
# Logic for handling login
        pass
    else:
        return "Done"

if __name__ == "__main__":
    app.debug = True
    app.register_blueprint(users, url_prefix='/users')
    app.run()