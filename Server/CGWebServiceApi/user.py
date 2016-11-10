from flask import Blueprint, jsonify, request, json
from authentication import requires_auth, users, generate_auth_token
from errors import not_found, bad_request, internal_server_error
import DBManager as dbm
import re

user_blueprint = Blueprint('user', __name__)

post_user_keys = ['ufirstname', 'ulastname', 'uemail', 'uphone', 'udob',
                  'uname', 'upassword', 'upayment', 'ushippingaddress', 'ubillingaddress']

post_address_keys = ['astate', 'aaddress1', 'aaddress2', 'acity', 'acountry', 'afullname', 'azip']

post_payment_keys = ['cname', 'cnumber', 'cexpdate', 'cvc', 'ctype']

cc_regex = r"""^(?:4[0-9]{12}(?:[0-9]{3})?|(?:5[1-5][0-9]{2}|222[1-9]|22[3-9][0-9]|2[3-6][0-9]{2}|27[01][0-9]|2720)[0-9]{12}|3[47][0-9]{13})$"""


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
            if 'shipping_addressid' or 'billing_addressid' or 'cid' not in request.json:
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
        print e
        return internal_server_error()


@user_blueprint.route("/<int:userid>/order", methods=['GET', 'POST'])
@requires_auth
def user_order(userid):
    try:
        if request.method == 'GET':
            orders = dbm.fetch_user_orders(userid)
            if orders:
                return jsonify(orders)
            return not_found()
        elif request.method == 'POST':
            if not request.json:
                return bad_request()
            if 'shipment_feeid' and 'aid' and 'cid' not in request.json:
                return missing_parameters_error()
            errors = validate_order(request.json, userid)
            if errors:
                return jsonify({'errors': errors}), 400
            # Get User Active Cart
            cartid = dbm.fetch_user_cartid(userid)['cartid']
            if cartid:
                # Deactivate cart to avoid errors
                if dbm.deactivate_user_cart(cartid, userid):
                    # Create an empty order
                    if dbm.insert_empty_order(cartid=cartid,
                                              shippment_feeid=request.json['shipment_feeid'],
                                              shipping_addressid=request.json['aid'],
                                              userid=userid,
                                              payment_methodid=request.json['cid']):
                        # Get latest order id
                        orderid = dbm.fetch_max_user_orderid(userid)['orderid']
                        if orderid:
                            # Insert products from cart into the order details
                            if dbm.insert_order_details(orderid, cartid):
                                # Update order total
                                if dbm.update_order_total(orderid):
                                    # Create a new cart to the user:
                                    dbm.create_user_cart(userid)
                                    # Update order status to placed
                                    dbm.update_order_status(1, orderid)
                                    # Fetch Order
                                    order = dbm.fetch_order(orderid,userid)
                                    if order:
                                        return jsonify(order)
            return internal_server_error()
    except Exception as e:
        print e
        return bad_request()


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
            payment_keys = post_payment_keys
            payment_keys.append('ppreferred')
            for key in payment_keys:
                if key not in request.json:
                    return missing_parameters_error()
            billing_addressid = dbm.fetch_user_preferences(userid)
            if billing_addressid:
                if dbm.insert_first_payment_method(card_name=request.json['cname'],
                                                   card_last_four_digits=request.json['cnumber'][-4:],
                                                   card_number=request.json['cnumber'],
                                                   card_exp_date=request.json['cexpdate'],
                                                   cvc=request.json['cvc'], card_type=request.json['ctype'],
                                                   userid=userid,
                                                   billing_addressid=billing_addressid):
                    # Get Payment Method id
                    new_payment_method = dbm.fetch_max_payment_methodid(userid)
                    set_preferred = request.json['ppreferred']
                    if set_preferred:
                        if not dbm.update_user_preferred_billing(new_payment_method['pid']):
                            return internal_server_error()
                    return jsonify(new_payment_method)
                return internal_server_error()
            else:
                return jsonify({'error': 'Preferred Billing Address Not Found For User {0}'.format(userid)}), 400
    except Exception as e:
        print e
        return internal_server_error()


@user_blueprint.route("/<int:userid>/payment/<payment_methodid>", methods=['PUT'])
@requires_auth
def update_payment(userid, payment_methodid):
    try:
        if request.json:
            payment_keys = post_payment_keys
            payment_keys.append('ppreferred')
            for key in payment_keys:
                if key not in request.json:
                    return missing_parameters_error()
            is_inactive = dbm.deactivate_user_payment_method(userid, payment_methodid)
            if is_inactive:
                billing_addressid = dbm.fetch_user_preferences(userid)
                if billing_addressid:
                    if dbm.insert_first_payment_method(card_name=request.json['cname'],
                                                       card_last_four_digits=request.json['cnumber'][-4:],
                                                       card_number=request.json['cnumber'],
                                                       card_exp_date=request.json['cexpdate'],
                                                       cvc=request.json['cvc'], card_type=request.json['ctype'],
                                                       userid=userid,
                                                       billing_addressid=billing_addressid):
                        # Get Payment Method id
                        new_payment_method = dbm.fetch_max_payment_methodid(userid)
                        set_preferred = request.json['ppreferred']
                        if set_preferred:
                            if not dbm.update_user_preferred_billing(new_payment_method['pid']):
                                return internal_server_error()
                        return jsonify(new_payment_method)
                    return internal_server_error()
                else:
                    return jsonify({'error': 'Preferred Billing Address Not Found For User {0}'.format(userid)}), 400
            return not_found()
        return bad_request()
    except Exception as e:
        print e
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
            is_inactive = dbm.deactivate_user_address(userid, addressid)
            if is_inactive:
                if dbm.insert_user_address(address_fullname=request.json['afullname'],
                                           address_line_1=request.json['aaddress1'],
                                           address_line_2=request.json['aaddress2'],
                                           address_city=request.json['acity'],
                                           address_zip=request.json['azip'],
                                           address_country=request.json['acountry'],
                                           address_state=request.json['astate'],
                                           userid=userid):
                    new_address = dbm.fetch_max_address(userid)
                    set_preferred = request.json['apreferred']
                    if set_preferred:
                        if request.json['atype'] == 'billing':
                            if not dbm.update_user_preferred_billing(new_address['aid']):
                                return internal_server_error()
                        elif request.json['atype'] == 'shipping':
                            if not dbm.update_user_preferred_shipping(new_address['aid']):
                                return internal_server_error()
                    return jsonify(new_address)

                else:
                    return internal_server_error()
            return not_found()
        return bad_request()
    except Exception as e:
        print e
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
            address_keys = post_address_keys
            address_keys.append('apreferred')
            address_keys.append('atype')
            for key in address_keys:
                if key not in request.json:
                    return missing_parameters_error()
            if dbm.insert_user_address(address_fullname=request.json['afullname'],
                                       address_line_1=request.json['aaddress1'],
                                       address_line_2=request.json['aaddress2'],
                                       address_city=request.json['acity'],
                                       address_zip=request.json['azip'],
                                       address_country=request.json['acountry'],
                                       address_state=request.json['astate'],
                                       userid=userid):
                new_address = dbm.fetch_max_address(userid)
                set_preferred = request.json['apreferred']
                if set_preferred:
                    if request.json['atype'] == 'billing':
                        if not dbm.update_user_preferred_billing(new_address['aid']):
                            return internal_server_error()
                    elif request.json['atype'] == 'shipping':
                        if not dbm.update_user_preferred_shipping(new_address['aid']):
                            return internal_server_error()
                return jsonify(new_address)
            else:
                return internal_server_error()
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
                # return jsonify({'message': 'Product {0} removed from user {1} wish list.'.format(productid, userid)})
                return jsonify(wish_list)
            else:
                not_found()
        elif request.method == 'POST':
            in_wish_list = dbm.wish_list_contains(productid=productid, userid=userid)['product_in_wishlist']
            if not in_wish_list:
                dbm.add_product_to_user_wishlist(productid=productid, userid=userid)
                wish_list = dbm.fetch_user_wish_list(userid=userid)
                # return jsonify({'message': 'Product {0} added to user {1} wish list.'.format(productid, userid)})
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
                if ('uname' and 'upassword' and 'ufirstname' and 'ulastname'
                    and 'uemail' and 'uphone' and 'udob' not in request.json):
                    return missing_parameters_error()
                # Verify that parameters are valid
                errors = validate_account(request.json)
                if errors:
                    return jsonify({'Errors': errors}), 400
                # Update user account:
                if dbm.update_user_account(username=request.json['uname'],
                                           upassword=request.json['upassword'],
                                           userid=userid):
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
                    return missing_parameters_error()
            for key in post_address_keys:
                if key not in request.json['ushippingaddress'] or key not in request.json['ubillingaddress']:
                    return missing_parameters_error()
            for key in post_payment_keys:
                if key not in request.json['upayment']:
                    return missing_parameters_error()
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
                # Insert user account:
                dbm.insert_account_info(username=request.json['uname'], upassword=request.json['upassword'])
                # Get account id
                accountid = dbm.fetch_accounid(username=request.json['uname'])['accountid']

                # Insert user information
                dbm.insert_personal_info(user_firstname=request.json['ufirstname'],
                                         user_lastname=request.json['ulastname'],
                                         email=request.json['uemail'],
                                         phone=request.json['uphone'],
                                         dob=request.json['udob'],
                                         accountid=accountid)
                # Get user id
                userid = dbm.fetch_userid(accountid)['userid']
                #  Insert Shipping Address
                shipping_address = request.json['ushippingaddress']
                dbm.insert_user_address(address_fullname=shipping_address['afullname'],
                                        address_line_1=shipping_address['aaddress1'],
                                        address_line_2=shipping_address['aaddress2'],
                                        address_city=shipping_address['acity'],
                                        address_zip=shipping_address['azip'],
                                        address_country=shipping_address['acountry'],
                                        address_state=shipping_address['astate'],
                                        userid=userid)
                # Get Address id
                shippin_addressid = dbm.fetch_min_address(userid)['aid']
                # Insert Billing Address
                billing_address = request.json['ubillingaddress']
                dbm.insert_user_address(address_fullname=billing_address['afullname'],
                                        address_line_1=billing_address['aaddress1'],
                                        address_line_2=billing_address['aaddress2'],
                                        address_city=billing_address['acity'],
                                        address_zip=billing_address['azip'],
                                        address_country=billing_address['acountry'],
                                        address_state=billing_address['astate'],
                                        userid=userid)
                # Get Address id
                billing_addressid = dbm.fetch_max_address(userid)['aid']
                # Insert Payment Method
                payment_method = request.json['upayment']
                dbm.insert_first_payment_method(card_name=payment_method['cname'],
                                                card_last_four_digits=payment_method['cnumber'][-4:],
                                                card_number=payment_method['cnumber'],
                                                card_exp_date=payment_method['cexpdate'],
                                                cvc=payment_method['cvc'], card_type=payment_method['ctype'],
                                                userid=userid,
                                                billing_addressid=billing_addressid)
                # Get Payment Method id
                payment_method = dbm.fetch_user_payment_methods(userid)[0]['cid']
                # Insert User Preferences
                dbm.insert_user_preferences(userid=userid,
                                            shipping_addressid=shippin_addressid,
                                            billing_addressid=billing_addressid,
                                            payment_methodid=payment_method)
                # Return user response
                cg_user = dbm.fetch_user_info(userid=userid)
                return jsonify(cg_user), 201
        else:
            bad_request()
    except Exception as e:
        print e
        return internal_server_error()


@user_blueprint.route("/login", methods=['POST'])
def get_user_id():
    if request.json:
        try:
            uid = dbm.fetch_user_accountid(request.json['uname'], request.json['upassword'])
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
        return missing_parameters_error()


def validate_account(data):
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

    # A Password must contain atleast an Upper case leter and a number
    has_upper = re.search('[A-Z]+', data['upassword'])
    has_digit = re.search('[\d]+', data['upassword'])
    # A Password must be 8 characters to 20 characters long
    if len(str(data['upassword'])) < 8 or len(str(data['upassword'])) > 20 or not has_upper or not has_digit:
        errors.append('Invalid password.')

    # Email regex for python
    is_email = re.search(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", data['uemail'])
    if not is_email:
        errors.append('Invalid email.')

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
    is_valid_cc = re.search(cc_regex, data['cnumber'])
    if not is_valid_cc:
        errors.append('Invalid Credit Card.')

    # Validate with Date regex for python
    is_date = re.search(r'^(\d{4}\-\d{2}\-\d{2})$', data['cexpdate'])
    if is_date:
        # Verify that is not expired
        not_expired = dbm.validate_exp_date(data['cexpdate'])['valid_exp_date']
        if not not_expired:
            errors.append('Invalid Expiration Date.')
    else:
        errors.append('Invalid Expiration Date.')

    # Validate CVC
    is_digit = re.search(r'^([\d]+)$', data['cvc'])
    if len(str(data['cvc'])) < 3 or len(str(data['cvc'])) > 4 or not is_digit:
        errors.append('Invalid CVC.')

    # Validate Card Type
    valid_cc = dbm.validate_cc(data['ctype'])['valid_cc']
    if not valid_cc:
        errors.append('Invalid Last Name.')

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


def missing_parameters_error():
    return jsonify({'Error': "Missing Parameters in Request JSON."}), 400


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




