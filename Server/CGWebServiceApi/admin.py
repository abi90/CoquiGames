from flask import Blueprint, jsonify, request, json
from authentication import admin_verification
from errors import not_found, bad_request, internal_server_error, missing_parameters_error
from user import validate_account, post_user_keys
import DBManager as dbm

admin_blueprint = Blueprint('admin', __name__)


@admin_blueprint.route("/users", methods=['GET'])
@admin_verification
def get_users():
    try:
        users = dbm.fetch_users()
        if users:
            return jsonify(users)
        return not_found()
    except Exception as e:
        print e
        return internal_server_error()


@admin_blueprint.route("/products", methods=['GET'])
@admin_verification
def get_products():
    try:
        products = dbm.fetch_all_products()
        if products:
            return jsonify(products)
        return not_found()
    except Exception as e:
        print e
        return internal_server_error()


@admin_blueprint.route("/account/<int:accountid>/deactivate", methods=['PUT'])
@admin_verification
def deactivate_user(accountid):
    try:
        result = dbm.deactivate_user(accountid)
        return jsonify(result)
    except Exception as e:
        print e.message
        return internal_server_error()


@admin_blueprint.route("/account/<int:accountid>/password", methods=['PUT'])
@admin_verification
def change_password(accountid):
    try:
        if request.json:
            result = dbm.update_user_password(accountid, request.json['upassword'])
            return jsonify(result)
        else:
            return bad_request

    except Exception as e:
        print e.message
        return internal_server_error()


@admin_blueprint.route("/admin", methods=['POST'])
@admin_verification
def create_admin():
    try:
        if request.json:
            for key in post_user_keys:
                if key not in request.json:
                    return missing_parameters_error()
            errors = validate_account(request.json)
            if errors:
                return jsonify({'errors': errors}), 400
            result = dbm.add_admin_user(request.json)
            return jsonify(result)
        else:
            return bad_request
    except Exception as e:
        print e.message
        return internal_server_error()


@admin_blueprint.route("/orders", methods=['GET'])
@admin_verification
def get_orders():
    try:
        orders = dbm.fetch_all_orders()
        if orders:
            return jsonify(orders)
        return not_found()
    except Exception as e:
        print e
        return internal_server_error()
