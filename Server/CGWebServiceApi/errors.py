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