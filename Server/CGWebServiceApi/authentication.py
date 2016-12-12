from flask import jsonify, request, g
from functools import wraps
from errors import unauthorized
import __init__ as config
from DBManager import authenticate_user, authenticate_admin
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)


def generate_auth_token(id, expiration=3600):
    """
    Generates token with the given id and expiration time
    :param id:
    :param expiration:
    :return:
    """
    s = Serializer(config.get_key(), expires_in=expiration)
    return s.dumps({'id': id})


def verify_auth_token(token, userid):
    """

    :param token:
    :param userid:
    :return:
    """
    s = Serializer(config.get_key())
    try:
        data = s.loads(token)
    except SignatureExpired:
        return False    # valid token, but expired
    except BadSignature:
        return False    # invalid token
    if data['id']['uid'] == int(userid):
        return True # valid token and request
    return False # valid token but invalid request


def check_auth(username, password, userid):
    """
    Verifies request username password and path argument userid matches a user in the list
    :param username:
    :param password:
    :param userid:
    :return:
    """
    # first try to authenticate by token
    if not verify_auth_token(password, userid):
        # try to authenticate with username/password/id(from url request)
        user = authenticate_user(username, userid, password)
        if user:
            return True
        else:
            return False

    return True


def authenticate():
    """
    Error Message when invalid user credentials or expired token.
    :return:
    """
    message = {'message': "Authenticate."}
    resp = jsonify(message)
    resp.status_code = 401
    return resp


def requires_auth(f):
    """
    Wrapper definition for requires_auth. Used in http basic authentication.
    :param f: function
    :return: decorated function
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return unauthorized()
        elif not check_auth(auth.username, auth.password, int(kwargs['userid'])):
            return authenticate()
        return f(*args, **kwargs)

    return decorated


def verify_admin_token(token):
    """

    :param token:
    :param userid:
    :return:
    """
    s = Serializer(config.get_key())
    try:
        data = s.loads(token)
    except SignatureExpired:
        return False    # valid token, but expired
    except BadSignature:
        return False    # invalid
    if int(data['id']['roleid']) == 3:
        return True # valid token and request
    return False # valid token but invalid request


def check_admin(username, password):
    """
        Verifies request username password matches an admin user
        :param username:
        :param password:
        :param userid:
        :return:
        """
    # first try to authenticate by token
    if not verify_admin_token(password):
        # try to authenticate with username/password/id(from url request)
        user = authenticate_admin(username, password)
        if user:
            return True
        else:
            return False
    return True


def admin_verification(function):
    """
    Wrapper definition for requires_auth. Used in http basic authentication.
    :param function: function
    :return: decorated function
    """
    @wraps(function)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth:
            return unauthorized()
        elif not check_admin(auth.username, auth.password):
            return authenticate()
        return function(*args, **kwargs)
    return decorated