from flask import jsonify, request, Blueprint

errors = Blueprint('errors', __name__)


@errors.errorhandler(404)
def not_found():
    message = {
            'status': 404,
            'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


@errors.errorhandler(400)
def bad_request():
    message = {
            'status': 400,
            'message': 'Incorrect or missing parameters in request: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 400

    return resp


@errors.errorhandler(500)
def internal_server_error():
    message = {
            'status': 500,
            'message': 'An unexpected error has occurred while processing the request: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 500

    return resp


@errors.errorhandler(401)
def unauthorized():
    message = {
            'status': 401,
            'message': 'The request does not include authentication information: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 401

    return resp


