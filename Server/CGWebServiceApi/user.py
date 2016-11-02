from flask import Blueprint, jsonify, request, json
from authentication import requires_auth, users, generate_auth_token
from errors import not_found, bad_request, internal_server_error
import DBManager as dbm
import re

user_blueprint = Blueprint('user', __name__)

count = 3

adrscnt = 4

ordercnt = 1

cardcnt = 2

user_address_list = [
    {
        'uid': 1,
        'uaddress':
            [
                {
                    'aid': 1,
                    'acurrent': True,
                    'atype': 'shipping',
                    'afullname': 'Gary Oak',
                    'aaddress1': 'Street Q, APT 3',
                    'aaddress2': '',
                    'acity': 'Pallet Town',
                    'azip': '00335',
                    'acountry': 'USA',
                    'aState': 'PR'
                },
                {
                    'aid': 2,
                    'acurrent': True,
                    'atype': 'billing',
                    'afullname': 'Gary Oak',
                    'aaddress1': 'Street Q, APT 3',
                    'aaddress2': '',
                    'acity': 'Pallet Town',
                    'azip': '00335',
                    'acountry': 'USA',
                    'aState': 'PR'
                }
            ]
    },
    {
        'uid': 2,
        'uaddress':
            [
                {
                    'aid': 3,
                    'acurrent': True,
                    'atype': 'shipping',
                    'afullname': 'Gary Oak',
                    'aaddress1': 'Street Q, APT 3',
                    'aaddress2': '',
                    'acity': 'Pallet Town',
                    'azip': '00335',
                    'acountry': 'USA',
                    'aState': 'PR'
                },
                {
                    'aid': 4,
                    'acurrent': True,
                    'atype': 'billing',
                    'afullname': 'Gary Oak',
                    'aaddress1': 'Street Q, APT 3',
                    'aaddress2': '',
                    'acity': 'Pallet Town',
                    'azip': '00335',
                    'acountry': 'USA',
                    'aState': 'PR'
                }
            ]
    }
]

user_payment_list = [
    {
        'uid': 1,
        'upayment':
            [
                {
                    'cid': 1,
                    'cname': 'Professor Oak',
                    'cnumber': '1234-1234-1234-1234',
                    'cexpdate': '01-2017',
                    'cvc': '123',
                    'ctype': 'visa'
                },
                {
                    'cid': 2,
                    'cname': 'Gary Oak',
                    'cnumber': '1234-1234-1234-1234',
                    'cexpdate': '03-2030',
                    'cvc': '123',
                    'ctype': 'mastercard'
                }
            ]
    },
    {
        'uid': 2,
        'upayment':
            [
                {
                    'cid': 3,
                    'cname': 'Delia Ketchum',
                    'cnumber': '1234-1234-1234-1234',
                    'cexpdate': '01-2017',
                    'cvc': '123',
                    'ctype': 'mastercard'
                }
            ]
    }
]

user_order_list = [
    {
        'uid':1,
        'uorders':
            [
                {
                    'oid': 1,
                    'odate':'dd-mm-yyyy',
                    'ostatus': 'shipped',
                    'oproducts': [
                        {
                            'pid': 1,
                            'pname': 'Pokemon Rumble',
                            'pprice': 75.25,
                            'optotal': 150.5,
                            'pquantity': 2
                        },
                        {
                            'pid': 1,
                            'pname': 'Pokemon X',
                            'pprice': 40,
                            'optotal': 120,
                            'pquantity': 3
                        }
                    ],
                    'osubtotal': 270.5,
                    'otax': 11.5,
                    'ototal': 301.60,
                    'osaddress':[
                        {
                            'aid': 1,
                        },
                        {
                            'aid': 2,
                        }
                    ] ,
                    'cid': 1
                }
            ]
    }
]

user_cart_list = [
    {
        'uid': 1,
        'cartlist':
            [
                {
                    'pid': 1,
                    'pname': 'Pokemon Rumble',
                    'pprice': 75.25,
                    'optotal': 150.5,
                    'pquantity': 2
                },
                {
                    'pid': 1,
                    'pname': 'Pokemon X',
                    'pprice': 40,
                    'optotal': 120,
                    'pquantity': 3
                }
            ]
    },
    {
        'uid': 2,
        'cartlist':
            [
                {
                    'pid': 1,
                    'pname': 'Pokemon Rumble',
                    'pprice': 75.25,
                    'pptotal': 150.5,
                    'pquantity': 2
                },
                {
                    'pid': 1,
                    'pname': 'Pokemon X',
                    'pprice': 40,
                    'pptotal': 120,
                    'pquantity': 3
                }
            ]
    }
]

user_wishlist = [
    {
        'uid': 1,
        'wishlist':
            [
                {
                    'pid': 2,
                    'pname': 'Gears of War 4',
                    'pprice': 59.99
                },
                {
                    'pid': 3,
                    'pname': 'Dragon Ball Xenoverse 2',
                    'pprice': 59.99
                }
            ]
    }
]


@user_blueprint.route("/<int:userid>/order", methods=['GET', 'POST'])
@requires_auth
def user_order(userid):
    try:
        if request.method == 'GET':
            for e in user_order_list:
                if e['uid'] == userid:
                    return jsonify(e['uorders'])
            return not_found()
        elif request.method == 'POST':
            if not request.json:
                return bad_request()
            for e in user_payment_list:
                if e['uid'] == userid:
                    for p in e['upayment']:
                        if p['cid'] == request.json['cid']:
                            global ordercnt
                            ordercnt += 1
                            order = {
                                'oid': ordercnt,
                                'odate': request.json['odate'],
                                'ostatus': request.json['ostatus'],
                                'oproducts': request.json['oproducts'],
                                'osubtotal': request.json['osubtotal'],
                                'otax': request.json['otax'],
                                'ototal': request.json['ototal'],
                                'osaddress': request.json['osaddress']
                            }
                            for u in user_order_list:
                                if u['uid'] == userid:
                                    u['uorders'].append(order)
                                    return jsonify(u['uorders'])
                            # User first order
                            result = {'uid': userid, 'uorders': [order]}
                            user_order_list.append(result)
                            return jsonify(result['uorders'])
                    return bad_request()
            return bad_request()
    except:
        return bad_request()


@user_blueprint.route("/<int:userid>/payment", methods=['GET', 'PUT', 'POST'])
@requires_auth
def user_payment(userid):
    if request.method == 'GET':
        for e in user_payment_list:
            if e['uid'] == userid:
                result = []
                for p in e['upayment']:
                    result.append(
                        {
                            'cid': p['cid'],
                            'cnumber': p['cnumber'][-4:],
                            'cexpdate': p['cexpdate'],
                            'ctype': p['ctype']
                        }
                    )
                return jsonify(result)
        return not_found()
    elif request.method == 'PUT':
        for e in user_payment_list:
            if e['uid'] == userid:
                for p in e['upayment']:
                    if p['cid'] == request.json['cid']:
                        e['cname'] = request.json['cname']
                        e['cnumber'] = request.json['cnumber']
                        e['cexpdate'] = request.json['cexpdate']
                        e['cvc'] = request.json['cvc']
                        e['ctype'] = request.json['ctype']
                        return jsonify({
                            'cid': request.json['cid'],
                            'cnumber': request.json['cnumber'][-4:],
                            'cexpdate': request.json['cexpdate'],
                            'ctype': request.json['ctype']
                        })
        return not_found()
    elif request.method == 'POST':
        global cardcnt
        if not request.json:
            return bad_request()
        for e in user_payment_list:
            if e['uid'] == userid:

                cardcnt += 1
                e['upayment'].append(
                    {
                        'cid': cardcnt,
                        'cname': request.json['cname'],
                        'cnumber': request.json['cnumber'],
                        'cexpdate': request.json['cexpdate'],
                        'cvc': request.json['cvc'],
                        'ctype': request.json['ctype']
                    }
                )
                return jsonify(
                    {
                        'cid': cardcnt,
                        'cnumber': request.json['cnumber'][-4:],
                        'cexpdate': request.json['cexpdate'],
                        'ctype': request.json['ctype']
                    }
                )

        cardcnt += 1
        user_payment_list.append(
            {
                'uid': userid,
                'upayment':
                    [
                        {
                            'cid': cardcnt,
                            'cname': request.json['cname'],
                            'cnumber': request.json['cnumber'],
                            'cexpdate': request.json['cexpdate'],
                            'cvc': request.json['cvc'],
                            'ctype': request.json['ctype']
                        }
                    ]
            }
        )
        return jsonify(
            {
                'cid': cardcnt,
                'cnumber': request.json['cnumber'][-4:],
                'cexpdate': request.json['cexpdate'],
                'ctype': request.json['ctype']
            }
        )


@user_blueprint.route("/<int:userid>/address/<atype>", methods=['PUT'])
@requires_auth
def update_address(userid, atype):
    for e in user_address_list:
        if e['uid'] == userid:
            for a in e['uaddress']:
                if a['atype'] == atype:
                    global adrscnt
                    adrscnt += 1
                    a['acurrent'] = False
                    e['uaddress'].append({
                        'aid': adrscnt,
                        'acurrent': True,
                        'atype': request.json['atype'],
                        'afullname': request.json['afullname'],
                        'aaddress1': request.json['aaddress1'],
                        'aaddress2': request.json['aaddress2'],
                        'acity': request.json['acity'],
                        'azip': request.json['azip'],
                        'acountry': request.json['acountry'],
                        'aState': request.json['aState']
                    })
                    return jsonify(e['uaddress'])
            return not_found()
    return not_found()


@user_blueprint.route("/<int:userid>/address", methods=['GET', 'POST'])
@requires_auth
def user_address(userid):
    if request.method == 'GET':
        for e in user_address_list:
            if e['uid'] == userid:
                return jsonify(e['uaddress'])
        return not_found()
    elif request.method == 'POST':
        try:
            if not request.json:
                return bad_request()
            for e in user_address_list:
                if e['uid'] == userid:
                    return bad_request()
            global adrscnt
            temp = adrscnt + 1
            adrscnt += 2
            result = {
                'uid': userid,
                'uaddress':
                    [
                        {
                            'aid': temp,
                            'acurrent': True,
                            'atype': request.json[0]['atype'],
                            'afullname': request.json[0]['afullname'],
                            'aaddress1': request.json[0]['aaddress1'],
                            'aaddress2': request.json[0]['aaddress2'],
                            'acity': request.json[0]['acity'],
                            'azip': request.json[0]['azip'],
                            'acountry': request.json[0]['acountry'],
                            'aState': request.json[0]['aState']
                        },
                        {
                            'aid': adrscnt,
                            'acurrent': True,
                            'atype': request.json[1]['atype'],
                            'afullname': request.json[1]['afullname'],
                            'aaddress1': request.json[1]['aaddress1'],
                            'aaddress2': request.json[1]['aaddress2'],
                            'acity': request.json[1]['acity'],
                            'azip': request.json[1]['azip'],
                            'acountry': request.json[1]['acountry'],
                            'aState': request.json[1]['aState']
                        }
                    ]
            }

            user_address_list.append(result)
            return jsonify(result['uaddress'])
        except Exception as e:
            response = jsonify({"Error": str(e)})
            response.status_code = 500
            return response


@user_blueprint.route("/<int:userid>/wishlist", methods=['GET', 'PUT', 'POST'])
@requires_auth
def user_wish_list(userid):
    print(user_wishlist)
    if request.method == 'GET':
        for e in user_wishlist:
            if e['uid'] == userid:
                return jsonify(e['wishlist'])
        return not_found()
    elif request.method == 'PUT':
        for e in user_wishlist:
            if e['uid'] == userid:
                user_wishlist.remove(e)
                user_wishlist.append(e)
                return jsonify(request.json['wishlist'])
        return not_found()
    elif request.method == 'POST':
        if not request.json:
            return bad_request()
        for e in user_wishlist:
            if e['uid'] == userid:
                return bad_request()
        user_wishlist.append(request.json)
        return jsonify(request.json['wishlist'])


@user_blueprint.route("/<int:userid>/wishlist/<int:productid>", methods=['DELETE'])
@requires_auth
def delete_wishlist(userid, productid):
    print(user_wishlist)
    for e in user_wishlist:
        if e['uid'] == userid:
            for p in e['wishlist']:
                if p['pid'] == productid:
                    e['wishlist'].remove(p)
                    print(user_wishlist)
                    return jsonify({'message': 'Product {} removed from user {} wish list.'.format(productid, userid)})
                return not_found()
        return not_found()
    return not_found()


@user_blueprint.route("/<int:userid>/cart/<int:productid>", methods=['DELETE', 'PUT'])
@requires_auth
def delete_cart(userid, productid):
    print(user_cart_list)
    if request.method == 'DELETE':
        for e in user_cart_list:
            if e['uid'] == userid:
                for p in e['cartlist']:
                    if p['pid'] == productid:
                        e['cartlist'].remove(p)
                        return jsonify({'message': 'Product {} removed from user {} cart.'.format(productid, userid)})
                return not_found()
        return not_found()
    if request.method == 'PUT':
        for e in user_cart_list:
            if e['uid'] == userid:
                for p in e['cartlist']:
                    if p['pid'] == productid:
                        p['pquantity'] = request.json['pquantity']
                        return jsonify(e['cartlist'])
                e['cartlist'].append(
                    {
                        'pid': request.json['pid'],
                        'pname': request.json['pname'],
                        'pprice': request.json['pprice'],
                        'pptotal': request.json['optotal'],
                        'pquantity': request.json['pquantity']
                    }
                )
                return jsonify(e['cartlist'])
        return not_found()


@user_blueprint.route("/<int:userid>/cart", methods=['GET', 'POST'])
@requires_auth
def user_cart(userid):
    print(user_cart_list)
    if request.method == 'GET':
        try:
            cart = dbm.fetch_user_cart(userid=userid)
            if cart:
                return jsonify(cart)
            return not_found()
        except Exception as e:
            print e
            return internal_server_error()
    elif request.method == 'POST':
        if not request.json:
            return bad_request()
        try:
            cart = dbm.fetch_user_cart(userid=userid)
            if not cart:
                dbm.create_user_cart(userid)
                cartid = dbm.fetch_user_cartid(userid=userid)
                for product in request.json['cartlist']:
                    dbm.add_product_to_cart(cartid=cartid['cartid'], productid=product['pid'],product_qty=product['pquantity'])
                cart = dbm.fetch_user_cart(userid=userid)
                return jsonify(cart), 201
            return bad_request()
        except Exception as e:
            print e
            return internal_server_error()


@user_blueprint.route("/<int:userid>", methods=['GET', 'PUT'])
@requires_auth
def user(userid):
    if request.method == 'GET':
        try:
            cg_user = dbm.fetch_user_info(userid=userid)
            if cg_user:
                return jsonify(cg_user)
            return not_found()
        except Exception as e:
            print e
            return internal_server_error()
    elif request.method == 'PUT':
        try:
            if request.json:
                # Verify request parameters
                try:
                    errors = []

                    if (request.json['uname'] and request.json['upassword']
                        and request.json['ufirstname'] and request.json['ulastname']
                        and request.json['uemail'] and request.json['uphone']
                        and request.json['udob']):
                        errors = validate_account(request.json)
                    if errors:
                        return jsonify({'Errors': errors}), 400
                except Exception as ex:
                    return jsonify({'Error': "Missing Parameter {0}.".format(ex)}), 400
                # Update user account:
                if dbm.update_user_account(username=request.json['uname'], upassword=request.json['upassword'], userid=userid):
                    dbm.update_user_info(user_firstname=request.json['ufirstname'],
                                         user_lastname=request.json['ulastname'],
                                         email=request.json['uemail'],
                                         phone=request.json['uphone'],
                                         dob=request.json['udob'],
                                         userid=userid)
                    response = jsonify(request.json)
                    response.status_code = 201
                    return response
                return not_found()
            else:
                bad_request()
        except Exception as e:
            print e
            return internal_server_error()


@user_blueprint.route("/", methods=['POST'])
def post_user():
    if request.json:
        for u in users:
            if u['uemail'] == request.json['uemail'] and u['uname'] == request.json['uname']:
                response = jsonify({'Message': 'Username or email already taken.'})
                response.status_code = 400
                return response
        global count
        count += 1
        result = {
            'uid': count,
            'uadmin': False,
            'ufirstname': request.json['ufirstname'],
            'ulastname': request.json['ulastname'],
            'uemail': request.json['uemail'],
            'uphone': request.json['uphone'],
            'udob': request.json['udob'],
            'uname': request.json['uname'],
            'upassword': request.json['upassword'],
        }
        users.append(result)
        return jsonify(result)
    else:
        bad_request()


@user_blueprint.route("/login", methods=['POST'])
def get_user_id():
    if request.json:
        try:
            uid = dbm.fetch_user_id(request.json['uname'], request.json['upassword'])
            if uid:
                token = generate_auth_token(uid)
                return jsonify({"uid": uid['uid'], 'token': token})
            else:
                # Login Error Response
                return jsonify({'Message': "Username or Password does not match!"}), 401
        except Exception as e:
            print e
            return bad_request()
    else:
        bad_request()


def validate_account(data):
    """
    Validates user account data in request.json
    :param data: request.json
    :return: list of errors
    """
    errors = []
    # Limit username to only characters and numbers. Starting with a letter.
    isValidUsername = re.search(r'(^([a-zA-Z]+)[\w]+)$', data['uname'])
    # username must be greater than 4 characters but less than 20 characters
    if len(str(data['uname'])) < 4 or len(str(data['uname'])) > 20 or not isValidUsername:
        errors.append('Invalid username.')

    # A Password must contain atleast an Upper case leter and a number
    hasupper = re.search('[A-Z]+', data['upassword'])
    hasdigit = re.search('[\d]+', data['upassword'])
    # A Password must be 8 characters to 20 characters long
    if len(str(data['upassword'])) < 8 or len(str(data['upassword'])) > 20 or not hasupper or not hasdigit:
        errors.append('Invalid password.')

    # Email regex for python
    isEmail = re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", data['uemail'])
    if not isEmail:
        errors.append('Invalid email.')

    # Phone regex for python
    isPhone = re.search(r'^(\d{3})([-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})$',
                        data['uphone'])
    if not isPhone:
        errors.append('Invalid Phone Number.')

    # Date regex for python
    isDate = re.search(r'^(\d{4}\-\d{2}\-\d{2})$', data['udob'])
    if not isDate:
        errors.append('Invalid DOB.')

    # Validate First Name
    if len(str(data['ufirstname'])) <= 1 or len(str(data['ufirstname'])) > 255:
        errors.append('Invalid First Name.')

    # Validate Last Name
    if len(str(data['ulastname'])) <= 1 or len(str(data['ulastname'])) > 255:
        errors.append('Invalid Last Name.')

    return errors


