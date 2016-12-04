import os
import psycopg2
import urlparse
import QueryManager as Query


DEC2FLOAT = psycopg2.extensions.new_type(
        psycopg2.extensions.DECIMAL.values,
        'DEC2FLOAT',
        lambda value, curs: float(value) if value is not None else None)

psycopg2.extensions.register_type(DEC2FLOAT)

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)
psycopg2.extensions.register_type(psycopg2.extensions.UNICODEARRAY)

urlparse.uses_netloc.append("postgres")
__url__ = urlparse.urlparse(os.environ["DATABASE_URL"])


def __connection__():
    """
    Returns a psycopg2 connection to the url stored in environment variable DATABASE_URL
    :return: psycopg2 connection
    """
    conn = psycopg2.connect(
        database=__url__.path[1:],
        user=__url__.username,
        password=__url__.password,
        host=__url__.hostname,
        port=__url__.port
    )
    return conn


def __execute_select_query__(query, parameters):
    """
    Executes a 'SELECT' query
    :param query: SQL Statement
    :param parameters: Tuple of query parameters
    :return: Query result
    """
    try:
        conn = __connection__()
        cur = conn.cursor()
        cur.execute(query, parameters)
        # List of columns
        columns = [x[0] for x in cur.description]

        results = []

        # Convert rows into a dictionary
        for row in cur.fetchall():
            results.append(dict(zip(columns, row)))

        conn.close()
        return results
    except Exception as e:
        print e


def __execute_select_product_query__(query, parameters):
    """
    Execute SELECT Query for Products Only
    :param query: string SQL statement
    :param parameters: Tuple of query parameters
    :return: Query Result
    """
    try:
        conn = __connection__()
        cur = conn.cursor()
        cur.execute(query, parameters)
        # List of columns
        columns = [x[0] for x in cur.description]

        results = []

        # Convert rows into a dictionary
        for row in cur.fetchall():
            results.append(dict(zip(columns, row)))

        if results:
            # Encode unicode special characters into xml special characters
            # This is done because the content will be displayed in an html client
            for e in results:
                e['description'] = e['description'].encode('ascii', 'xmlcharrefreplace').replace('\n', '<br />')
                e['aditionalinfo'] = e['aditionalinfo'].encode('ascii', 'xmlcharrefreplace').replace('\n', '<br />')

        conn.close()
        return results
    except Exception as e:
        print e


def __execute_commit_query__(query, parameters):
    """
    Executes a transaction query
    :param query: string SQL Statement
    :param parameters: tuple of query parameters
    :return: True if transaction was performed, False if transaction failed.
    """
    try:
        conn = __connection__()
        cur = conn.cursor()
        cur.execute(query, parameters)
        # List of columns
        columns = [x[0] for x in cur.description]
        # Convert rows into a dictionary
        results = [dict(zip(columns, row)) for row in cur.fetchall()]
        conn.commit()
        conn.close()
        return results
    except Exception as e:
        if conn:
            if not conn.closed:
                conn.rollback()
                conn.close()
        print e.message
        raise


def fetch_special_products():
    return __execute_select_product_query__(Query.SELECT_SPECIAL_PRODUCTS, ())


def fetch_platform_special_products(productid):
    return __execute_select_query__(Query.SELECT_PLATFORM_SPECIAL_PRODUCTS, (productid,))


def fetch_latest_products():
    return __execute_select_query__(Query.SELECT_LATEST_PRODUCTS, ())


def fetch_platforms():
    try:

        conn = __connection__()
        cur = conn.cursor()
        cur.execute(Query.SELECT_PLATFORMS)

        columns = [x[0] for x in cur.description]
        results = []

        for row in cur.fetchall():
            results.append(dict(zip(columns, row)))

        for r in results:
            cur.execute(Query.SELECT_PLATFORM_CONSOLES, (r['platformid'],))
            columns = [x[0] for x in cur.description]
            r['consoles'] = []
            for row in cur.fetchall():
                r['consoles'].append(dict(zip(columns, row)))

        for r in results:
            cur.execute(Query.SELECT_PLATFORM_ACCESORIES, (r['platformid'],))
            r['accesories'] = []
            for row in cur.fetchall():
                r['accesories'].append(str(row[0]))

        for r in results:
            cur.execute(Query.SELECT_PLATFORM_GAME_GENRES, (r['platformid'],))
            r['gamegen'] = []
            for row in cur.fetchall():
                r['gamegen'].append(str(row[0]))

        #for e in results:
            #print e
        conn.close()
        return results
    except Exception as e:
        print e


def fetch_product(productid):
    return __execute_select_product_query__(Query.SELECT_PRODUCT_DETAILS, (productid,))[0]

def fetch_all_products():
    return __execute_select_product_query__(Query.SELECT_ALL_PRODUCTS, ())


def fetch_platform_latest_products(platformid):
    return __execute_select_product_query__(Query.SELECT_PLATFORM_LATEST_PRODUCTS, (platformid,))


def fetch_platform_special_products(platformid):
    return __execute_select_product_query__(Query.SELECT_PLATFORM_SPECIAL_PRODUCTS, (platformid,))


def fetch_platform_announcements(platformid):
    return __execute_select_query__(Query.SELECT_PLATFORM_ANNOUNCEMENTS, (platformid,))


def fetch_store_announcements():
    return __execute_select_query__(Query.SELECT_STORE_ANNOUNCEMENT, ())


def insert_product_rating(productid, rate):
   return __execute_commit_query__(Query.INSERT_PRODUCT_RATING, (productid, rate))


def authenticate_user(username, userid, password):
    try:
        conn = __connection__()
        cur = conn.cursor()
        cur.execute(Query.AUTHENTICATE_USER_WITH_ID, (username, userid, password))
        results = cur.fetchall()

        print results

        conn.close()
        return results
    except Exception as e:
        print e


def fetch_user_info(userid):
    return __execute_select_query__(Query.SELECT_USER, (userid,))[0]


def fetch_user_wish_list(userid):
    return __execute_select_query__(Query.SELECT_USER_WISH_LIST, (userid,))


def fetch_user_address(userid):
    return __execute_select_query__(Query.SELECT_USER_ADDRESS, (userid,))


def fetch_user_payment_methods(userid):
    return __execute_select_query__(Query.SELECT_USER_CREDIT_CARD, (userid,))


def fetch_user_cart(userid):
    return __execute_select_query__(Query.SELECT_USER_CART, (userid,))


def update_user_account(username, upassword, userid):
    return __execute_commit_query__(Query.UPDATE_USER_ACCOUNT, (username, upassword, userid))


def update_cart_product_qty(product_qty, productid, userid):
    return __execute_commit_query__(Query.UPDATE_USER_CART, (product_qty, productid, userid))


def deactivate_user_cart(cartid, userid):
    return __execute_commit_query__(Query.UPDATE_USER_CART_TO_INACTIVE, (cartid, userid))


def deactivate_user_payment_method(userid, payment_methodid):
    return __execute_commit_query__(Query.UPDATE_USER_PAYMENT_METHOD_TO_INACTIVE, (userid, payment_methodid))


def insert_user_payment_method(card_name, card_last_four_digits, card_number, card_exp_date, cvc, card_type, userid):
    return __execute_commit_query__(Query.INSERT_USER_PAYMENT_METHOD_USING_PREF, (card_name, card_last_four_digits, card_number, card_exp_date, cvc, card_type, userid, userid))


def create_user_cart(userid):
    return __execute_commit_query__(Query.INSERT_AN_USER_CART, (userid,))


def add_product_to_user_wishlist(productid, userid):
    return __execute_commit_query__(Query.INSERT_PRODUCT_INTO_WISH_LIST, (productid, userid))


def update_user_info(user_firstname, user_lastname, email, phone, dob, userid):
    print user_firstname, user_lastname, email, phone, dob, userid
    return __execute_commit_query__(Query.UPDATE_USER, (user_firstname, user_lastname, email, phone, dob, userid))


def add_product_to_cart(cartid, productid, product_qty):
    return __execute_commit_query__(Query.INSERT_PRODUCT_INTO_CART, (cartid, productid, product_qty))


def deactivate_user_address(userid, addressid):
    return __execute_commit_query__(Query.UPDATE_USER_ADDRESS_TO_INACTIVE, (userid, addressid))


def insert_user_address(address_fullname, address_line_1, address_line_2, address_city, address_zip, address_country, address_state, userid):
    return __execute_commit_query__(Query.INSERT_USER_ADDRESS, (address_fullname, address_line_1, address_line_2, address_city, address_zip, address_country, address_state, userid))


def fetch_user_id(username, password):
    return __execute_select_query__(Query.AUTHENTICATE_USER_WITHOUT_ID, (password, username))


def fetch_user_cartid(userid):
    return __execute_select_query__(Query.SELECT_USER_CARTID, (userid,))[0]


def remove_product_from_cart(userid, productid):
    return __execute_commit_query__(Query.DELETE_PRODUCT_FROM_CART, (userid, productid))


def cart_contains(productid, cartid):
    return __execute_select_query__(Query.CART_CONTAINS, (productid, cartid))[0]


def remove_from_wish_list(productid,userid):
    return __execute_commit_query__(Query.DELETE_PRODUCT_FROM_WISH_LIST, (productid, userid))


def wish_list_contains(productid, userid):
    return __execute_select_query__(Query.WISH_LIST_CONTAINS, (productid, userid))[0]


def user_account_exist(username, email):
    return __execute_select_query__(Query.EXISTING_ACCOUNT, (username, email))[0]


def insert_account_info(username, upassword):
    return __execute_commit_query__(Query.INSERT_ACCOUNT_INFO, (username, upassword))


def fetch_accounid(username):
    return __execute_select_query__(Query.SELECT_ACCOUNTID, (username))[0]


def insert_personal_info(user_firstname, user_lastname, email, phone, dob, accountid):
    return __execute_commit_query__(Query.INSERT_USER, (user_firstname, user_lastname, email, phone, dob, accountid))


def fetch_userid(accountid):
    return __execute_select_query__(Query.SELECT_USERID, (accountid,))[0]


def fetch_min_address(userid):
    return __execute_select_query__(Query.SELECT_MIN_ADDRESS_ID, (userid,))[0]


def fetch_max_address(userid):
    return __execute_select_query__(Query.SELECT_MAX_ADDRESS_ID, (userid,))[0]


def insert_first_payment_method(card_name, card_last_four_digits, card_number, card_exp_date, cvc, card_type, userid, billing_addressid):
    return __execute_commit_query__(Query.INSERT_USER_PAYMENT_METHOD,
                                    (card_name, card_last_four_digits, card_number,
                                     card_exp_date, cvc, card_type, userid, billing_addressid))[0]


def insert_user_preferences(userid, shipping_addressid, billing_addressid, payment_methodid):
    return __execute_commit_query__(Query.INSERT_USER_PREFERENCES, (userid, shipping_addressid, billing_addressid, payment_methodid))


def validate_cc(card_type):
    return __execute_select_query__(Query.VALIDATE_CC, (card_type,))[0]


def validate_exp_date(date):
    return __execute_select_query__(Query.VALIDATE_EXP_DATE, (date,))[0]


def fetch_order(orderid, userid):
        order = __execute_select_query__(Query.SELECT_ORDER, (orderid, userid))[0]
        if order:
            products = __execute_select_query__(Query.SELECT_ORDER_PRODUCTS, (orderid,))
            order['oproducts'] = products
            order['shipping_address'] = __execute_select_query__(Query.SELECT_USER_ADDRESS_ID, (userid, order['shipping_addressid'],))[0]
            order['billing_address'] = __execute_select_query__(Query.SELECT_USER_ADDRESS_ID, (userid, order['billing_addressid'],))[0]
            order['payment_method'] = __execute_select_query__(Query.SELECT_USER_PAYMENT_BY_ID, (userid, order['cid']))[0]
            order.pop('shipping_addressid', None)
            order.pop('billing_addressid', None)
            order.pop('cid', None)
        return order


def fetch_user_orders(userid):
    orders = __execute_select_query__(Query.SELECT_USER_ORDERS, (userid,))
    if orders:
        for order in orders:
            products = __execute_select_query__(Query.SELECT_ORDER_PRODUCTS, (order['oid'],))
            order['oproducts'] = products
            order['shipping_address'] = __execute_select_query__(
                Query.SELECT_USER_ADDRESS_ID, (userid, order['shipping_addressid'],))[0]
            order['billing_address'] = __execute_select_query__(
                Query.SELECT_USER_ADDRESS_ID, (userid, order['billing_addressid'],))[0]
            order['payment_method'] = __execute_select_query__(Query.SELECT_USER_PAYMENT_BY_ID, (userid, order['cid']))[0]
            order.pop('shipping_addressid', None)
            order.pop('billing_addressid', None)
            order.pop('cid', None)
    return orders


def update_user_preferred_billing(addressid, userid):
    return __execute_commit_query__(Query.UPDATE_USER_PREFERRED_BILLING_ADDR, (addressid, userid))


def update_user_preferred_shipping(addressid, userid):
    return __execute_commit_query__(Query.UPDATE_USER_PREFERRED_SHIPPING_ADDR, (addressid, userid))


def update_user_preferred_payment(payment_methodid, userid):
    return __execute_commit_query__(Query.UPDATE_USER_PREFERRED_PAYMENT, (payment_methodid, userid))


def fetch_user_preferences(userid):
    preferences = __execute_select_query__(Query.SELECT_USER_PREFERENCES, (userid,))[0]
    if preferences:
        preferences['shipping_address'] = __execute_select_query__(
            Query.SELECT_USER_ADDRESS_ID, (userid, preferences['shipping_addressid']))[0]
        preferences['billing_address'] = __execute_select_query__(
            Query.SELECT_USER_ADDRESS_ID, (userid, preferences['billing_addressid']))[0]
        preferences['payment_method'] = __execute_select_query__(
            Query.SELECT_USER_PAYMENT_BY_ID, (userid, preferences['payment_methodid']))[0]
        preferences.pop('shipping_addressid', None)
        preferences.pop('billing_addressid', None)
        preferences.pop('payment_methodid', None)
        preferences.pop('userid', None)
    return preferences


def fetch_max_payment_methodid(userid):
    return __execute_select_query__(Query.SELECT_USER_MAX_PAYMENT_ID, (userid,))


def search_products_by_title(title):
    return __execute_select_product_query__(Query.SELECT_SEARCH_TITLE, ('%{0}%'.format(title),))

def advanced_search(platform,genre,category):
    return __execute_select_product_query__(Query.SELECT_SEARCH_NAVBAR, (platform, genre, category))


def insert_empty_order(cartid, shippment_feeid, shipping_addressid, userid, payment_methodid):
    return __execute_commit_query__(Query.INSERT_EMPTY_ORDER, (cartid, shippment_feeid, shipping_addressid, userid, payment_methodid))


def insert_order_details(orderid, cartid):
    return __execute_commit_query__(Query.INSERT_ORDER_DETAILS, (orderid, cartid))


def fetch_max_user_orderid(userid):
    return __execute_select_query__(Query.SELECT_USER_MAX_ORDER_ID, (userid,))[0]


def update_order_total(orderid):
    return __execute_commit_query__(Query.UPDATE_ORDER_TOTAL, (orderid, orderid))


def validate_shipment_fee(shfeeid):
    return __execute_select_query__(Query.VALIDATE_SHIPMENT_FEE, (shfeeid,))[0]


def validate_address(aid, userid):
    return __execute_select_query__(Query.VALIDATE_ADDRESS_ID, (aid,userid))[0]


def validate_payment(cid, userid):
    return __execute_select_query__(Query.VALIDATE_PAYMENT_ID, (cid, userid))[0]


def update_order_status(order_statusid, orderid):
    return __execute_commit_query__(Query.UPDATE_ORDER_SATUS, (order_statusid, orderid))


def fetch_shipment_fees():
    return __execute_select_query__(Query.SELECT_SHIPMENT_FEE, ())


def fetch_user_billing_address(userid):
    return __execute_select_query__(Query.SELECT_USER_BILLING_ADDRESS, (userid,))


def fetch_user_shipping_address(userid):
    return __execute_select_query__(Query.SELECT_USER_SHIPPING_ADDRESS, (userid,))


def fetch_store_genres():
    dict = __execute_select_query__(Query.SELECT_STORE_GENRES, ())
    result = []
    for e in dict:
        result.append(e['genre'])
    return result


def fetch_related_products(pid):
    return __execute_select_query__(Query.SELECT_RELATED_PRODUCTS, (pid, pid))


def fetch_home_top():
    return __execute_select_query__(Query.SELECT_HOME_TOP_PRODUCTS, ())


def fetch_platform_top(platformid):
    return __execute_select_query__(Query.SELECT_PLATFORM_TOP_PRODUCTS, (platformid,))


def authenticate_admin(username, password):
    try:
        conn = __connection__()
        cur = conn.cursor()
        cur.execute(Query.AUTHENTICATE_ADMIN_USER, (password, username))
        results = cur.fetchall()
        conn.close()
        return results
    except Exception as e:
        print e


def fetch_users():
    return __execute_select_query__(Query.SELECT_USERS, ())


def fetch_product_alt_img(pid):
    return __execute_select_query__(Query.SELECT_PRODUCT_ALT_IMGS, (pid,))

"""
Multi Transactions:
"""
def register_user(user_data):
    """
    Register a new user in a single transaction
    :param user_data: user data in request.json
    :return: user id
    """
    try:
        conn = __connection__()
        cur = conn.cursor()
        # Insert account info returning the account id
        cur.execute(Query.INSERT_ACCOUNT_INFO, (user_data['uname'], user_data['upassword']))
        columns = [x[0] for x in cur.description]
        accountid = [dict(zip(columns, row)) for row in cur.fetchall()][0]
        # Insert the user info with the resulting account id
        cur.execute(Query.INSERT_USER, (user_data['ufirstname'], user_data['ulastname'], user_data['uemail'], user_data['uphone'], user_data['udob'], accountid['accountid']))
        columns = [x[0] for x in cur.description]
        userid = [dict(zip(columns, row))  for row in cur.fetchall()][0]
        # Insert the user shipping address with the resulting user id
        shipping_address = user_data['ushippingaddress']
        cur.execute(Query.INSERT_USER_ADDRESS,
                    (shipping_address['afullname'], shipping_address['aaddress1'], shipping_address['aaddress2'],
                     shipping_address['acity'], shipping_address['azip'], shipping_address['acountry'],
                     shipping_address['astate'], userid['userid']))
        columns = [x[0] for x in cur.description]
        shipping_addressid  = [dict(zip(columns, row)) for row in cur.fetchall()][0]
        # Insert the user billing address with the resulting user id
        billing_address = user_data['ubillingaddress']
        cur.execute(Query.INSERT_USER_ADDRESS,
                    (billing_address['afullname'], billing_address['aaddress1'], billing_address['aaddress2'],
                     billing_address['acity'], billing_address['azip'], billing_address['acountry'],
                     billing_address['astate'], userid['userid']))
        columns = [x[0] for x in cur.description]
        billing_addressid = [dict(zip(columns, row))  for row in cur.fetchall()][0]
        # Insert Payment Method with the resulting user id and billing address id
        payment_method = user_data['upayment']
        cur.execute(Query.INSERT_USER_PAYMENT_METHOD,
                    (payment_method['cname'], payment_method['cnumber'][-4:], payment_method['cnumber'],
                     payment_method['cexpdate'], payment_method['cvc'], payment_method['ctype'], userid['userid'], billing_addressid['addressid']))
        columns = [x[0] for x in cur.description]
        payment_methodid = [dict(zip(columns, row))  for row in cur.fetchall()][0]
        cur.execute(Query.INSERT_USER_PREFERENCES, (userid['userid'], shipping_addressid['addressid'], billing_addressid['addressid'], payment_methodid['payment_methodid']))
        # Create Empty Cart for the new user
        cur.execute(Query.INSERT_AN_USER_CART, (userid['userid'],))
        conn.commit()
        cur.close()
        conn.close()
        return userid['userid']
    except:
        if conn:
            if not conn.closed:
                conn.rollback()
                conn.close()
        raise


def process_order(userid, order_data):
    """
    Place order from user cart
    :param userid: user id
    :param order_data: request order data
    :return: order id
    """
    try:
        conn = __connection__()
        cur = conn.cursor()
        # Deactivate cart to avoid errors
        cur.execute(Query.SELECT_USER_CARTID, (userid,))
        columns = [x[0] for x in cur.description]
        cartid = [dict(zip(columns, row)) for row in cur.fetchall()][0]['cartid']
        cur.execute(Query.UPDATE_USER_CART_TO_INACTIVE, (cartid, userid))
        # Create an empty order
        cur.execute(Query.INSERT_EMPTY_ORDER, (cartid, order_data['shipment_feeid'], order_data['aid'], userid, order_data['cid']))
        columns = [x[0] for x in cur.description]
        orderid = [dict(zip(columns, row)) for row in cur.fetchall()][0]['orderid']
        # Insert products from cart into the order details
        cur.execute(Query.INSERT_ORDER_DETAILS, (orderid, cartid))
        # Update order total
        cur.execute(Query.UPDATE_ORDER_TOTAL, (orderid, orderid))
        # Create a new cart to the user
        cur.execute(Query.INSERT_AN_USER_CART, (userid,))
        # Update order status to placed
        placed = 1
        cur.execute(Query.UPDATE_ORDER_SATUS, (placed, orderid))
        conn.commit()
        cur.close()
        conn.close()
        return orderid
    except:
        if conn:
            if not conn.closed:
                conn.rollback()
                conn.close()
        raise


def update_user_password(accountid, upassword):
    """
    Update User Password
    :param accountid:
    :param upassword:
    :return:
    """
    return __execute_commit_query__(Query.UPDATE_USER_PASSWORD, (accountid, upassword))






def update_payment_method(userid, payment_methodid, card_data, billing_addressid):
    """
    Update Payment Method
    :param userid: user id
    :param payment_methodid: payment method id
    :param card_data: card data
    :param billing_addressid: billing address id
    :return:
    """
    try:
        conn = __connection__()
        cur = conn.cursor()
        # Deactivate given card to avoid errors
        cur.execute(Query.UPDATE_USER_PAYMENT_METHOD_TO_INACTIVE, (userid, int(payment_methodid)))
        updated = cur.fetchall()
        if not updated:
            raise Exception("Invalid Payment.")
        # Create an new card
        cur.execute(Query.INSERT_USER_PAYMENT_METHOD,
                                    (card_data['cname'], card_data['cnumber'][-4:], card_data['cnumber'],
                                     card_data['cexpdate'], card_data['cvc'], card_data['ctype'],
                                     userid, billing_addressid))
        columns = [x[0] for x in cur.description]
        cid = [dict(zip(columns, row)) for row in cur.fetchall()][0]['payment_methodid']
        # Verify if it is preferred payment
        set_preferred = card_data['ppreferred']
        if set_preferred:
            cur.execute(Query.UPDATE_USER_PREFERRED_PAYMENT, (cid, userid))
        conn.commit()
        cur.close()
        conn.close()
        return cid
    except:
        if conn:
            if not conn.closed:
                conn.rollback()
                conn.close()
        raise


def update_user_address(userid, addressid, address_data):
    """
    Update given address
    :param userid: user id
    :param addressid: address id
    :param address_data: address data
    :return: new address id
    """
    try:
        conn = __connection__()
        cur = conn.cursor()
        # Deactivate given address to avoid errors
        cur.execute(Query.UPDATE_USER_ADDRESS_TO_INACTIVE, (userid, addressid))
        columns = [x[0] for x in cur.description]
        updated = [dict(zip(columns, row)) for row in cur.fetchall()]
        if not updated:
            raise Exception("Invalid Address.")
        # Create an new address
        cur.execute(Query.INSERT_USER_ADDRESS,
                    (address_data['afullname'], address_data['aaddress1'], address_data['aaddress2'],
                     address_data['acity'], address_data['azip'], address_data['acountry'],
                     address_data['astate'], userid))
        columns = [x[0] for x in cur.description]
        addressid = [dict(zip(columns, row)) for row in cur.fetchall()][0]['addressid']
        # Verify if it's going to be a preferred address
        set_preferred = address_data['apreferred']
        if set_preferred:
            if address_data['atype'] == 'billing':
                cur.execute(Query.UPDATE_USER_PREFERRED_BILLING_ADDR, (addressid, userid))
            elif address_data['atype'] == 'shipping':
                cur.execute(Query.UPDATE_USER_PREFERRED_SHIPPING_ADDR, (addressid, userid))
        conn.commit()
        cur.close()
        conn.close()
        return addressid
    except:
        if conn:
            if not conn.closed:
                conn.rollback()
                conn.close()
        raise


def create_user_payment_method(userid, card_data, billing_addressid):
    """
    Create a new payment method
    :param userid: user id
    :param card_data: card data
    :param billing_addressid: billing address
    :return: payment method id
    """
    try:
        conn = __connection__()
        cur = conn.cursor()
        # Create an new card
        cur.execute(Query.INSERT_USER_PAYMENT_METHOD,
                                    (card_data['cname'], card_data['cnumber'][-4:], card_data['cnumber'],
                                     card_data['cexpdate'], card_data['cvc'], card_data['ctype'],
                                     userid, billing_addressid))
        columns = [x[0] for x in cur.description]
        cid = [dict(zip(columns, row)) for row in cur.fetchall()][0]['payment_methodid']
        # Verify if it is preferred payment
        set_preferred = card_data['ppreferred']
        if set_preferred:
            cur.execute(Query.UPDATE_USER_PREFERRED_PAYMENT, (cid, userid))
        conn.commit()
        cur.close()
        conn.close()
        return cid
    except:
        if conn:
            if not conn.closed:
                conn.rollback()
                conn.close()
        raise


def create_user_address(userid, address_data):
    """
    Create a new address
    :param userid: user id
    :param address_data: address data
    :return: address id
    """
    try:
        conn = __connection__()
        cur = conn.cursor()
        # Create an new address
        cur.execute(Query.INSERT_USER_ADDRESS,
                    (address_data['afullname'], address_data['aaddress1'], address_data['aaddress2'],
                     address_data['acity'], address_data['azip'], address_data['acountry'],
                     address_data['astate'], userid))
        columns = [x[0] for x in cur.description]
        addressid = [dict(zip(columns, row)) for row in cur.fetchall()][0]['addressid']
        # Verify if it's going to be a preferred address
        set_preferred = address_data['apreferred']
        if set_preferred:
            if address_data['atype'] == 'billing':
                cur.execute(Query.UPDATE_USER_PREFERRED_BILLING_ADDR, (addressid, userid))
            elif address_data['atype'] == 'shipping':
                cur.execute(Query.UPDATE_USER_PREFERRED_SHIPPING_ADDR, (addressid, userid))
        conn.commit()
        cur.close()
        conn.close()
        return addressid
    except:
        if conn:
            if not conn.closed:
                conn.rollback()
                conn.close()
        raise


def deactivate_user(accountid):
    """
    Deactivate user account
    :param userid: user id
    :return: las record updated
    """
    try:
        conn = __connection__()
        cur = conn.cursor()
        cur.execute(Query.DEACTIVATE_USER, (accountid,))
        columns = [x[0] for x in cur.description]
        aid = [dict(zip(columns, row)) for row in cur.fetchall()][0]['accountid']
        cur.execute(Query.DEACTIVATE_ACCOUNT, (aid,))
        columns = [x[0] for x in cur.description]
        done = [dict(zip(columns, row)) for row in cur.fetchall()]
        return done
    except:
        if conn:
            if not conn.closed:
                conn.rollback()
                conn.close()
        raise

def deactivate_platform(platformid):
    """
    Deactivate platform
    :param platformid: platform id
    :return: las record updated
    """
    try:
        conn = __connection__()
        cur = conn.cursor()
        cur.execute(Query.DEACTIVATE_PLATFORM, (platformid,))
        columns = [x[0] for x in cur.description]
        done = [dict(zip(columns, row)) for row in cur.fetchall()]
        return done
    except:
        if conn:
            if not conn.closed:
                conn.rollback()
                conn.close()
        raise


def add_admin_user(user_data):
    """

    :param user_data:
    :return:
    """
    try:
        conn = __connection__()
        cur = conn.execute(Query.INSERT_ADMIN_USER, (user_data['uname'], user_data['upassword']))
        columns = [x[0] for x in cur.description]
        aid = [dict(zip(columns, row)) for row in cur.fetchall()][0]['accountid']
        # Add user information
        cur.execute(Query.INSERT_USER,
                    (user_data['ufirstname'], user_data['ulastname'],
                     user_data['uemail'], user_data['uphone'], user_data['udob'],
                     aid))
        columns = [x[0] for x in cur.description]
        result = [dict(zip(columns, row)) for row in cur.fetchall()][0]['accountid']
        return result
    except:
        if conn:
            if not conn.closed:
                conn.rollback()
                conn.close()
        raise


def fetch_all_orders():
    return __execute_select_query__(Query.SELECT_ALL_ORDERS, ())

def fetch_esrb_ratings():
    return __execute_select_query__(Query.SELECT_ESRB_RATING, ())

def fetch_all_platforms():
    return __execute_select_query__(Query.SELECT_ALL_PLATFORMS, ())

def fetch_all_categories():
    return __execute_commit_query__(Query.SELECT_ALL_CATEGORIES, ())

def fetch_all_announcements():
    return __execute_commit_query__(Query.SELECT_ALL_ANNOUNCEMENTS, ())







