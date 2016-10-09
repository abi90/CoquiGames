from flask import jsonify, request
from functools import wraps


def check_auth(username, password):
    """

    :param username:
    :param password:
    :return:
    """
    return username == 'admin' and password == 'secret'


def authenticate():
    """

    :return:
    """
    message = {'message': "Authenticate."}
    resp = jsonify(message)

    resp.status_code = 401
    resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'

    return resp


def requires_auth(f):
    """

    :param f:
    :return:
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return authenticate()

        elif not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)

    return decorated
