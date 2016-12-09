from flask import Blueprint, jsonify, request
from authentication import requires_auth, generate_auth_token
from errors import not_found, bad_request, internal_server_error, missing_parameters_error
import DBManager as dbm
import re

user_blueprint = Blueprint('user', __name__)

post_user_keys = ['ufirstname', 'ulastname', 'uemail', 'uphone', 'udob',
                  'uname', 'upassword', 'upayment', 'ushippingaddress', 'ubillingaddress']

post_address_keys = ['astate', 'aaddress1', 'aaddress2', 'acity', 'acountry', 'afullname', 'azip']

post_payment_keys = ['cname', 'cnumber', 'cexpdate', 'cvc', 'ctype']

cc_regex = r"""^(?:4[0-9]{12}(?:[0-9]{3})?|(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}|3[47][0-9]{13})$"""

MISSING_PARAMETER = "Missing Parameter {0} in Request JSON."


@user_blueprint.route("/<int:userid>/preferences", methods=['GET', 'PUT'])
@requires_auth
def user_preferences(userid):
    try:
        if request.method == 'GET':
            preferences = dbm.fetch_user_preferences(userid)
            if preferences:
                return jsonify(preferences)
            return not_found()
        elif request.method == 'PUT':
            if ('shipping_addressid' or 'billing_addressid' or 'cid') not in request.json:
                return missing_parameters_error()
            errors = validate_user_preferences(request.json, userid)
            if errors:
                return jsonify({'errors': errors}), 400
            if 'shipping_addressid' in request.json:
                dbm.update_user_preferred_shipping(request.json['shipping_addressid'],userid)
            if 'billing_addressid' in request.json:
                dbm.update_user_preferred_billing(request.json['billing_addressid'], userid)
            if 'cid' in request.json:
                dbm.update_user_preferred_payment(request.json['cid'], userid)
            preferences = dbm.fetch_user_preferences(userid)
            if preferences:
                return jsonify(preferences)
            return bad_request()
    except Exception as e:
        print e.message
        return internal_server_error()


@user_blueprint.route("/<int:userid>/order", methods=['GET', 'POST'])
@requires_auth
def user_order(userid):
    try:
        if request.method == 'GET':
            orders = dbm.fetch_user_orders(userid)
            return jsonify(orders)
        elif request.method == 'POST':
            if not request.json:
                return bad_request()
            if 'shipment_feeid' and 'aid' and 'cid' not in request.json:
                return missing_parameters_error()
            errors = validate_order(request.json, userid)
            if errors:
                return jsonify({'errors': errors}), 400
            orderid = dbm.process_order(userid, request.json)
            if orderid:
                # Fetch Order
                order = dbm.fetch_order(orderid, userid)
                return jsonify(order)
            return internal_server_error()
    except Exception as e:
        print e.message
        return internal_server_error()


@user_blueprint.route("/<int:userid>/payment", methods=['GET', 'POST'])
@requires_auth
def user_payment(userid):
    try:
        if request.method == 'GET':
            payment_method = dbm.fetch_user_payment_methods(userid)
            if payment_method:
                return jsonify(payment_method)
            return not_found()
        elif request.method == 'POST':
            if request.json:
                payment_keys = post_payment_keys
                payment_keys.append('ppreferred')
                for key in payment_keys:
                    if key not in request.json:
                        return missing_parameters_error()
                errors = validate_payment(request.json)
                if errors:
                    return jsonify({'Errors': errors}), 400
                billing_addressid = dbm.fetch_user_preferences(userid)['billing_address']['aid']
                if billing_addressid:
                    pid = dbm.create_user_payment_method(userid, request.json, billing_addressid)
                    return jsonify({'payment_methodid': pid}), 201
                else:
                    return jsonify({'error': 'Preferred Billing Address Not Found For User {0}'.format(userid)}), 400
            return bad_request()
    except Exception as e:
        print e.message
        return internal_server_error()


@user_blueprint.route("/<int:userid>/payment/<payment_methodid>", methods=['PUT', 'DELETE'])
@requires_auth
def update_payment(userid, payment_methodid):
    try:
        if request.method=='PUT':
            if request.json:
                payment_keys = post_payment_keys
                payment_keys.append('ppreferred')
                for key in payment_keys:
                    if key not in request.json:
                        return missing_parameters_error()
                errors = validate_payment(request.json)
                if errors:
                    return jsonify({'Errors': errors}), 400
                billing_addressid = dbm.fetch_user_preferences(userid)['billing_address']['aid']
                if billing_addressid:
                    pid = dbm.update_payment_method(userid, payment_methodid, request.json, billing_addressid)
                    return jsonify({'payment_methodid': pid}), 201
                else:
                    return jsonify({'error': 'Preferred Billing Address Not Found For User {0}'.format(userid)}), 400
            return bad_request()
        elif request.method=='DELETE':
            result = dbm.deactivate_user_payment_method(userid, payment_methodid)
            if result:
                return jsonify(result)
            return bad_request()
    except Exception as e:
        print e.message
        return internal_server_error()


@user_blueprint.route("/<int:userid>/address/<int:addressid>", methods=['PUT'])
@requires_auth
def update_address(userid, addressid):
    try:
        if request.json:
            put_address_keys = post_address_keys
            put_address_keys.append('apreferred')
            put_address_keys.append('atype')
            for key in put_address_keys:
                if key not in request.json:
                    return missing_parameters_error()
            errors = validate_address(request.json)
            if errors:
                return jsonify({'Errors': errors}), 400
            new_address_id = dbm.update_user_address(userid, addressid, request.json)
            return jsonify({'aid': new_address_id}), 201
        return bad_request()
    except Exception as e:
        print e.message
        return internal_server_error()


@user_blueprint.route("/<int:userid>/address", methods=['GET', 'POST'])
@requires_auth
def user_address(userid):
    try:
        if request.method == 'GET':
            address = dbm.fetch_user_address(userid)
            if address:
                return jsonify(address)
            return not_found()
        elif request.method == 'POST':
            if request.json:
                address_keys = post_address_keys
                address_keys.append('apreferred')
                address_keys.append('atype')
                for key in address_keys:
                    if key not in request.json:
                        return missing_parameters_error()
                errors = validate_address(request.json)
                if errors:
                    return jsonify({'Errors': errors}), 400

                if request.json['atype'] == 'billing' and 'pid' not in request.json:
                    return jsonify({'Errors': errors.append("Missing Payment Method.")}), 400

                new_address_id = dbm.create_user_address(userid, request.json)
                return jsonify({'aid': new_address_id}), 201
            else:
                return missing_parameters_error()
    except Exception as e:
        print e.message
        return internal_server_error()


@user_blueprint.route("/<int:userid>/billing_address", methods=['GET'])
@requires_auth
def user_billing_address(userid):
    try:
        address = dbm.fetch_user_billing_address(userid)
        if address:
            return jsonify(address)
        return not_found()
    except Exception as e:
        print e
        return internal_server_error()


@user_blueprint.route("/<int:userid>/shipping_address", methods=['GET'])
@requires_auth
def user_shipping_address(userid):
    try:
        address = dbm.fetch_user_shipping_address(userid)
        if address:
            return jsonify(address)
        return not_found()
    except Exception as e:
        print e
        return internal_server_error()


@user_blueprint.route("/<int:userid>/wishlist", methods=['GET'])
@requires_auth
def user_wish_list(userid):
    try:
        if request.method == 'GET':
            wish_list = dbm.fetch_user_wish_list(userid=userid)
            return jsonify(wish_list)
    except:
        return internal_server_error()


@user_blueprint.route("/<int:userid>/wishlist/<int:productid>", methods=['DELETE', 'POST'])
@requires_auth
def delete_from_user_wish_list(userid, productid):
    try:
        if request.method == 'DELETE':
            in_wish_list = dbm.wish_list_contains(productid=productid,userid=userid)['product_in_wishlist']
            if in_wish_list:
                dbm.remove_from_wish_list(productid=productid,userid=userid)
                wish_list = dbm.fetch_user_wish_list(userid=userid)
                return jsonify(wish_list)
            else:
                not_found()
        elif request.method == 'POST':
            in_wish_list = dbm.wish_list_contains(productid=productid, userid=userid)['product_in_wishlist']
            if not in_wish_list:
                dbm.add_product_to_user_wishlist(productid=productid, userid=userid)
                wish_list = dbm.fetch_user_wish_list(userid=userid)
                return jsonify(wish_list)
            else:
                return jsonify({'error': 'Product {0} is already in user {1} wish list.'.format(productid,userid)}), 400
    except Exception as e:
        print e
        return internal_server_error()


@user_blueprint.route("/<int:userid>/cart/<int:productid>", methods=['DELETE', 'PUT', 'POST'])
@requires_auth
def edit_cart(userid, productid):
    try:
        if request.method == 'DELETE':
            is_deleted = dbm.remove_product_from_cart(userid=userid, productid=productid)
            if is_deleted:
                return jsonify({'Message': 'Product {0} was deleted from user {1} cart'.format(productid, userid)})
            return not_found()
        elif request.method == 'PUT':
            if request.json:
                if 'pquantity' in request.json:
                    cartid = dbm.fetch_user_cartid(userid=userid)['cartid']
                    if cartid:
                        product_qty = int(request.json['pquantity'])
                        if product_qty > 0:
                            cart_contains_product = dbm.cart_contains(productid=productid, cartid=cartid)['product_in_cart']
                            if cart_contains_product:
                                has_changed = dbm.update_cart_product_qty(product_qty=product_qty, productid=productid, userid=userid)
                                if has_changed:
                                    cart = dbm.fetch_user_cart(userid=userid)
                                    return jsonify(cart)
                                return bad_request()
                            else:
                                return jsonify({'error': 'Product {0} does not exist in user {1} cart.'.format(
                                    productid, userid)}), 400
                        else:
                            return jsonify({'error': 'Product Quantity must be greater than 0.'}), 400
                    else:
                        return jsonify({'error': 'User {0} does not have an active cart.'.format(userid)}), 400
            return missing_parameters_error()

        elif request.method == 'POST':
            if request.json:
                if 'pquantity' in request.json:
                    cartid = dbm.fetch_user_cartid(userid=userid)['cartid']
                    if cartid:
                        product_qty = int(request.json['pquantity'])
                        if product_qty > 0:
                            cart_contains_product = dbm.cart_contains(productid=productid, cartid=cartid)['product_in_cart']
                            if not cart_contains_product:
                                added_product = dbm.add_product_to_cart(cartid=cartid, productid=productid,
                                                                        product_qty=product_qty)
                                if added_product:
                                    cart = dbm.fetch_user_cart(userid=userid)
                                    return jsonify(cart)
                            else:
                                return jsonify({'error': 'Product {0} is already in user {1} cart.'.format(productid,userid)}), 400
                        else:
                            return jsonify({'error': 'Product Quantity must be greater than 0.'}), 400
                    else:
                        return jsonify({'error': 'User {0} does not have an active cart.'.format(userid)}), 400
            return missing_parameters_error()

    except Exception as e:
        print e
        return internal_server_error()


@user_blueprint.route("/<int:userid>/cart", methods=['GET', 'POST'])
@requires_auth
def user_cart(userid):
    try:
        if request.method == 'GET':
            cart = dbm.fetch_user_cart(userid=userid)
            if cart:
                return jsonify(cart)
            else:
                # Verify cart is empty
                cartid = dbm.fetch_user_cartid(userid)
                if cartid:
                    return jsonify([])
            return not_found()
        elif request.method == 'POST':
            # Verify that the user does not have an active cart
            cart = dbm.fetch_user_cart(userid=userid)
            if not cart:
                # Create an empty cart
                dbm.create_user_cart(userid)
                cartid = dbm.fetch_user_cartid(userid=userid)
                # Verify if request has a cart list
                if request.json and cartid:
                    if 'cartlist' in request.json:
                        # If there's a cart list with the request add them to the created cart
                        for product in request.json['cartlist']:
                            if 'cartid' and 'pid' and 'ppquantity' in product:
                                dbm.add_product_to_cart(cartid=cartid['cartid'], productid=product['pid'], product_qty=product['pquantity'])
                        # Return the created and filled cart
                        cart = dbm.fetch_user_cart(userid=userid)
                        return jsonify(cart), 201
                    # Invalid request JSON but cart was created
                    return jsonify(cartid), 201
                elif cartid:
                    # If request did not contain a cart list return only the cartid
                    return jsonify(cartid), 201
                else:
                    # Cartid was not created return a bad request
                    return bad_request()
    except Exception as e:
        print e
        return internal_server_error()


@user_blueprint.route("/<int:userid>/password", methods=['PUT'])
@requires_auth
def change_password(userid):
    try:
        if request.json:
            # Verify request json contains needed parameters
            if 'upassword' in request.json:
                return missing_parameters_error()
            # Verify that parameters are valid
            if not validate_password(request.json['upassword']):
                return jsonify({'error': 'Invalid Password.'}), 400
            # Update user password:
            if dbm.change_password(userid):
                return jsonify({"message": "User {0} Password Was Changed.".format(userid)})
            return not_found()
        else:
            return bad_request()
    except Exception as e:
        print e
        return internal_server_error()


@user_blueprint.route("/<int:userid>", methods=['GET', 'PUT'])
@requires_auth
def user(userid):
    try:
        if request.method == 'GET':
            cg_user = dbm.fetch_user_info(userid=userid)
            if cg_user:
                return jsonify(cg_user)
            return not_found()
        elif request.method == 'PUT':
            if request.json:
                # Verify request json contains needed parameters
                if ('uname' and 'ufirstname' and 'ulastname'
                        and 'uemail' and 'uphone' and 'udob' not in request.json):
                    return missing_parameters_error()
                # Verify that parameters are valid
                errors = validate_account_data(request.json)
                if errors:
                    return jsonify({'Errors': errors}), 400
                # Update user account:
                if dbm.update_user_account(username=request.json['uname'],
                                           userid=userid,
                                           user_firstname=request.json['ufirstname'],
                                           user_lastname=request.json['ulastname'],
                                           email=request.json['uemail'],
                                           phone=request.json['uphone'],
                                           dob=request.json['udob'],
                                           ):
                    response = jsonify(request.json)
                    response.status_code = 201
                    return response
                return not_found()
            else:
                return bad_request()
    except Exception as e:
        print e
        return internal_server_error()


@user_blueprint.route("/", methods=['POST'])
def post_user():
    try:
        if request.json:
            # TODO: email user after post
            # Verify request json contains needed parameters
            for key in post_user_keys:
                if key not in request.json:
                    return jsonify({'Error': MISSING_PARAMETER.format(key)}), 400
            for key in post_address_keys:
                if key not in request.json['ushippingaddress'] or key not in request.json['ubillingaddress']:
                    return jsonify({'Error': MISSING_PARAMETER.format(key)}), 400
            for key in post_payment_keys:
                if key not in request.json['upayment']:
                    return jsonify({'Error': MISSING_PARAMETER.format(key)}), 400
            # Verify that parameters are valid
            account_errors = validate_account(request.json)
            if account_errors:
                return jsonify({'errors': account_errors}), 400
            payment_method_errors = validate_payment(request.json['upayment'])
            if payment_method_errors:
                return jsonify({'errors': payment_method_errors}), 400
            address_errors = validate_address(request.json['ushippingaddress'])
            if address_errors:
                return jsonify({'errors': address_errors}), 400
            address_errors = validate_address(request.json['ubillingaddress'])
            if address_errors:
                return jsonify({'errors': address_errors}), 400
            # Verify user account does not exist
            user_exist = dbm.user_account_exist(username=request.json['uname'],
                                                email=request.json['uemail'])['user_exist']
            if not user_exist:
                # Register user and return user data as response
                userid = dbm.register_user(request.json)

                cg_user = dbm.fetch_user_info(userid=userid)
                return jsonify(cg_user), 201
        else:
            return bad_request()
    except Exception as e:
        print e
        return internal_server_error()


@user_blueprint.route("/login", methods=['POST'])
def get_user_id():
    if request.json:
        try:
            uid = dbm.fetch_user_id(request.json['uname'], request.json['upassword'])
            if uid:
                user = uid[0]
                token = generate_auth_token(user)
                return jsonify({"uid": user['uid'], 'token': token, 'roleid': user['roleid']})
            else:
                # Login Error Response
                return jsonify({'Message': "Username or Password does not match!"}), 401
        except Exception as e:
            print e
            return bad_request()
    else:
        return missing_parameters_error()


@user_blueprint.route("/shipmentfees", methods=['GET'])
def shipment_fees():
    try:
        result = dbm.fetch_shipment_fees()
        if result:
            return jsonify(result)
        return not_found()
    except Exception as e:
        print e
        return internal_server_error()


def validate_account_data(data):
    """
    Validates user account data in request.json
    :param data: request.json
    :return: list of errors
    """
    errors = []
    # Limit username to only characters and numbers. Starting with a letter.
    is_valid_username = re.search(r'(^([a-zA-Z]+)[\w]+)$', data['uname'])
    # username must be greater than 4 characters but less than 20 characters
    if len(str(data['uname'])) < 4 or len(str(data['uname'])) > 20 or not is_valid_username:
        errors.append('Invalid username.')
    elif dbm.is_username_taken(data['uname'])['taken']:
        errors.append('Username already taken. Please try with another username.')

    # Email regex for python
    is_email = re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", data['uemail'])
    if not is_email:
        errors.append('Invalid email.')
    elif dbm.is_email_taken(data['uemail'])['taken']:
        errors.append('Email already taken. Please try with another email.')

    # Phone regex for python
    is_phone = re.search(r'^(\d{3})([-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})$',
                         data['uphone'])
    if not is_phone:
        errors.append('Invalid Phone Number.')

    # Date regex for python
    is_date = re.search(r'^(\d{4}\-\d{2}\-\d{2})$', data['udob'])
    if not is_date:
        errors.append('Invalid DOB.')

    # Validate First Name
    if len(str(data['ufirstname'])) <= 1 or len(str(data['ufirstname'])) > 255:
        errors.append('Invalid First Name.')

    # Validate Last Name
    if len(str(data['ulastname'])) <= 1 or len(str(data['ulastname'])) > 255:
        errors.append('Invalid Last Name.')

    return errors


def validate_payment(data):
    """
        Validates user payment data in request.json
        :param data: request.json
        :return: list of errors
        """
    errors = []
    # Limit Card Name to only 255 characters.
    if len(str(data['cname'])) <= 1 or len(str(data['cname'])) > 255:
        errors.append('Invalid Card Name.')

    # Validate with Credit Card regex for python
    is_valid_cc = re.search(cc_regex, str(data['cnumber']))
    if not is_valid_cc:
        errors.append('Invalid Credit Card.')

    # Validate with Date regex for python
    is_date = re.search(r'^(\d{4}\-\d{2})$', data['cexpdate'])
    if is_date:
        # Verify that is not expired
        not_expired = dbm.validate_exp_date(data['cexpdate'])['valid_exp_date']
        if not not_expired:
            errors.append('Invalid Expiration Date.')
    else:
        errors.append('Invalid Expiration Date.')

    # Validate CVC
    is_digit = re.search(r'^([\d]+)$', str(data['cvc']))
    if len(str(data['cvc'])) < 3 or len(str(data['cvc'])) > 4 or not is_digit:
        errors.append('Invalid CVC.')

    # Validate Card Type
    valid_cc = dbm.validate_cc(data['ctype'])['valid_cc']
    if not valid_cc:
        errors.append('Invalid Card Type.')

    return errors


def validate_address(data):
    """
        Validates user address data in request.json
        :param data: request.json
        :return: list of errors
        """
    errors = []
    # Limit Address Sate to only 2 characters.
    if len(str(data['astate'])) < 2 or len(str(data['astate'])) > 2:
        errors.append('Invalid Card Name.')

    # Limit Address Line 1 to only 255 characters.
    if len(str(data['aaddress1'])) < 2 or len(str(data['aaddress1'])) > 255:
        errors.append('Invalid Address Line 1.')

    # Limit Address Line 2 to only 255 characters.
    if len(str(data['aaddress2'])) > 255:
        errors.append('Invalid Address Line 2.')

    # Limit Address City to only 255 characters.
    if len(str(data['acity'])) < 2 or len(str(data['acity'])) > 255:
        errors.append('Invalid Address Line 2.')

    # Check Country is USA
    if not (str(data['acountry']).upper() == 'USA'):
        errors.append('Invalid Country. Only USA is accepted.')

    # Validate Address Full Name
    if len(str(data['afullname'])) < 2 or len(str(data['afullname'])) > 255:
        errors.append('Invalid Address Name.')

    # Validate Zip Code
    is_digit = re.search(r'^([\d]+)$', data['azip'])
    if len(str(data['azip'])) < 5 or len(str(data['azip'])) > 6 or not is_digit:
        errors.append('Invalid Zip Code.')

    return errors


def validate_order(data, userid):
    # Vaidate 'shipment_feeid' and 'aid' and 'cid' in data
    errors = []
    is_valid_fee = dbm.validate_shipment_fee(data['shipment_feeid'])['valid_fee']
    if not is_valid_fee:
        errors.append('Invalid Shipment Fee.')
    is_valid_aid = dbm.validate_address(data['aid'], userid)['valid_aid']
    if not is_valid_aid:
        errors.append('Invalid Address.')
    is_valid_cid = dbm.validate_payment(data['cid'], userid)['valid_pid']
    if not is_valid_cid:
        errors.append('Invalid Payment Method.')
    return errors


def validate_user_preferences(data, userid):
    # Vaidate 'shipping_addressid' and 'billing_addressid' and 'cid'
    errors = []
    if 'shipping_addressid' in data:
        is_valid_aid = dbm.validate_address(data['shipping_addressid'], userid)['valid_aid']
        if not is_valid_aid:
            errors.append('Invalid Shipping Address.')
    if 'billing_addressid' in data:
        is_valid_aid = dbm.validate_address(data['billing_addressid'], userid)['valid_aid']
        if not is_valid_aid:
            errors.append('Invalid Billing Address.')
    if 'cid' in data:
        is_valid_cid = dbm.validate_payment(data['cid'], userid)['valid_pid']
        if not is_valid_cid:
            errors.append('Invalid Payment Method.')
    return errors


def validate_password(password):
    # A Password must contain at least an Upper case letter and a number
    has_upper = re.search('[A-Z]+', password)
    has_digit = re.search('[\d]+', password)
    # A Password must be 8 characters to 20 characters long
    valid = not (len(str(password)) < 8 or len(str(password)) > 20 or not has_upper or not has_digit)
    return valid


def validate_account(data):
    errors = validate_account_data(data)
    if not validate_password(data['upassword']):
        errors.append('Invalid Password')
    return errors





