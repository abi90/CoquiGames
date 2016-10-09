from flask import Blueprint, jsonify, request, json
from authentication import requires_auth
from errors import not_found

user_blueprint = Blueprint('user', __name__)

users = [
    {
        'id': 1,
        'first_name': 'Gary',
        'last_name': "Oak"
    },
    {
        'id': 2,
        'first_name': 'Ash',
        'last_name': 'Sucks'
    },
    {
        'id': 3,
        'first_name': 'Red',
        'last_name': 'Rules'
    }
]


@user_blueprint.route("/<userid>", methods=['GET', 'PUT'])
@requires_auth
def user(userid):
    print(users)
    if request.method == 'GET':
        for e in users:
            if e['id'] == int(userid):
                return jsonify(e)
        return not_found()

    elif request.method == 'PUT':
        for e in users:
            if e['id'] == int(userid):
                users.remove(e)
                users.append(request.json)
                return jsonify(request.json)
        return not_found()


@user_blueprint.route("/", methods=['POST'])
@requires_auth
def post_user():
    users.append(request.json)
    return json.dumps(request.json)
