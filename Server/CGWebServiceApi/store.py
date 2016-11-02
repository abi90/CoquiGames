from flask import Blueprint, jsonify, request
from errors import not_found, bad_request, internal_server_error
import DBManager as dbm

store_blueprint = Blueprint('store', __name__)

# Platform List with navbar information
try:
    platform_list = dbm.fetch_platforms()
except Exception as e:
    print e
    platform_list = []


"""
GET Product
"""


@store_blueprint.route("/product/<int:productid>", methods=['GET'])
def get_product(productid):
    try:
        product = dbm.fetch_product(productid)
        if product:
            return jsonify(product)
        return not_found()
    except Exception as e:
        print e
        return internal_server_error()


"""
Products Methods by Platform
"""


@store_blueprint.route("/platform/<int:platformid>/latest", methods=['GET'])
def latest_prod(platformid):
    try:
        result = dbm.fetch_platform_latest_products(platformid)
        if result:
            return jsonify(result)
        else:
            return not_found()
    except Exception as e:
        print e
        return internal_server_error()

"""
Get's platform drop-down menu content
"""


@store_blueprint.route("/platform/<int:platformid>", methods=['GET'])
def get_platform(platformid):
    try:
        for p in platform_list:
            if p['platformid'] == platformid:
                return jsonify(p)
        return not_found()
    except Exception as e:
        print e
        return internal_server_error()


@store_blueprint.route("/platform/<int:platformid>/special", methods=['GET'])
def special_products(platformid):
    try:
        result = dbm.fetch_platform_special_products(platformid)
        if result:
            #result = sorted(result, key=lambda k: parser.parse(k['release']))
            return jsonify(result)
        else:
            return not_found()
    except Exception as e:
        print e
        return internal_server_error()


@store_blueprint.route("/platform/<int:platformid>/announcements", methods=['GET'])
def announcement_by_platform(platformid):
    try:
        announcements = dbm.fetch_platform_announcements(platformid)
        if announcements:
            return jsonify(announcements)
        else:
            return not_found()
    except Exception as e:
        print e
        return internal_server_error()


@store_blueprint.route("/product/<int:productid>/rating", methods=['PUT'])
def rating(productid):
    try:
        if request.json:
            try:
                if dbm.insert_product_rating(productid=productid,rate=request.json['Rating']):
                    response = jsonify({"Message": "Completed"})
                    response.status_code = 201
                    return response
                return not_found()
            except Exception as e:
                print e
                bad_request()
        else:
            return bad_request()
    except Exception as e:
        print e
        return internal_server_error()


"""
GET's for Store Home Page
"""


@store_blueprint.route("/platforms", methods=['GET'])
def store_platforms():
    try:
        return jsonify(platform_list)
    except Exception as e:
        print e
        return internal_server_error()


@store_blueprint.route("/search", methods=['POST'])
def search():
    try:
        products = dbm.fetch_latest_products()
        result = []
        if request.json:
            for p in products:
                if match(p, request.json):
                    result.append(p)
            if result:
                if request.json['Sort'] == 'A-Z':
                    result = sorted(result, key=lambda k: k['Title'])
                elif request.json['Sort'] == 'Z-A':
                    result = sorted(result, key=lambda k: k['Title'], reverse=True)
                return jsonify(result[:request.json['Max']])
            else:
                not_found()
        else:
            return bad_request()
    except Exception as e:
        print e
        return internal_server_error()


@store_blueprint.route("/announcements", methods=['GET'])
def home_announcements():
    try:
        # Global Store (Home) carousel announcements
        home_announcements_list = dbm.fetch_store_announcements()
        return jsonify(home_announcements_list)
    except Exception as e:
        print e
        return internal_server_error()


@store_blueprint.route("/latestproduct", methods=['GET'])
def home_latest_prod():
    try:
        result = dbm.fetch_latest_products()
        if result:
            return jsonify(result)
        else:
            not_found()
    except Exception as e:
        print e
        return internal_server_error()


@store_blueprint.route("/specialproduct", methods=['GET'])
def home_specials_prod():
    try:
        result = dbm.fetch_special_products()
        if result:
            return jsonify(result)
        else:
            return not_found()
    except Exception as e:
        print e
        return internal_server_error()


def match(prod, request):
    result = prod['PlatformId'] == request['PlatformId']
    result = result and prod['Genre'] in request['Genre']
    result = result and prod['Category'] in request['Category']
    result = result and (prod['Price'] >= request['Price']['From'] or prod['Price'] <= request['Price']['To'])
    if request['InOffer'] == "True":
        result = result and prod['InOffer']
    return result
