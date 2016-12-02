from flask import Blueprint, jsonify, request, json
from authentication import admin_verification
from errors import not_found, bad_request, internal_server_error
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