from flask import Blueprint, jsonify, request, json
from authentication import admin_verification
from errors import not_found, bad_request, internal_server_error, missing_parameters_error
from user import validate_account, post_user_keys
import DBManager as dbm

admin_blueprint = Blueprint('admin', __name__)

product_keys = ['title', 'release', 'price', 'platformid',
                'genre', 'esrb', 'description', 'aditionalinfo', 'category']


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


@admin_blueprint.route("/product/platforms", methods=['GET'])
@admin_verification
def get_platforms():
    try:
        platforms = dbm.fetch_all_platforms()
        if platforms:
            return jsonify(platforms)
        return not_found()
    except Exception as e:
        print e
        return internal_server_error()


@admin_blueprint.route("/product/categories", methods=['GET'])
@admin_verification
def get_categories():
    try:
        categories = dbm.fetch_all_categories()
        if categories:
            return jsonify(categories)
        return not_found()
    except Exception as e:
        print e
        return internal_server_error()

@admin_blueprint.route("/product/genres", methods=['GET'])
@admin_verification
def get_genre():
    try:
        genre = dbm.fetch_all_genre()
        if genre:
            return jsonify(genre)
        return not_found()
    except Exception as e:
        print e
        return internal_server_error()


@admin_blueprint.route("/announcements", methods=['GET'])
@admin_verification
def get_announcements():
    try:
        announcements = dbm.fetch_all_announcements()
        if announcements:
            return jsonify(announcements)
        return not_found()
    except Exception as e:
        print e
        return internal_server_error()


@admin_blueprint.route("/account/<int:accountid>/deactivate", methods=['PUT'])
@admin_verification
def deactivate_user(accountid):
    try:
        result = dbm.deactivate_user(accountid)
        return jsonify({"mesagge": result})
    except Exception as e:
        print e.message
        return internal_server_error()


@admin_blueprint.route("/account/<int:accountid>/password", methods=['PUT'])
@admin_verification
def change_password(accountid):
    try:
        if request.json:
            result = dbm.update_user_password(accountid, request.json['upassword'])
            return jsonify({"mesagge": result})
        else:
            return bad_request

    except Exception as e:
        print e.message
        return internal_server_error()


@admin_blueprint.route("/", methods=['POST'])
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
            return jsonify({"uid": result})
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

@admin_blueprint.route("/orders/status", methods=['GET'])
@admin_verification
def get_all_status():
    try:
        status = dbm.fetch_all_status()
        if status:
            return jsonify(status)
        return not_found()
    except Exception as e:
        print e
        return internal_server_error()


@admin_blueprint.route("/product", methods=['POST'])
@admin_verification
def create_product():
    try:
        if request.json:
            for key in product_keys:
                if key not in request.json:
                    return missing_parameters_error()
            result = dbm.create_product(request.json)
            return jsonify({"pid": result})
        else:
            return bad_request
    except Exception as e:
        print e.message
        return internal_server_error()


@admin_blueprint.route("/product/rating", methods=['GET'])
@admin_verification
def get_ratings():
    try:
        rating = dbm.fetch_esrb_ratings()
        if rating:
            return jsonify(rating)
        return not_found()
    except Exception as e:
        print e
        return internal_server_error()


@admin_blueprint.route("/platform/<int:platformid>/deactivate", methods=['PUT'])
@admin_verification
def deactivate_platform_admi(platformid):
    try:
        result = dbm.deactivate_platform(platformid)
        return jsonify({"mesagge": result})
    except Exception as e:
        print e.message
        return internal_server_error()


@admin_blueprint.route("/product/<int:productid>/deactivate", methods=['PUT'])
@admin_verification
def deactivate_product(productid):
    try:
        result = dbm.deactivate_product(productid)
        return jsonify({"mesagge": result})
    except Exception as e:
        print e.message
        return internal_server_error()