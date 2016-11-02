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
url = urlparse.urlparse(os.environ["DATABASE_URL"])


def connection():
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
        port=url.port
    )
    return conn


def execute_select_query(query):
    try:
        conn = connection()
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


def execute_select_product_query(query):
    try:
        conn = connection()
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


def execute_commit_query(query):
    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute(query)
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print e
        return False


def fetch_special_products():
    return execute_select_product_query(Query.SELECT_SPECIAL_PRODUCTS)


def fetch_latest_products():
    return execute_select_query(Query.SELECT_LATEST_PRODUCTS)


def fetch_platforms():
    try:

        conn = connection()
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
    return execute_select_product_query(Query.SELECT_PRODUCT_DETAILS.format(productid))[0]


def fetch_platform_latest_products(platformid):
    return execute_select_product_query(Query.SELECT_PLATFORM_LATEST_PRODUCTS.format(platformid))


def fetch_platform_special_products(platformid):
    return execute_select_product_query(Query.SELECT_PLATFORM_SPECIAL_PRODUCTS.format(platformid))


def fetch_platform_announcements(platformid):
    return execute_select_query(Query.SELECT_PLATFORM_ANNOUNCEMENTS.format(platformid))


def fetch_store_announcements():
    return execute_select_query(Query.SELECT_STORE_ANNOUNCEMENT)


def insert_product_rating(productid, rate):
   return execute_commit_query(Query.INSERT_PRODUCT_RATING.format(productid, rate))


def authenticate_user(username, userid, password):
    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute(Query.AUTHENTICATE_USER_WITH_ID.format(username, userid, password))
        results = cur.fetchall()

        print results

        conn.close()
        return results
    except Exception as e:
        print e


def fetch_user_info(userid):
    return execute_select_query(Query.SELECT_USER.format(userid))[0]


def fetch_user_wish_list(userid):
    return execute_select_query(Query.SELECT_USER_WISH_LIST.format(userid))


def fetch_user_address(userid):
    return execute_select_query(Query.SELECT_USER_ADDRESS.format(userid))


def fetch_user_payment_methods(userid):
    return execute_select_query(Query.SELECT_USER_CREDIT_CARD.format(userid))


def fetch_user_cart(userid):
    return execute_select_query(Query.SELECT_USER_CART.format(userid))


def update_user_account(username, upassword, userid):
    return execute_commit_query(Query.UPDATE_USER_ACCOUNT.format(username,upassword, userid))


def update_cart_product_qty(product_qty, productid, userid):
    return execute_commit_query(Query.UPDATE_USER_CART.format(product_qty,productid, userid))


def deactivate_user_cart(cartid, userid):
    return execute_commit_query(Query.UPDATE_USER_CART_TO_INACTIVE.format(cartid, userid))


def deactivate_user_payment_method(userid, payment_methodid):
    return execute_commit_query(Query.UPDATE_USER_PAYMENT_METHOD_TO_INACTIVE.format(userid,payment_methodid))


def insert_user_payment_method(card_name, card_last_four_digits, card_number, card_exp_date, cvc, card_type, userid):
    return execute_commit_query(Query.INSERT_USER_PAYMENT_METHOD.format(card_name, card_last_four_digits, card_number, card_exp_date, cvc, card_type, userid,userid))


def create_user_cart(userid):
    return execute_commit_query(Query.INSERT_AN_USER_CART.format(userid))


def add_product_to_user_wishlist(productid, userid):
    return execute_commit_query(Query.INSERT_PRODUCT_INTO_WISH_LIST.format(productid, userid))


def update_user_info(user_firstname, user_lastname, email, phone, dob, userid):
    print user_firstname, user_lastname, email, phone, dob, userid
    return execute_commit_query(Query.UPDATE_USER.format(user_firstname, user_lastname, email, phone, dob, userid))


def add_product_to_cart(cartid, productid, product_qty):
    return execute_commit_query(Query.INSERT_PRODUCT_INTO_CART.format(cartid, productid, product_qty))


def deactivate_user_address(userid):
    return execute_commit_query(Query.UPDATE_USER_ADDRESS_TO_INACTIVE.format(userid, userid))


def insert_user_address(active, address_fullname, address_line_1, address_line_2, address_city, address_zip, address_country, address_state, userid):
    return execute_commit_query(Query.INSERT_USER_ADDRESS.format(active, address_fullname, address_line_1, address_line_2, address_city, address_zip, address_country, address_state, userid))


def fetch_user_id(username, password):
    return execute_select_query(Query.AUTHENTICATE_USER_WITHOUT_ID.format(username, password))[0]


def fetch_user_cartid(userid):
    return execute_select_query(Query.SELECT_USER_CARTID.format(userid))[0]

#fetch_latest_products()
#fetch_special_products()
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
#fetch_user_id('gary123', 'Gary123s')
#fetch_user_cartid(1)