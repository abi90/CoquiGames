"""
Store Queries
"""
SELECT_PRODUCT_DETAILS = """SELECT * FROM product_details WHERE pid = {0}"""


SELECT_LATEST_PRODUCTS = """SELECT *
                            FROM product_details
                            WHERE to_date(release,'YYYY-MM-DD') BETWEEN now()::DATE -  '30 days'::INTERVAL AND now()::DATE
                            ORDER BY to_date(release,'YYYY-MM-DD')"""


SELECT_SPECIAL_PRODUCTS = """SELECT * FROM product_details WHERE INOFFER = true"""


SELECT_PLATFORMS = """SELECT pa.platformid, pa.logoimg, pa.platform
                      FROM platform AS pa
                      WHERE pa.active = TRUE"""


SELECT_PLATFORM_CONSOLES = """SELECT P.productid, P.product_title
                                FROM product AS P
                                WHERE P.categoryid IN (SELECT C.categoryid FROM category AS C WHERE C.category='Console')
                                AND P.platformid = {0}"""


SELECT_PLATFORM_GAME_GENRES = """SELECT DISTINCT G.genre
                                  FROM product AS P JOIN genre AS G USING (genreid)
                                  WHERE categoryid IN (SELECT C.categoryid FROM category AS C WHERE C.category = 'Game') AND P.platformid = {0}"""


SELECT_PLATFORM_ACCESORIES = """SELECT DISTINCT G.genre
                                  FROM product AS P JOIN genre AS G USING (genreid)
                                  WHERE categoryid IN (SELECT C.categoryid FROM category AS C WHERE C.category='Accessory')
                                  AND P.platformid = {0}"""


SELECT_PLATFORM_LATEST_PRODUCTS = """SELECT *
                                      FROM product_details AS P
                                      WHERE to_date(P.release,'YYYY-MM-DD') BETWEEN now()::DATE -  '30 days'::INTERVAL AND now()::DATE
                                      AND P.platformid = {0}
                                      ORDER BY to_date(P.release,'YYYY-MM-DD')"""


SELECT_PLATFORM_SPECIAL_PRODUCTS = """SELECT * FROM product_details WHERE inoffer = true AND pid = {0}"""


SELECT_PLATFORM_ANNOUNCEMENTS = """SELECT * FROM platform_announcements WHERE platformid = {0}"""


SELECT_STORE_ANNOUNCEMENT = """SELECT * FROM store_announcement"""


INSERT_PRODUCT_RATING = """INSERT INTO rate (productid, rate_date, rate)
                            VALUES ({0}, current_date, round(cast({1} AS NUMERIC),2))"""

"""
User Queriess
"""
AUTHENTICATE_USER_WITH_ID = """SELECT active FROM account_info
                          WHERE username = '{0}' AND accountid = (SELECT cg.accountid FROM cg_user AS cg WHERE userid = {1}) AND upassword = crypt('{2}',upassword) AND active = TRUE"""


AUTHENTICATE_USER_WITHOUT_ID = """SELECT accountid AS uid FROM account_info WHERE username = '{0}' AND upassword = crypt('{1}',upassword) AND active = TRUE"""


SELECT_USER = """SELECT to_char(dob, 'YYYY-MM-DD') AS udob, email AS uemail, user_firstname AS ufirstname, userid AS uid, user_lastname AS ulastname, username AS uname , phone AS uphone
                  FROM cg_user NATURAL INNER JOIN account_info
                  WHERE userid = {0}"""


SELECT_USER_WISH_LIST = """SELECT productid as pid, product_title as pname, product_price as pprice
                          FROM wishlist_contains NATURAL INNER JOIN product
                          WHERE userid = {0}"""


SELECT_USER_ADDRESS = """SELECT address_state AS aState, address_line_1 AS aaddress1, address_line_2 AS aaddress2, address_city AS acity,
                      address_country AS acountry, active AS acurrent, address_fullname AS afullname, addressid AS aid,
                      address_zip AS azip, CASE WHEN addressid IN (SELECT billing_addressid FROM payment_method) THEN 'billing' ELSE 'shipping' END AS atype
                      FROM address
                      WHERE userid = {0}"""


SELECT_USER_CREDIT_CARD = """SELECT to_char(card_exp_date, 'YYYY-MM-DD') AS cexpdate, payment_methodid AS cid, card_last_four_digits AS cnumber, card_type AS ctype
                              FROM payment_method
                              WHERE userid = {0}"""


SELECT_USER_CART = """SELECT cc.productid AS pid,p.product_title AS pname, p.product_price AS pprice, cc.cart_product_qty as pquantity
                      FROM cart_contains cc JOIN product P USING (productid)
                      WHERE cc.cartid IN (SELECT c.cartid FROM cart as c WHERE c.userid = {0} AND c.active = TRUE)
                      ORDER BY cc.cartid, cc.insert_date"""


SELECT_USER_CARTID = """SELECT cartid FROM cart WHERE userid = {0} AND active = TRUE;"""


UPDATE_USER_ACCOUNT = """UPDATE account_info
                          SET username = '{0}', upassword = crypt('{1}',gen_salt('md5'))
                          WHERE accountid = (SELECT u.accountid FROM cg_user AS u WHERE u.userid = {2})"""


UPDATE_USER_CART = """UPDATE cart_contains AS cc
                      SET cart_product_qty = {0}
                      WHERE cc.productid = {1} AND cc.cartid IN (SELECT cartid FROM cart WHERE userid = {2} AND cart.active = TRUE )"""


UPDATE_USER_CART_TO_INACTIVE = """UPDATE cart
                                  SET active = FALSE
                                  WHERE cartid = {0} AND userid = {1}"""


UPDATE_USER_PAYMENT_METHOD_TO_INACTIVE = """UPDATE payment_method
                                              SET active = FALSE
                                              WHERE userid = {0} AND payment_methodid = {1}"""


UPDATE_USER_PAYMENT_METHOD_TO_INACTIVE = """UPDATE payment_method
                                            SET active = FALSE
                                            WHERE userid = {0} AND payment_methodid = {1}"""


INSERT_USER_PAYMENT_METHOD_USING_PREF = """INSERT INTO payment_method (card_name, card_last_four_digits, card_number, card_exp_date, cvc, card_type, userid, billing_addressid, active)
                                            VALUES ('{0}','{1}',crypt('{2}',gen_salt('md5')),to_date('{3}','YYYY-MM-DD'),'{4}','{5}',{6},
                                                      (SELECT u.billing_addressid FROM user_preferences u WHERE u.userid = {7}), TRUE)"""


INSERT_AN_USER_CART = """INSERT INTO cart (userid, active, insert_date) values ({0},TRUE ,current_date)"""


INSERT_PRODUCT_INTO_WISH_LIST = """INSERT INTO wishlist_contains(productid, userid) values({0},{1})"""


UPDATE_USER = """UPDATE cg_user AS u
                  SET user_firstname = '{0}', user_lastname = '{1}', email = '{2}', phone = '{3}', dob = to_date('{4}', 'YYYY-MM-DD')
                  WHERE u.userid = {5}"""


INSERT_PRODUCT_INTO_CART = """INSERT INTO cart_contains (cartid, productid, cart_product_qty, insert_date)
                              VALUES ({0},{1},{2},current_date)"""


UPDATE_USER_ADDRESS_TO_INACTIVE = """UPDATE address AS a SET active = FALSE
                                      WHERE a.userid = {0} AND a.active = TRUE AND a.addressid = {1}"""


INSERT_USER_ADDRESS = """INSERT INTO address (active, address_fullname, address_line_1, address_line_2, address_city, address_zip, address_country, address_state, userid)
                          VALUES (TRUE, '{0}', '{1}', '{2}', '{3}', '{4}', '{5}', '{6}', {7})"""


DELETE_PRODUCT_FROM_CART = """DELETE FROM cart_contains AS cc
                              WHERE cc.cartid = (SELECT c.cartid FROM cart AS c WHERE c.userid = {0} AND c.active = TRUE)
                              AND cc.productid = {1}"""

CART_CONTAINS = """SELECT CASE
                            WHEN {0} IN (SELECT productid FROM cart_contains WHERE cartid = {1}) THEN TRUE
                            ELSE FALSE
                          END AS product_in_cart"""


DELETE_PRODUCT_FROM_WISH_LIST = """DELETE FROM wishlist_contains WHERE productid = {0} AND userid = {1}"""


WISH_LIST_CONTAINS = """SELECT  CASE
                                  WHEN {0} IN (SELECT productid FROM wishlist_contains WHERE userid = {1}) THEN TRUE
                                  ELSE FALSE
                                END AS product_in_wishlist"""


EXISTING_ACCOUNT = """SELECT CASE
                                  WHEN ('{0}') IN (SELECT username FROM account_info) THEN TRUE
                                  WHEN ('{1}') IN (SELECT email FROM cg_user) THEN TRUE
                                  ELSE FALSE
                              END AS user_exist"""


INSERT_ACCOUNT_INFO = """INSERT INTO account_info (username, upassword, roleid, active)
                          VALUES ('{0}', crypt('{1}', gen_salt('md5')), 1, TRUE)"""


SELECT_ACCOUNTID = """SELECT accountid FROM account_info WHERE username = '{0}'"""


INSERT_USER = """INSERT INTO cg_user (user_firstname, user_lastname, email, phone, dob, active, accountid)
                  VALUES ('{0}', '{1}', '{2}', '{3}', to_date('{4}', 'YYYY-MM-DD'), TRUE, {5})"""


SELECT_USERID = """SELECT userid FROM cg_user WHERE accountid = {0}"""


INSERT_USER_PAYMENT_METHOD = """INSERT INTO payment_method (card_name, card_last_four_digits, card_number, card_exp_date, cvc, card_type, userid, billing_addressid, active)
                                            VALUES ('{0}','{1}',crypt('{2}',gen_salt('md5')),to_date('{3}','YYYY-MM-DD'),'{4}','{5}',{6}, {7}, TRUE)"""


INSERT_USER_PREFERENCES = """INSERT INTO user_preferences (userid, shipping_addressid, billing_addressid, payment_methodid)
                              VALUES ({0}, {1}, {2}, {3})"""


SELECT_MAX_ADDRESS_ID = """SELECT MAX(addressid) AS aid FROM address WHERE userid = {0}"""


SELECT_MIN_ADDRESS_ID = """SELECT MIN(addressid) AS aid FROM address WHERE userid = {0}"""


VALIDATE_EXP_DATE = """SELECT CASE
                                    WHEN to_date('{0}', 'YYYY-MM-DD') > current_date THEN TRUE
                                    ELSE FALSE
                            END AS valid_exp_date"""


VALIDATE_CC = """SELECT CASE
                            WHEN '{0}' IN (SELECT card_type FROM card_type WHERE active = TRUE ) THEN TRUE
                            ELSE FALSE
                        END AS valid_cc"""



SELECT_ORDER = """SELECT orderid AS oid, to_char(order_date, 'YYYY-MM-DD') AS odate, payment_methodid AS cid, order_status_name AS ostatus, osubtotal,
                  fee AS oshipmment_fee, order_total AS ototal, shipping_addressid, billing_addressid
                  FROM orders JOIN order_status USING (order_statusid) JOIN order_subtotal USING (orderid)
                  JOIN payment_method USING (userid, payment_methodid) JOIN shippment_fee USING (shippment_feeid)
                  WHERE orderid = {0} AND userid = {1}"""


SELECT_ORDER_PRODUCTS = """SELECT o.productid AS pid, p.product_title AS pname, o.product_price AS pprice,
                            o.product_qty AS pquantity, o.product_price * o.product_qty AS ptotal
                            FROM order_details AS o JOIN product AS p USING (productid)
                            WHERE o.orderid = {0}"""


SELECT_USER_ORDERS = """SELECT orderid AS oid, to_char(order_date, 'YYYY-MM-DD') AS odate, payment_methodid AS cid, order_status_name AS ostatus, osubtotal,
                  fee AS oshipmment_fee, order_total AS ototal, shipping_addressid, billing_addressid
                  FROM orders JOIN order_status USING (order_statusid) JOIN order_subtotal USING (orderid)
                  JOIN payment_method USING (userid, payment_methodid) JOIN shippment_fee USING (shippment_feeid)
                  WHERE userid = {0}"""


UPDATE_USER_PREFERRED_BILLING_ADDR = """UPDATE user_preferences SET billing_addressid = {0} WHERE userid = {1}"""


UPDATE_USER_PREFERRED_SHIPPING_ADDR = """UPDATE user_preferences SET shipping_addressid = {0} WHERE userid = {1}"""


UPDATE_USER_PREFERRED_PAYMENT = """UPDATE user_preferences SET payment_methodid = {0} WHERE userid = {1}"""


SELECT_USER_PREFERENCES = """SELECT * FROM user_preferences WHERE userid = {0}"""


SELECT_USER_MAX_PAYMENT_ID = """SELECT max(payment_methodid) as pid FROM payment_method WHERE userid = {0}"""


