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
    conn = psycopg2.connect(
        database=__url__.path[1:],
        user=__url__.username,
        password=__url__.password,
        host=__url__.hostname,
        port=__url__.port
    )
    return conn


def __execute_select_query__(query):
    try:
        conn = __connection__()
        cur = conn.cursor()
        cur.execute(query)
        # List of columns
        columns = [x[0] for x in cur.description]

        results = []

        # Convert rows into a dictionary
        for row in cur.fetchall():
            results.append(dict(zip(columns, row)))

        # Encode unicode special characters into xml special characters
        # This is done because the content will be displayed in an html client
        for e in results:
            #e = dict((k, v.encode('ascii', 'xmlcharrefreplace').replace('\n', '<br />')) for (k, v) in e.items())
            print e

        conn.close()
        return results
    except Exception as e:
        print e


def __execute_select_product_query__(query):
    try:
        conn = __connection__()
        cur = conn.cursor()
        cur.execute(query)
        # List of columns
        columns = [x[0] for x in cur.description]

        results = []

        # Convert rows into a dictionary
        for row in cur.fetchall():
            results.append(dict(zip(columns, row)))

        # Encode unicode special characters into xml special characters
        # This is done because the content will be displayed in an html client
        for e in results:
            e['description'] = e['description'].encode('ascii', 'xmlcharrefreplace').replace('\n', '<br />')
            e['aditionalinfo'] = e['aditionalinfo'].encode('ascii', 'xmlcharrefreplace').replace('\n', '<br />')
            print e

        conn.close()
        return results
    except Exception as e:
        print e


def __execute_commit_query__(query):
    try:
        conn = __connection__()
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print e
        return False


def fetch_special_products():
    return __execute_select_product_query__(Query.SELECT_SPECIAL_PRODUCTS)


def fetch_platform_special_products(productid):
    return __execute_select_query__(Query.SELECT_PLATFORM_SPECIAL_PRODUCTS.format(productid))


def fetch_latest_products():
    return __execute_select_query__(Query.SELECT_LATEST_PRODUCTS)


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
            cur.execute(Query.SELECT_PLATFORM_CONSOLES.format(r['platformid']))
            columns = [x[0] for x in cur.description]
            r['consoles'] = []
            for row in cur.fetchall():
                r['consoles'].append(dict(zip(columns, row)))

        for r in results:
            cur.execute(Query.SELECT_PLATFORM_ACCESORIES.format(r['platformid']))
            r['accesories'] = []
            for row in cur.fetchall():
                r['accesories'].append(str(row[0]))

        for r in results:
            cur.execute(Query.SELECT_PLATFORM_GAME_GENRES.format(r['platformid']))
            r['gamegen'] = []
            for row in cur.fetchall():
                r['gamegen'].append(str(row[0]))

        for e in results:
            print e
        conn.close()
        return results
    except Exception as e:
        print e


def fetch_product(productid):
    return __execute_select_product_query__(Query.SELECT_PRODUCT_DETAILS.format(productid))[0]


def fetch_platform_latest_products(platformid):
    return __execute_select_product_query__(Query.SELECT_PLATFORM_LATEST_PRODUCTS.format(platformid))


def fetch_platform_special_products(platformid):
    return __execute_select_product_query__(Query.SELECT_PLATFORM_SPECIAL_PRODUCTS.format(platformid))


def fetch_platform_announcements(platformid):
    return __execute_select_query__(Query.SELECT_PLATFORM_ANNOUNCEMENTS.format(platformid))


def fetch_store_announcements():
    return __execute_select_query__(Query.SELECT_STORE_ANNOUNCEMENT)


def insert_product_rating(productid, rate):
   return __execute_commit_query__(Query.INSERT_PRODUCT_RATING.format(productid, rate))


def authenticate_user(username, userid, password):
    try:
        conn = __connection__()
        cur = conn.cursor()
        cur.execute(Query.AUTHENTICATE_USER_WITH_ID.format(username, userid, password))
        results = cur.fetchall()

        print results

        conn.close()
        return results
    except Exception as e:
        print e


def fetch_user_info(userid):
    return __execute_select_query__(Query.SELECT_USER.format(userid))[0]


def fetch_user_wish_list(userid):
    return __execute_select_query__(Query.SELECT_USER_WISH_LIST.format(userid))


def fetch_user_address(userid):
    return __execute_select_query__(Query.SELECT_USER_ADDRESS.format(userid))


def fetch_user_payment_methods(userid):
    return __execute_select_query__(Query.SELECT_USER_CREDIT_CARD.format(userid))


def fetch_user_cart(userid):
    return __execute_select_query__(Query.SELECT_USER_CART.format(userid))


def update_user_account(username, upassword, userid):
    return __execute_commit_query__(Query.UPDATE_USER_ACCOUNT.format(username, upassword, userid))


def update_cart_product_qty(product_qty, productid, userid):
    return __execute_commit_query__(Query.UPDATE_USER_CART.format(product_qty, productid, userid))


def deactivate_user_cart(cartid, userid):
    return __execute_commit_query__(Query.UPDATE_USER_CART_TO_INACTIVE.format(cartid, userid))


def deactivate_user_payment_method(userid, payment_methodid):
    return __execute_commit_query__(Query.UPDATE_USER_PAYMENT_METHOD_TO_INACTIVE.format(userid, payment_methodid))


def insert_user_payment_method(card_name, card_last_four_digits, card_number, card_exp_date, cvc, card_type, userid):
    return __execute_commit_query__(Query.INSERT_USER_PAYMENT_METHOD_USING_PREF.format(card_name, card_last_four_digits, card_number, card_exp_date, cvc, card_type, userid, userid))


def create_user_cart(userid):
    return __execute_commit_query__(Query.INSERT_AN_USER_CART.format(userid))


def add_product_to_user_wishlist(productid, userid):
    return __execute_commit_query__(Query.INSERT_PRODUCT_INTO_WISH_LIST.format(productid, userid))


def update_user_info(user_firstname, user_lastname, email, phone, dob, userid):
    print user_firstname, user_lastname, email, phone, dob, userid
    return __execute_commit_query__(Query.UPDATE_USER.format(user_firstname, user_lastname, email, phone, dob, userid))


def add_product_to_cart(cartid, productid, product_qty):
    return __execute_commit_query__(Query.INSERT_PRODUCT_INTO_CART.format(cartid, productid, product_qty))


def deactivate_user_address(userid, addressid):
    return __execute_commit_query__(Query.UPDATE_USER_ADDRESS_TO_INACTIVE.format(userid, addressid))


def insert_user_address(address_fullname, address_line_1, address_line_2, address_city, address_zip, address_country, address_state, userid):
    return __execute_commit_query__(Query.INSERT_USER_ADDRESS.format(address_fullname, address_line_1, address_line_2, address_city, address_zip, address_country, address_state, userid))


def fetch_user_accountid(username, password):
    return __execute_select_query__(Query.AUTHENTICATE_USER_WITHOUT_ID.format(username, password))[0]


def fetch_user_cartid(userid):
    return __execute_select_query__(Query.SELECT_USER_CARTID.format(userid))[0]


def remove_product_from_cart(userid, productid):
    return __execute_commit_query__(Query.DELETE_PRODUCT_FROM_CART.format(userid, productid))


def cart_contains(productid, cartid):
    return __execute_select_query__(Query.CART_CONTAINS.format(productid, cartid))[0]


def remove_from_wish_list(productid,userid):
    return __execute_commit_query__(Query.DELETE_PRODUCT_FROM_WISH_LIST.format(productid, userid))


def wish_list_contains(productid, userid):
    return __execute_select_query__(Query.WISH_LIST_CONTAINS.format(productid, userid))[0]


def user_account_exist(username, email):
    return __execute_select_query__(Query.EXISTING_ACCOUNT.format(username, email))[0]


def insert_account_info(username, upassword):
    return __execute_commit_query__(Query.INSERT_ACCOUNT_INFO.format(username, upassword))


def fetch_accounid(username):
    return __execute_select_query__(Query.SELECT_ACCOUNTID.format(username))[0]


def insert_personal_info(user_firstname, user_lastname, email, phone, dob, accountid):
    return __execute_commit_query__(Query.INSERT_USER.format(user_firstname, user_lastname, email, phone, dob, accountid))


def fetch_userid(accountid):
    return __execute_select_query__(Query.SELECT_USERID.format(accountid))[0]


def fetch_min_address(userid):
    return __execute_select_query__(Query.SELECT_MIN_ADDRESS_ID.format(userid))[0]


def fetch_max_address(userid):
    return __execute_select_query__(Query.SELECT_MAX_ADDRESS_ID.format(userid))[0]


def insert_first_payment_method(card_name, card_last_four_digits, card_number, card_exp_date, cvc, card_type, userid, billing_addressid):
    return __execute_commit_query__(Query.INSERT_USER_PAYMENT_METHOD.format(card_name, card_last_four_digits, card_number, card_exp_date, cvc, card_type, userid, billing_addressid))


def insert_user_preferences(userid, shipping_addressid, billing_addressid, payment_methodid):
    return __execute_commit_query__(Query.INSERT_USER_PREFERENCES.format(userid, shipping_addressid, billing_addressid, payment_methodid))


def validate_cc(card_type):
    return __execute_select_query__(Query.VALIDATE_CC.format(card_type))[0]


def validate_exp_date(date):
    return __execute_select_query__(Query.VALIDATE_EXP_DATE.format(date))[0]


def fetch_order(orderid, userid):
        order = __execute_select_query__(Query.SELECT_ORDER.format(orderid, userid))[0]
        if order:
            products = __execute_select_query__(Query.SELECT_ORDER_PRODUCTS.format(orderid))
            order['oproducts'] = products
            order['shipping_address'] = __execute_select_query__(Query.SELECT_USER_ADDRESS_ID.format(userid,order['shipping_addressid']))[0]
            order['billing_address'] = __execute_select_query__(Query.SELECT_USER_ADDRESS_ID.format(userid, order['billing_address']))[0]

        return order


def fetch_user_orders(userid):
    orders = __execute_select_query__(Query.SELECT_USER_ORDERS.format(userid))
    if orders:
        for order in orders:
            products = __execute_select_query__(Query.SELECT_ORDER_PRODUCTS.format(order['oid']))
            order['oproducts'] = products
            order['shipping_address'] = __execute_select_query__(
                Query.SELECT_USER_ADDRESS_ID.format(userid, order['shipping_addressid']))[0]
            order['billing_address'] = __execute_select_query__(
                Query.SELECT_USER_ADDRESS_ID.format(userid, order['billing_addressid']))[0]
            order['payment_method'] = __execute_select_query__(Query.SELECT_USER_PAYMENT_BY_ID.format(userid, order['cid']))[0]
            order.pop('shipping_addressid', None)
            order.pop('billing_addressid', None)
            order.pop('cid', None)
    return orders


def update_user_preferred_billing(addressid, userid):
    return __execute_commit_query__(Query.UPDATE_USER_PREFERRED_BILLING_ADDR.format(addressid, userid))


def update_user_preferred_shipping(addressid, userid):
    return __execute_commit_query__(Query.UPDATE_USER_PREFERRED_SHIPPING_ADDR.format(addressid, userid))


def update_user_preferred_payment(payment_methodid, userid):
    return __execute_commit_query__(Query.UPDATE_USER_PREFERRED_PAYMENT.format(payment_methodid, userid))


def fetch_user_preferences(userid):
    preferences = __execute_select_query__(Query.SELECT_USER_PREFERENCES.format(userid))[0]
    if preferences:
        preferences['shipping_address'] = __execute_select_query__(
            Query.SELECT_USER_ADDRESS_ID.format(userid, preferences['shipping_addressid']))[0]
        preferences['billing_address'] = __execute_select_query__(
            Query.SELECT_USER_ADDRESS_ID.format(userid, preferences['billing_addressid']))[0]
        preferences['payment_method'] = __execute_select_query__(
            Query.SELECT_USER_PAYMENT_BY_ID.format(userid, preferences['payment_methodid']))[0]
        preferences.pop('shipping_addressid', None)
        preferences.pop('billing_addressid', None)
        preferences.pop('payment_methodid', None)
        preferences.pop('userid', None)
    return preferences


def fetch_max_payment_methodid(userid):
    return __execute_select_query__(Query.SELECT_USER_MAX_PAYMENT_ID.format(userid))


def search_products_by_title(title):
    return __execute_select_product_query__(Query.SELECT_SEARCH_TITLE.format(title))


def advanced_product_search(data):
    if 'title' in data:
        custom_query = Query.SELECT_SEARCH_TITLE.format(data['title'])

        if 'genres' in data:
            custom_query = custom_query + " AND  genre IN ('{0}') ".format("','".join(data['genres']))

        if 'platformid' in data:
            custom_query = custom_query + ' AND  platformid = {0} '.format(data['platformid'])

        if 'price' in data:
            custom_query = custom_query + ' AND price BETWEEN {0} AND {1} '.format(data['price'][0], data['price'][1])
        print custom_query
        return __execute_select_product_query__(custom_query)
    else:
        custom_query = Query.SELECT_SEARCH_BLANK
        if 'genre' in data:
            custom_query += "  genre IN ('{0}') AND ".format("','".join(data['genres']))

        if 'platformid' in data:
            custom_query += ' platformid = {0} AND '.format(data['platformid'])

        if 'price' in data:
            custom_query += ' price BETWEEN {0} AND {1} '.format(data['price'][0], data['price'][1])

        else:
            custom_query = custom_query + ' price BETWEEN 0 AND 100000000 '
        print custom_query
        return __execute_select_product_query__(custom_query)


def insert_empty_order(cartid, shippment_feeid, shipping_addressid, userid, payment_methodid):
    return __execute_commit_query__(Query.INSERT_EMPTY_ORDER.format(cartid, shippment_feeid, shipping_addressid, userid, payment_methodid))


def insert_order_details(orderid, cartid):
    return __execute_commit_query__(Query.INSERT_ORDER_DETAILS.format(orderid, cartid))


def fetch_max_user_orderid(userid):
    return __execute_select_query__(Query.SELECT_USER_MAX_ORDER_ID.format(userid))[0]


def update_order_total(orderid):
    return __execute_commit_query__(Query.UPDATE_ORDER_TOTAL.format(orderid, orderid))


def validate_shipment_fee(shfeeid):
    return __execute_select_query__(Query.VALIDATE_SHIPMENT_FEE.format(shfeeid))[0]


def validate_address(aid, userid):
    return __execute_select_query__(Query.VALIDATE_ADDRESS_ID.format(aid,userid))[0]


def validate_payment(cid, userid):
    return __execute_select_query__(Query.VALIDATE_PAYMENT_ID.format(cid, userid))[0]


def update_order_status(order_statusid, orderid):
    return __execute_commit_query__(Query.UPDATE_ORDER_SATUS.format(order_statusid, orderid))


def fetch_shipment_fees():
    return __execute_select_query__(Query.SELECT_SHIPMENT_FEE)


def fetch_user_billing_address(userid):
    return __execute_select_query__(Query.SELECT_USER_BILLING_ADDRESS.format(userid))


def fetch_user_shipping_address(userid):
    return __execute_select_query__(Query.SELECT_USER_SHIPPING_ADDRESS.format(userid))


def fetch_store_genres():
    dict = __execute_select_query__(Query.SELECT_STORE_GENRES)
    result = []
    for e in dict:
        result.append(e['genre'])
    return result


#advanced_product_search({'title':'PS4','platformid':1, 'genres':['Console']})
#advanced_product_search({'platformid':1, 'genres':['Console'],'price':[40,600]})
#search_products_by_title('Gears of War 4')
#fetch_latest_products()
#fetch_platform_special_products()
#fetch_platforms()
#fetch_product(2)
#fetch_platform_latest_products(1)
#fetch_platform_special_products(4)
#authenticate_user('gary123',1,'Gary123s')
#print 'executing'
#insert_product_rating(1,5)
#print 'Done'
#fetch_platform_announcements(1)
#fetch_store_announcements()
#fetch_user_info(1)
#fetch_user_wish_list(1)
#fetch_user_address(1)
#fetch_user_payment_methods(1)
#fetch_user_cart(1)
#update_user_account('gary123', 'Gary123s',1)
#update_cart_product_qty(100,2,1)
#deactivate_user_payment_method(1,5)
#insert_user_payment_method('Test Test', '1234','1234-1234-1234-1234', '2018-01-02', '123', 'Master Card', 1)
#deactivate_user_cart(5,3)
#create_user_cart(3)
#add_product_to_user_wishlist(14,1)
#update_user_info(user_firstname='Luz', user_lastname='Rojas', email='luz.rojas1@upr.edu', phone='787-234-7175', dob='1997-10-12',userid=3)
#add_product_to_cart(1,20,6)
#fetch_user_accountid('gary123', 'Gary123s')
#fetch_user_cartid(1)
#cart_contains(1,2)
#wish_list_contains(1,1)
#user_account_exist('gary12', 'gary.oak@upr.edu')
#print fetch_order(1,2)
#print fetch_user_orders(14)
