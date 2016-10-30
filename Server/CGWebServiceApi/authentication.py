from flask import jsonify, request, g
from functools import wraps
from __init__ import app
from itsdangerous import (TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired)

users = [
    {
        'uid': 1,
        'uadmin': False,
        'ufirstname': 'Gary',
        'ulastname': 'Oak',
        'uemail': 'gary.oak@upr.edu',
        'uphone': '787-893-9067',
        'udob': '31-12-1996',
        'uname': 'gary123',
        'upassword': 'Gary123s'
    },
    {
        'uid': 2,
        'uadmin': False,
        'ufirstname': 'Ash',
        'ulastname': 'Ketchum',
        'uemail': 'ash.ketchum@upr.edu',
        'uphone': '787-893-9067',
        'udob': '03-12-1996',
        'uname': 'ash123',
        'upassword': 'Ash123s'
    },
    {
        'uid': 3,
        'uadmin': True,
        'ufirstname': 'Elsa',
        'ulastname': 'Pito',
        'uemail': 'elsa.pito@upr.edu',
        'uphone': '787-893-9067',
        'udob': '03-12-1996',
        'uname': 'elsa123',
        'upassword': 'secret'
    }
]


def generate_auth_token(id, expiration=600):
    s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
    return s.dumps({'id': id})


def verify_auth_token(token, userid):
    s = Serializer(app.config['SECRET_KEY'])
    try:
        data = s.loads(token)
    except SignatureExpired:
        return False    # valid token, but expired
    except BadSignature:
        return False    # invalid token
    if data['id'] == userid:
        return True

    return False




def check_auth(username, password, userid):
    """
    Verifies request username password and path argument userid matches a user in the list
    :param username:
    :param password:
    :param userid:
    :return:
    """
    # first try to authenticate by token

    if not verify_auth_token(username, userid):
        # try to authenticate with username/password
       return False

    return True

    """
    for usr in users:
        if usr['uname'] == username:
            return usr['upassword'] == password and usr['uid'] == userid
    return False
    """


def authenticate():
    """

    :return:
    """
    message = {'message': "Authenticate."}
    resp = jsonify(message)

    resp.status_code = 401
    # resp.headers['WWW-Authenticate'] = 'Basic realm="Example"'

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
        elif not check_auth(auth.username, auth.password, int(kwargs['userid'])):
            return authenticate()
        return f(*args, **kwargs)

    return decorated
