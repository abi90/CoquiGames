from flask import Blueprint, jsonify, request
from errors import not_found, bad_request
from dateutil import parser

store_blueprint = Blueprint('store', __name__)

# Platform List with navbar information
platform_list = [
    {
        'PlatformId': 1,
        'platform': "PS4",
        'imglogo': 'images/product-images/ps4-logo.jpg',
        'consoles':
            [
                {'pid':1, 'name': "PS4 Pro"},{'pid': 2, 'name': "PS4 Slim"}
            ],
        'accesories':
            [
                "Controllers", "Headsets & Mics","Batteries & Chargers","Memory","Storage & Cases","Cables & Adapters","Guides"
            ],
        'gamegen':
            [
                "Action", "Fighting", "VR Games", "Music & Party", "RPG", "Shooter","Simulation", "Strategy", "Sports"
            ]
    },
    {
        'PlatformId': 2,
        'platform': "XBOX ONE",
        'imglogo': 'images/product-images/xbox-one-logo.jpg',
        'consoles': [{'pid':1, 'name': "Xbox One S"},{'pid':2, 'name': "Xbox One"}],
        'accesories': ["Controllers", "Headsets & Mics","Batteries & Chargers","Memory","Storage & Cases","Cables & Adapters","Guides"],
        'gamegen':["Action", "Fighting", "Kinect Games", "Music & Party", "RPG", "Shooter","Simulation", "Strategy", "Sports"]
    },
    {
        'PlatformId': 3,
        'platform': "3DS",
        'imglogo': 'images/product-images/3ds-logo.jpg',
        'consoles': [{'pid':1, 'name': "Nintendo 3DS XL"},{'pid':2, 'name': "Nintendo 3DS"},{'id':3, 'name': "Nitendo 2DS"}],
        'accesories': ["Controllers", "Headsets & Mics","Batteries & Chargers","Memory","Storage & Cases","Cables & Adapters","Guides"],
        'gamegen':["Action","eSHop","Fighting","Music & Party", "RPG", "Shooter","Simulation", "Strategy", "Sports"]
    },
    {
        'PlatformId': 4,
        'platform': "Wii U",
        'imglogo': 'images/product-images/wii-u-logo.jpg',
        'consoles': [{'pid': 1, 'name': "Wii U"}],
        'accesories': ["Controllers", "Headsets & Mics","Batteries & Chargers","Memory","Storage & Cases", "Cables & Adapters","Guides"],
        'gamegen':["Action","eSHop","Fighting","Music & Party", "RPG", "Shooter","Simulation", "Strategy", "Sports"]
    }
]

products = [
    # {
    #     'Pid': 1,
    #     'PhotoLink': 'img/{example}',
    #     'Title': '{Title}',
    #     'Platform': '{Platformid}',
    #     'Genre': '{Genre|Category}',
    #     'ESRB': '{M|E|T|NR|etc}',
    #     'Release': 'YYYY-mm-dd',
    #     'Availability': True,
    #     'Price': 00.00,
    #     'Description': '{Description}',
    #     'AditionalInfo': '{Additional info}',
    #     'InOffer': True,
    #     'OfferPrice': 0,
    #     'Rating': 5
    # },

    # Nintendo 3DS Console
    {
        'Pid': 1,
        'PhotoLink': 'img/{example}',
        'Title': 'Nintendo 3DS XL Red ',
        'PlatformId': 3,
        'Genre': 'Console',
        'Category': 'Console',
        'ESRB': 'E',
        'Release': '2011-07-11',
        'Availability': True,
        'Price': 199.99,
        'Description': '{Description}',
        'AditionalInfo': '{Additional info}',
        'InOffer': False,
        'OfferPrice': 149.99,
        'Rating': 5
    },
    #Nintendo 3DS Game
    {
        'Pid': 2,
        'PhotoLink': 'img/{example}',
        'Title': 'Pokemon Rumble',
        'PlatformId': 3,
        'Genre': 'Adventure',
        'Category': 'Game',
        'ESRB': 'E',
        'Release': '2015-10-22',
        'Availability': True,
        'Price': 39.99,
        'Description': '{Description}',
        'AditionalInfo': '{Additional info}',
        'InOffer': True,
        'OfferPrice': 29.99,
        'Rating': 3
    },
    # Nintendo 3DS Accesory
    {
        'Pid': 3,
        'PhotoLink': 'img/{example}',
        'Title': 'Nintendo USB AC Adapter',
        'PlatformId': 3,
        'Genre': 'Cables & Adapter',
        'Category': 'Accessory',
        'ESRB': 'E',
        'Release': '2014-12-01',
        'Availability': True,
        'Price': 19.99,
        'Description': '{Description}',
        'AditionalInfo': '{Additional info}',
        'InOffer': False,
        'OfferPrice': 15.99,
        'Rating': 2
    },
    # XBOX One Console
    {
        'Pid': 4,
        'PhotoLink': 'img/{example}',
        'Title': 'Xbox One',
        'PlatformId': 2,
        'Genre': 'Console',
        'Category': 'Console',
        'ESRB': 'E',
        'Release': '2014-06-04',
        'Availability': True,
        'Price': 349.99,
        'Description': '{Description}',
        'AditionalInfo': '{Additional info}',
        'InOffer': True,
        'OfferPrice': 249.99,
        'Rating': 3
    },
    #XBOX One Game
    {
        'Pid': 5,
        'PhotoLink': 'img/{example}',
        'Title': 'Gears of War 4',
        'PlatformId': 2,
        'Genre': 'Action',
        'Category': 'Game',
        'ESRB': 'M',
        'Release': '2016-10-11',
        'Availability': True,
        'Price': 349.99,
        'Description': '{Description}',
        'AditionalInfo': '{Additional info}',
        'InOffer': False,
        'OfferPrice': 259.99,
        'Rating': 5
    },
    # XBOX One Accesory
    {
        'Pid': 6,
        'PhotoLink': 'img/{example}',
        'Title': 'Xbox Elite Wireless Controller',
        'PlatformId': 2,
        'Genre': 'Controllers',
        'Category': 'Accessories',
        'ESRB': 'E',
        'Release': '2016-10-22',
        'Availability': True,
        'Price': 199.99,
        'Description': '{Description}',
        'AditionalInfo': '{Additional info}',
        'InOffer': True,
        'OfferPrice': 149.99,
        'Rating': 1
    },
    # PS4 Console
    {
        'Pid': 7,
        'PhotoLink': 'img/{example}',
        'Title': 'PlayStation 4 Pro 1TB System',
        'PlatformId': 1,
        'Genre': 'Console',
        'Category': 'Console',
        'ESRB': 'E',
        'Release': '2015-06-15',
        'Availability': True,
        'Price': 399.99,
        'Description': '{Description}',
        'AditionalInfo': '{Additional info}',
        'InOffer': True,
        'OfferPrice': 259.99,
        'Rating': 4
    },
    #PS4 Game
    {
        'Pid': 8,
        'PhotoLink': 'img/{example}',
        'Title': 'Kingdom Hearts 3',
        'PlatformId': 1,
        'Genre': 'Roleplaying',
        'Category': 'Game',
        'ESRB': 'T',
        'Release': '2017-11-23',
        'Availability': False,
        'Price': 69.99,
        'Description': '{Description}',
        'AditionalInfo': '{Additional info}',
        'InOffer': False,
        'OfferPrice': 59.99,
        'Rating': 5
    },
    # PS4 Accesory
    {
        'Pid': 9,
        'PhotoLink': 'img/{example}',
        'Title': 'PS4 Wired Headset',
        'PlatformId': 1,
        'Genre': 'Headsets & Mics',
        'Category': 'Accessory',
        'ESRB': 'E',
        'Release': '2016-03-17',
        'Availability': False,
        'Price': 12.99,
        'Description': '{Description}',
        'AditionalInfo': '{Additional info}',
        'InOffer': False,
        'OfferPrice': 8.99,
        'Rating': 5
    },
    # WiiU Console
    {
        'Pid': 10,
        'PhotoLink': 'img/{example}',
        'Title': 'Nintedno WiiU 32GB - Black',
        'PlatformId': 1,
        'Genre': 'Console',
        'Category': 'Console',
        'ESRB': 'E',
        'Release': '2012-11-25',
        'Availability': True,
        'Price': 299.99,
        'Description': '{Description}',
        'AditionalInfo': '{Additional info}',
        'InOffer': True,
        'OfferPrice': 229.99,
        'Rating': 4
    },
    # WiiU Game
    {
        'Pid': 11,
        'PhotoLink': 'img/{example}',
        'Title': 'The Legend of Zelda: Wind Waker HD',
        'PlatformId': 3,
        'Genre': 'Adventure',
        'Category': 'Game',
        'ESRB': 'E',
        'Release': '2013-08-13',
        'Availability': True,
        'Price': 59.99,
        'Description': '{Description}',
        'AditionalInfo': '{Additional info}',
        'InOffer': True,
        'OfferPrice': 49.99,
        'Rating': 4
    },
    # WiiU Accesory
    {
        'Pid': 12,
        'PhotoLink': 'img/{example}',
        'Title': '320 GB External Hard Drive',
        'PlatformId': 4,
        'Genre': 'Memory',
        'Category': 'Accessory',
        'ESRB': 'E',
        'Release': '2012-05-09',
        'Availability': True,
        'Price': 29.99,
        'Description': '{Description}',
        'AditionalInfo': '{Additional info}',
        'InOffer': True,
        'OfferPrice': 19.97,
        'Rating': 1
    }
]

# Product Home carousel announcements
platform_announcements = [
    #Nintendo 3DS
    {
        'PlatformId': 3,
        'Announcements':
            [
                {
                    'PAnid': 1,
                    'PAnPhotolink': 'img/{example}',
                    'PAnTitle': 'Pre-Order Pokemon Moon and Pokemon Sun',
                    'Product': 'Nintendo 3DS'
                },

                {
                    'PAnid': 2,
                    'PAnPhotolink': 'img/{example}',
                    'PAnTitle': '20% off on all XL consoles',
                    'Product': 'Nintendo 3DS'
                },

                {
                    'PAnid': 3,
                    'PAnPhotolink': 'img/{example}',
                    'PAnTitle': 'New Animal Crossing Amiibo Figures!',
                    'Product': 'Nintendo 3DS'
                },
            ]
    },
    #Xbox One
    {
        'PlatformId': 2,
        'Announcements':
            [
                {
                    'PAnid': 4,
                    'PAnPhotolink': 'img/{example}',
                    'PAnTitle': 'Gears of War 4 Available now',
                    'Product': 'Xbox One'
                },

                {
                    'PAnid': 5,
                    'PAnPhotolink': 'img/{example}',
                    'PAnTitle': 'Warhammer Available Now',
                    'Product': 'Xbox One'
                },

                {
                    'PAnid': 6,
                    'PAnPhotolink': 'img/{example}',
                    'PAnTitle': 'Gears of War 4 Save 20%',
                    'Product': 'Xbox One'
                },
            ]
    },
    #PS4
    {
        'PlatformId': 1,
        'Announcements':
            [
                {
                    'PAnid': 7,
                    'PAnPhotolink': 'img/{example}',
                    'PAnTitle': 'Pre-order Kingdom Hearts 3, get 15%',
                    'Product': 'PS4'
                },

                {
                    'PAnid': 8,
                    'PAnPhotolink': 'img/{example}',
                    'PAnTitle': 'Available 2016/10/29',
                    'Product': 'PS4'
                },

                {
                    'PAnnid': 9,
                    'PAnPhotolink': 'img/{example}',
                    'PAnTitle': '60% off all consoles',
                    'Product': 'PS4'
                },
            ]
    },
    #Wii U
    {
        'PlatformId': 4,
        'Announcements':
            [
                {
                    'PAnid': 10,
                    'PAnPhotolink': 'img/{example}',
                    'PAnTitle': 'amiibo Pre-Order Now',
                    'Product': 'Wiiu'
                },

                {
                    'PAnid': 11,
                    'PAnPhotolink': 'img/{example}',
                    'PAnTitle': 'The Legend of Zelda: Breath of the Wild',
                    'Product': 'Wiiu'
                },

                {
                    'PAnid': 12,
                    'PAnPhotolink': 'img/{example}',
                    'PAnTitle': 'Pre-Order Skylanders today!',
                    'Product': 'Wiiu'
                },
            ]
    }
]

# Global Store (Home) carousel announcements
home_announcements_list = [
    {
        'Anid': 0,
        'AnImg': 'images/slider-imgs/slide1-img.jpg',
        'AnTitle': 'Promo 0'
    },
    {
        'Anid': 1,
        'AnImg': 'images/slider-imgs/slide2-img.jpg',
        'AnTitle': 'Promo 1'
    },
    {
        'Anid': 2,
        'AnImg': 'images/slider-imgs/slide3-img.jpg',
        'AnTitle': 'Promo 2 '
    },
    {
        'Anid': 3,
        'AnImg': 'images/slider-imgs/slide4-img.jpg',
        'AnTitle': 'Promo 3'
    }
]

"""
GET Product
"""


@store_blueprint.route("/<productid>", methods=['GET'])
def get_product(productid):
    for p in products:
        if p['Pid'] == int(productid):
            return jsonify(p)
    return not_found()


"""
Products Methods by Platform
"""


@store_blueprint.route("/latest/<platformid>", methods=['GET'])
def latest_prod(platformid):
    result = []
    for p in products:
        if p['PlatformId'] == int(platformid):
            result.append(p)
    if result:
        result = sorted(result, key=lambda k: parser.parse(k['Release']))
        return jsonify({"Latest": result, "PlatformId": int(platformid)})
    else:
        return not_found()


@store_blueprint.route("/special/<platformid>", methods=['GET'])
def special_products(platformid):
    result = []
    for p in products:
        if p['PlatformId'] == int(platformid) and p['InOffer']:
            result.append(p)
    if result:
        result = sorted(result, key=lambda k: parser.parse(k['Release']))
        return jsonify({"Specials": result, "PlatformId": int(platformid)})
    else:
        return not_found()


@store_blueprint.route("/announcements/<platformid>", methods=['GET'])
def announcement_by_platform(platformid):
    result = []
    for a in platform_announcements:
        if a['PlatformId'] == int(platformid):
            return jsonify(a)
    else:
        return not_found()


@store_blueprint.route("/ratings/<productid>", methods=['PUT'])
def rating(productid):
    if request.json:
        for p in products:
            if p['Pid'] == int(productid):
                p['Rating'] = request.json['Rating']
                return jsonify({"Message": "Completed"})
        return not_found()
    else:
        return bad_request()


"""
GET's for Store Home Page
"""


@store_blueprint.route("/platforms", methods=['GET'])
def store_platforms():
    return jsonify({'Platforms': platform_list})


@store_blueprint.route("/search", methods=['POST'])
def search():
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
            return jsonify({'SearchResult': result[:request.json['Max']]})
        else:
            not_found()
    else:
        return bad_request()


@store_blueprint.route("/announcements", methods=['GET'])
def home_announcements():
    return jsonify({'Announcements': home_announcements_list})


@store_blueprint.route("/latestproduct", methods=['GET'])
def home_latest_prod():
    result = sorted(products, key=lambda k: parser.parse(k['Release']), reverse=True)
    return jsonify({'LatestProducts':result})


@store_blueprint.route("/specialproduct", methods=['GET'])
def home_specials_prod():
    result = []
    for p in products:
        if p['InOffer']:
            result.append(p)
    if result:
        result = []
        for p in products:
            if p['InOffer']==True:
                result.append(p)
        result = sorted(result, key=lambda k: parser.parse(k['Release']), reverse=True)
        return jsonify({'SpecialProducts':result})
    else:
        return not_found()


def match(prod, request):
    result = prod['PlatformId'] == request['PlatformId']
    result = result and prod['Genre'] in request['Genre']
    result = result and prod['Category'] in request['Category']
    result = result and (prod['Price'] >= request['Price']['From'] or prod['Price'] <= request['Price']['To'])
    if request['InOffer'] == "True":
        result = result and prod['InOffer']
    return result
