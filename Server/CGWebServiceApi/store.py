from flask import Blueprint, jsonify, request
from errors import not_found, bad_request

store_blueprint = Blueprint('store', __name__)

products = [
    {
        'Pid': 1,
        'PhotoLink': 'img/{example}',
        'Title': '{Title}',
        'Platform': '{Platformid}',
        'Genre': '{Genre|Category}',
        'ESRB': '{M|E|T|NR|etc}',
        'Release': 'YYYY-mm-dd',
        'Availability': True,
        'Price': 00.00,
        'Description': '{Description}',
        'AditionalInfo': '{Additional info}',
        'InOffer': True,
        'OfferProce': 0,
        'Rating': 5
    }
]
platforms = []

announcements = []

products_announcements = []

"""
GET Product
"""


@store_blueprint.route("/<prodictid>", methods=['GET'])
def prod(productid):
    for p in products:
        if p['Pid'] == productid:
            return jsonify(p)
    return not_found()


"""
Products Methods by Platform
"""


@store_blueprint.route("/latest/<platform>", methods=['GET'])
def latest_prod(platform):
    result = []
    for p in products:
        if p['Platform'] == platform:
            result.append()
    if result:
        result = sorted(result, key=lambda k: k['Release'])
        return jsonify(result)
    else:
        return not_found()


@store_blueprint.route("/special/<platform>", methods=['GET'])
def special_products(platform):
    result = []
    for p in products:
        if p['Platform'] == platform and p['InOffer']:
            result.append()
    if result:
        result = sorted(result, key=lambda k: k['Release'])
        return jsonify(result)
    else:
        return not_found()


@store_blueprint.route("/announcements/<platformid>", methods=['GET'])
def announcement_by_platform(platform):
    result = []
    for a in announcement_by_platform:
        if a['Platform'] == platform:
            result.append(a)
    if result:
        result = sorted(products, key=lambda k: k['Release'])
        return jsonify(result)
    else:
        return not_found()


@store_blueprint.route("/ratings/<productid>", methods=['PUT'])
def rating(productid):
    if request.json:
        for p in products:
            if p['Pid'] == productid:
                p['Rating'] = request.json['Rating']
        return not_found()
    else:
        return bad_request()


"""
Home Methods
"""


@store_blueprint.route("/platforms", methods=['GET'])
def platforms():
    return jsonify(platforms)


@store_blueprint.route("/search", methods=['GET'])
def search():
    result = []
    if request.json:
        # TODO: Search for products that match request.json parameters
        return jsonify(result)
    else:
        return bad_request()


@store_blueprint.route("/announcements", methods=['GET'])
def announcements():
    return jsonify(announcements)


@store_blueprint.route("/latestproduct", methods=['GET'])
def latest_prod():
    result = sorted(products, key=lambda k: k['Release'])
    return jsonify(result)


@store_blueprint.route("/specialproduct", methods=['GET'])
def latest_prod():
    result = []
    for p in products:
        if p['InOffer']:
            result.append(p)
    if result:
        result = sorted(products, key=lambda k: k['Release'])
        return jsonify(result)
    else:
        return not_found()
