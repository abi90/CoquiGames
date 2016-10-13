from flask import jsonify, request
from functools import wraps

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


def check_auth(username, password, userid):
    """
    Verifies request username password and path argument userid matches a user in the list
    :param username:
    :param password:
    :param userid:
    :return:
    """
    for usr in users:
        if usr['uname'] == username:
            return usr['upassword'] == password and usr['uid'] == userid
    return False


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
