from flask import Blueprint, jsonify, request
from errors import not_found, bad_request
from dateutil import parser

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

# Platform List with navbar information
platforms = [
        {
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
            'platform': "XBOX ONE",
            'imglogo': 'images/product-images/xbox-one-logo.jpg',
            'consoles': [{'pid':1, 'name': "Xbox One S"},{'pid':2, 'name': "Xbox One"}],
            'accesories': ["Controllers", "Headsets & Mics","Batteries & Chargers","Memory","Storage & Cases","Cables & Adapters","Guides"],
            'topgames':["Action", "Fighting", "Kinect Games", "Music & Party", "RPG", "Shooter","Simulation", "Strategy", "Sports"]
        },
        {
            'platform': "3DS",
            'imglogo': 'images/product-images/3ds-logo.jpg',
            'consoles': [{'pid':1, 'name': "Nintendo 3DS XL"},{'pid':2, 'name': "Nintendo 3DS"},{'id':3, 'name': "Nitendo 2DS"}],
            'accesories': ["Controllers", "Headsets & Mics","Batteries & Chargers","Memory","Storage & Cases","Cables & Adapters","Guides"],
            'gamegen':["Action","eSHop","Fighting","Music & Party", "RPG", "Shooter","Simulation", "Strategy", "Sports"]
        },
        {
            'platform': "Wii U",
            'imglogo': 'images/product-images/wii-u-logo.jpg',
            'consoles': [{'pid': 1, 'name': "Wii U"}],
            'accesories': ["Controllers", "Headsets & Mics","Batteries & Chargers","Memory","Storage & Cases", "Cables & Adapters","Guides"],
            'gamegen':["Action","eSHop","Fighting","Music & Party", "RPG", "Shooter","Simulation", "Strategy", "Sports"]
        }
    ]

announcements = []

products_announcements = []

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
        'Platform': 'Nintendo 3DS',
        'Genre': 'Platform',
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
        'Platform': 'Nintendo 3DS',
        'Genre': 'Adventure',
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
        'Platform': 'Nintendo 3DS',
        'Genre': 'Accesory',
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
        'Platform': 'Xbox One',
        'Genre': 'Platform',
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
        'Platform': 'Xbox One',
        'Genre': 'Action',
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
        'Platform': 'Xbox One',
        'Genre': 'Accesory',
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
        'Platform': 'PS4',
        'Genre': 'Platform',
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
        'Platform': 'PS4',
        'Genre': 'Roleplaying',
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
        'Platform': 'PS4',
        'Genre': 'Accesory',
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
        'Platform': 'Wiiu',
        'Genre': 'Platform',
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
        'Platform': 'Wiiu',
        'Genre': 'Adventure',
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
        'Platform': 'Wiiu',
        'Genre': 'Accesory',
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
products_announcements = [
    #Nintendo 3DS
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

    #Xbox One
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

    #PS4
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

    #Wii U
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
        result = sorted(result, key=lambda k: parser.parse(k['Release']))
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
def home_latest_prod():
    result = sorted(products, key=lambda k: parser.parse(k['Release']))
    return jsonify(result)


@store_blueprint.route("/specialproduct", methods=['GET'])
def home_specials_prod():
    result = []
    for p in products:
        if p['InOffer']:
            result.append(p)
    if result:
        result = sorted(products, key=lambda k: parser.parse(k['Release']))
        return jsonify(result)
    else:
        return not_found()
