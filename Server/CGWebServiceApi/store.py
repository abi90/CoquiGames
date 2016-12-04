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
GET Product and related products
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


@store_blueprint.route("/product/<int:productid>/related", methods=['GET'])
def related_products(productid):
    try:
        results = dbm.fetch_related_products(productid)
        return jsonify(results)
    except Exception as e:
        print e
        return internal_server_error()


@store_blueprint.route("/product/<int:productid>/altimgs", methods=['GET'])
def get_product_alt_imgs(productid):
    try:
        imgs = dbm.fetch_product_alt_img(productid)
        return jsonify(imgs)
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
            for p in platform_list:
                if p['platformid'] == platformid:
                    return jsonify([])
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
            return jsonify(result)
        else:
            for p in platform_list:
                if p['platformid'] == platformid:
                    return jsonify([])
        return not_found()

    except Exception as e:
        print e
        return internal_server_error()


@store_blueprint.route("/platform/<int:platformid>/top", methods=['GET'])
def platform_top(platformid):
    try:
        top = dbm.fetch_platform_top(platformid)
        return jsonify(top)
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

                if dbm.insert_product_rating(productid=productid,rate=request.json['rating']):
                    response = jsonify({"Message": "Completed"})
                    response.status_code = 201
                    return response
                return not_found()
        else:
            return bad_request()
    except Exception as e:
        print e
        return internal_server_error()


"""
GET's for Store Home Page
"""


@store_blueprint.route("/top", methods=['GET'])
def store_top():
    try:
        top = dbm.fetch_home_top()
        return jsonify(top)
    except Exception as e:
        print e
        return internal_server_error()


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
        if 'title' in request.json:

            products = dbm.search_products_by_title(request.json['title'])
            result = []

            if 'platformid' or 'genres' or 'price' in request.json:
                # Filter results by title
                for p in products:
                    if match(p, request.json):
                        result.append(p)
            else:
                result = products

            if result:
                # Sort Results
                if 'sort' in request.json:
                    if request.json['sort'] == 'A-Z':
                        result = sorted(result, key=lambda k: k['title'])
                    elif request.json['sort'] == 'Z-A':
                        result = sorted(result, key=lambda k: k['title'], reverse=True)
                # Return Results
                if 'max' in request.json:
                    return jsonify(result[:request.json['max']])
                else:
                    return jsonify(result)
            else:
                return not_found()
        else:
            return bad_request()
    except Exception as e:
        print e
        return internal_server_error()



@store_blueprint.route("/advanced_search", methods=['POST'])
def advanced_search():
    try:
        if 'platform' and 'genre' and 'category' in request.json:

            products = dbm.advanced_search(request.json['platformid'],request.json['genre'],request.json['category'])

            if products:

              return jsonify(products)

            else:
                return not_found()
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


@store_blueprint.route("/genres", methods=['GET'])
def genres():
    try:
        result = dbm.fetch_store_genres();
        if result:
            return jsonify(result)
        else:
            return not_found()
    except Exception as e:
        print e
        return internal_server_error()


def match(prod, data):
    result = True
    if 'genres' in data:
        result = result and prod['genre'] in data['genres']
    if 'platformid' in data:
        result = result and (str(prod['platformid']) == str(data['platformid']))
    if 'price' in data:
        result = result and (float(data['price']['from']) <= float(prod['price']) <= float(data['price']['to']))
    if 'category' in data:
        result = result and prod['category'] in data['category']
    return result

