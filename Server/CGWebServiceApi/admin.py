from flask import Blueprint, jsonify, request, json
from authentication import admin_verification
from errors import not_found, bad_request, internal_server_error, missing_parameters_error
from user import validate_account
import DBManager as dbm

admin_blueprint = Blueprint('admin', __name__)

product_keys = ['title', 'release', 'price', 'platformid',
                'genre', 'esrb', 'description', 'aditionalinfo', 'category']

post_user_keys = ['ufirstname', 'ulastname', 'uemail', 'uphone', 'udob',
                  'uname', 'upassword']

announcement_keys = ['aid', 'a_img', 'a_title', 'active', 'platformid']


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


@admin_blueprint.route("/announcements", methods=['GET', 'POST'])
@admin_verification
def get_announcements():
    try:
        if request.method=='GET':
            announcements = dbm.fetch_all_announcements()
            if announcements:
                return jsonify(announcements)
            return not_found()
        elif request.method=='POST':
            for key in announcement_keys:
                if key not in announcement_keys:
                    return jsonify({"error": "Paramenter {0} missing in request".format(key)})
            aid = dbm.create_announcement(request.json['a_title'], request.json['a_img'], request.json['platformid'], request.json['active'])
            return jsonify({'aid': aid})
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


@admin_blueprint.route("/order/<int:orderid>/status/<int:order_statusid>", methods=['PUT'])
@admin_verification
def update_order_status(order_statusid,orderid):
    try:
        result = dbm.change_order_status(order_statusid,orderid)
        return jsonify({"mesagge": result})
    except Exception as e:
        print e.message
        return internal_server_error()


@admin_blueprint.route("/announcement/<int:aid>/deactivate", methods=['PUT'])
@admin_verification
def deactivate_announcement(aid):
    try:
        if request.json:

            for key in announcement_keys:
                if key not in request.json:
                    return jsonify({"error": "Paramenter {0} missing in request".format(key)})

            result = dbm.deactivate_announcements(request.json['platformid'], aid)
            return jsonify(result)
        else:
            return bad_request()
    except Exception as e:
        print e.message
        return internal_server_error()


@admin_blueprint.route("/announcement/<int:aid>", methods=['PUT'])
@admin_verification
def update_announcement(aid):
    try:
        if request.json:
            for key in announcement_keys:
                if key not in request.json:
                    return jsonify({"error": "Paramenter {0} missing in request".format(key)})
            if int(request.json['platformid']) > 0:
                result = dbm.edit_platform_announcement(request.json['a_img'], request.json['a_title'],
                                                        request.json['active'], request.json['aid'], request.json['platformid'])
            else:
                result = dbm.edit_store_announcement(request.json['a_img'],
                                                     request.json['a_title'], request.json['active'], request.json['aid'])
            return jsonify({'aid': result})
        else:
            return bad_request()
    except Exception as e:
        print e.message
        return internal_server_error()


@admin_blueprint.route("/product/<int:productid>", methods=['PUT'])
@admin_verification
def update_product(productid):
    try:
        if request.json:
            for key in product_keys:
                if key not in request.json:
                    return jsonify({"error": "Missing {0} in request".format(key)})
            result = dbm.update_product(productid, request.json)
            return jsonify({"pid": result})
    except Exception as e:
        print e.message
        return internal_server_error()

@admin_blueprint.route("/genres", methods=['GET'])
@admin_verification
def get_genres():
    try:
        genres = dbm.fetch_all_genres()
        if genres:
            return jsonify(genres)
        return not_found()
    except Exception as e:
        print e
        return internal_server_error()


@admin_blueprint.route("/genres/<int:genreid>/deactivate", methods=['PUT'])
@admin_verification
def deactivate_genre(genreid):
    try:
        result = dbm.deactivate_genre(genreid)
        return jsonify({"mesagge": result})
    except Exception as e:
        print e.message
        return internal_server_error()


@admin_blueprint.route("/genres/<int:genreid>/activate", methods=['PUT'])
@admin_verification
def activate_genre(genreid):
    try:
        result = dbm.activate_genre(genreid)
        return jsonify({"mesagge": result})
    except Exception as e:
        print e.message
        return internal_server_error()

@admin_blueprint.route("/genres", methods=['POST'])
@admin_verification
def create_genre():
    try:
        if request.json:
            if 'genre' and 'active' not in request.json:
                    return missing_parameters_error()
            result = dbm.create_genre(request.json)
            return jsonify({"genreid": result})
        else:
            return bad_request
    except Exception as e:
        print e.message
        return internal_server_error()
