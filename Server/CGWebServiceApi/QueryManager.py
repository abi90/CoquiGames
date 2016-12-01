"""
Store Queries
"""
SELECT_PRODUCT_DETAILS = """SELECT * FROM product_details WHERE pid = %s"""


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
                                AND P.platformid = %s"""


SELECT_PLATFORM_GAME_GENRES = """SELECT DISTINCT G.genre
                                  FROM product AS P JOIN genre AS G USING (genreid)
                                  WHERE categoryid IN (SELECT C.categoryid FROM category AS C WHERE C.category = 'Game') AND P.platformid = %s"""


SELECT_PLATFORM_ACCESORIES = """SELECT DISTINCT G.genre
                                  FROM product AS P JOIN genre AS G USING (genreid)
                                  WHERE categoryid IN (SELECT C.categoryid FROM category AS C WHERE C.category='Accessory')
                                  AND P.platformid = %s"""


SELECT_PLATFORM_LATEST_PRODUCTS = """SELECT *
                                      FROM product_details AS P
                                      WHERE to_date(P.release,'YYYY-MM-DD') BETWEEN now()::DATE -  '30 days'::INTERVAL AND now()::DATE
                                      AND P.platformid = %s
                                      ORDER BY to_date(P.release,'YYYY-MM-DD')"""


SELECT_PLATFORM_SPECIAL_PRODUCTS = """SELECT * FROM product_details WHERE inoffer = true AND platformid = %s"""


SELECT_PLATFORM_ANNOUNCEMENTS = """SELECT * FROM platform_announcements WHERE platformid = %s"""


SELECT_STORE_ANNOUNCEMENT = """SELECT * FROM store_announcement"""


INSERT_PRODUCT_RATING = """INSERT INTO rate (productid, rate_date, rate)
                            VALUES (%s, current_date, round(cast(%s AS NUMERIC),2)) RETURNING *"""

"""
User Queriess
"""
AUTHENTICATE_USER_WITH_ID = """SELECT active FROM account_info
                          WHERE username = %s
                          AND accountid = (SELECT cg.accountid FROM cg_user AS cg WHERE userid = %s)
                          AND upassword = crypt(%s,upassword)
                          AND active = TRUE"""


AUTHENTICATE_USER_WITHOUT_ID = """SELECT userid AS uid, roleid
                                  FROM account_info JOIN cg_user USING (accountid)
                                  WHERE account_info.active = TRUE AND cg_user.active = TRUE
                                  AND upassword = crypt(%s, upassword)
                                  AND username = %s"""


SELECT_USER = """SELECT to_char(dob, 'YYYY-MM-DD') AS udob, email AS uemail, user_firstname AS ufirstname, userid AS uid, user_lastname AS ulastname, username AS uname , phone AS uphone
                  FROM cg_user NATURAL INNER JOIN account_info
                  WHERE userid = %s"""


SELECT_USER_WISH_LIST = """SELECT productid as pid, product_title as pname, product_price as pprice
                          FROM wishlist_contains NATURAL INNER JOIN product
                          WHERE userid = %s"""


SELECT_USER_ADDRESS = """SELECT address_state AS aState, address_line_1 AS aaddress1, address_line_2 AS aaddress2, address_city AS acity,
                      address_country AS acountry, active AS acurrent, address_fullname AS afullname, addressid AS aid,
                      address_zip AS azip, CASE WHEN addressid IN (SELECT billing_addressid FROM payment_method) THEN 'billing' ELSE 'shipping' END AS atype,
                      CASE WHEN addressid IN (SELECT up.billing_addressid FROM user_preferences up) THEN TRUE
                        WHEN  addressid IN (SELECT up.shipping_addressid FROM user_preferences up) THEN TRUE
                        ELSE FALSE END AS preferred
                      FROM address
                      WHERE userid = %s"""


SELECT_USER_ADDRESS_ID = """SELECT address_state AS aState, address_line_1 AS aaddress1, address_line_2 AS aaddress2, address_city AS acity,
                      address_country AS acountry, active AS acurrent, address_fullname AS afullname, addressid AS aid,
                      address_zip AS azip, CASE WHEN addressid IN (SELECT billing_addressid FROM payment_method) THEN 'billing' ELSE 'shipping' END AS atype,
                      CASE WHEN addressid IN (SELECT up.billing_addressid FROM user_preferences up) THEN TRUE
                        WHEN  addressid IN (SELECT up.shipping_addressid FROM user_preferences up) THEN TRUE
                        ELSE FALSE END AS preferred
                      FROM address
                      WHERE userid = %s AND addressid = %s"""


SELECT_USER_CREDIT_CARD = """SELECT to_char(card_exp_date, 'YYYY-MM') AS cexpdate, payment_methodid AS cid, card_last_four_digits AS cnumber, card_type AS ctype,
                              CASE WHEN payment_methodid IN (SELECT up.payment_methodid FROM user_preferences up) THEN TRUE
                              ELSE FALSE END AS preferred
                              FROM payment_method
                              WHERE userid = %s"""

SELECT_USER_PAYMENT_BY_ID= """SELECT to_char(card_exp_date, 'YYYY-MM') AS cexpdate, payment_methodid AS cid, card_last_four_digits AS cnumber, card_type AS ctype,
                              CASE WHEN payment_methodid IN (SELECT up.payment_methodid FROM user_preferences up) THEN TRUE
                              ELSE FALSE END AS preferred
                              FROM payment_method
                              WHERE userid = %s AND payment_methodid = %s"""


SELECT_USER_CART = """SELECT cc.productid AS pid,p.product_title AS pname, p.product_price AS pprice, cc.cart_product_qty as pquantity
                      FROM cart_contains cc JOIN product P USING (productid)
                      WHERE cc.cartid IN (SELECT c.cartid FROM cart as c WHERE c.userid = %s AND c.active = TRUE)
                      ORDER BY cc.cartid, cc.insert_date"""


SELECT_USER_CARTID = """SELECT cartid FROM cart WHERE userid = %s AND active = TRUE;"""


UPDATE_USER_ACCOUNT = """UPDATE account_info
                          SET username = %s, upassword = crypt(%s,gen_salt('md5'))
                          WHERE accountid = (SELECT u.accountid FROM cg_user AS u WHERE u.userid = %s) RETURNING *"""


UPDATE_USER_CART = """UPDATE cart_contains AS cc
                      SET cart_product_qty = %s
                      WHERE cc.productid = %s AND cc.cartid IN (SELECT cartid FROM cart WHERE userid = %s AND cart.active = TRUE) RETURNING *"""


UPDATE_USER_CART_TO_INACTIVE = """UPDATE cart
                                  SET active = FALSE
                                  WHERE cartid = %s AND userid = %s RETURNING *"""


UPDATE_USER_PAYMENT_METHOD_TO_INACTIVE = """UPDATE payment_method
                                              SET active = FALSE
                                              WHERE userid = %s AND payment_methodid = %s RETURNING *"""


UPDATE_USER_PAYMENT_METHOD_TO_INACTIVE = """UPDATE payment_method
                                            SET active = FALSE
                                            WHERE userid = %s AND payment_methodid = %s RETURNING *"""


INSERT_USER_PAYMENT_METHOD_USING_PREF = """INSERT INTO payment_method (card_name, card_last_four_digits, card_number, card_exp_date, cvc, card_type, userid, billing_addressid, active)
                                            VALUES (%s,%s,crypt(%s,gen_salt('md5')),to_date(%s,'YYYY-MM-DD'),%s,%s,%s,
                                                      (SELECT u.billing_addressid FROM user_preferences u WHERE u.userid = %s), TRUE) RETURNING *"""



INSERT_AN_USER_CART = """INSERT INTO cart (userid, active, insert_date) values (%s,TRUE ,current_date) RETURNING *"""


INSERT_PRODUCT_INTO_WISH_LIST = """INSERT INTO wishlist_contains(productid, userid) values(%s,%s) RETURNING *"""


UPDATE_USER = """UPDATE cg_user AS u
                  SET user_firstname = %s, user_lastname = %s, email = %s, phone = %s, dob = to_date(%s, 'YYYY-MM-DD')
                  WHERE u.userid = %s
                  RETURNING *"""


INSERT_PRODUCT_INTO_CART = """INSERT INTO cart_contains (cartid, productid, cart_product_qty, insert_date)
                              VALUES (%s,%s,%s,current_date) RETURNING *"""


UPDATE_USER_ADDRESS_TO_INACTIVE = """UPDATE address AS a SET active = FALSE
                                      WHERE a.userid = %s AND a.active = TRUE AND a.addressid = %s RETURNING *"""


INSERT_USER_ADDRESS = """INSERT INTO address (active, address_fullname, address_line_1, address_line_2, address_city, address_zip, address_country, address_state, userid)
                          VALUES (TRUE, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING addressid"""


DELETE_PRODUCT_FROM_CART = """DELETE FROM cart_contains AS cc
                              WHERE cc.cartid = (SELECT c.cartid FROM cart AS c WHERE c.userid = %s AND c.active = TRUE)
                              AND cc.productid = %s
                              RETURNING *"""

CART_CONTAINS = """SELECT CASE
                            WHEN %s IN (SELECT productid FROM cart_contains WHERE cartid = %s) THEN TRUE
                            ELSE FALSE
                          END AS product_in_cart"""


DELETE_PRODUCT_FROM_WISH_LIST = """DELETE FROM wishlist_contains WHERE productid = %s AND userid = %s RETURNING *"""


WISH_LIST_CONTAINS = """SELECT  CASE
                                  WHEN %s IN (SELECT productid FROM wishlist_contains WHERE userid = %s) THEN TRUE
                                  ELSE FALSE
                                END AS product_in_wishlist"""


EXISTING_ACCOUNT = """SELECT CASE
                                  WHEN (%s) IN (SELECT username FROM account_info) THEN TRUE
                                  WHEN (%s) IN (SELECT email FROM cg_user) THEN TRUE
                                  ELSE FALSE
                              END AS user_exist"""


INSERT_ACCOUNT_INFO = """INSERT INTO account_info (username, upassword, roleid, active)
                          VALUES (%s, crypt(%s, gen_salt('md5')), 1, TRUE) RETURNING accountid"""


SELECT_ACCOUNTID = """SELECT accountid FROM account_info WHERE username = %s"""


INSERT_USER = """INSERT INTO cg_user (user_firstname, user_lastname, email, phone, dob, active, accountid)
                  VALUES (%s, %s, %s, %s, to_date(%s, 'YYYY-MM-DD'), TRUE, %s) RETURNING userid"""


SELECT_USERID = """SELECT userid FROM cg_user WHERE accountid = %s"""


INSERT_USER_PAYMENT_METHOD = """INSERT INTO payment_method (card_name, card_last_four_digits, card_number, card_exp_date, cvc, card_type, userid, billing_addressid, active)
                                            VALUES (%s,%s,crypt(%s,gen_salt('md5')),to_date(%s,'YYYY-MM'),%s,%s,%s, %s, TRUE) RETURNING payment_methodid"""


INSERT_USER_PREFERENCES = """INSERT INTO user_preferences (userid, shipping_addressid, billing_addressid, payment_methodid)
                              VALUES (%s, %s, %s, %s) RETURNING *"""


SELECT_MAX_ADDRESS_ID = """SELECT MAX(addressid) AS aid FROM address WHERE userid = %s"""


SELECT_MIN_ADDRESS_ID = """SELECT MIN(addressid) AS aid FROM address WHERE userid = %s"""


VALIDATE_EXP_DATE = """SELECT CASE
                                    WHEN to_date(%s, 'YYYY-MM-DD') > current_date THEN TRUE
                                    ELSE FALSE
                            END AS valid_exp_date"""


VALIDATE_CC = """SELECT CASE
                            WHEN %s IN (SELECT card_type FROM card_type WHERE active = TRUE ) THEN TRUE
                            ELSE FALSE
                        END AS valid_cc"""



SELECT_ORDER = """SELECT orderid AS oid, to_char(order_date, 'YYYY-MM-DD') AS odate, payment_methodid AS cid, order_status_name AS ostatus, osubtotal,
                  fee AS oshipmment_fee, order_total AS ototal, shipping_addressid, billing_addressid
                  FROM orders JOIN order_status USING (order_statusid) JOIN order_subtotal USING (orderid)
                  JOIN payment_method USING (userid, payment_methodid) JOIN shipment_fee USING (shipment_feeid)
                  WHERE orderid = %s AND userid = %s"""


SELECT_ORDER_PRODUCTS = """SELECT o.productid AS pid, p.product_title AS pname, o.product_price AS pprice,
                            o.product_qty AS pquantity, o.product_price * o.product_qty AS ptotal
                            FROM order_details AS o JOIN product AS p USING (productid)
                            WHERE o.orderid = %s"""


SELECT_USER_ORDERS = """SELECT orderid AS oid, to_char(order_date, 'YYYY-MM-DD') AS odate, payment_methodid AS cid, order_status_name AS ostatus, osubtotal,
                  fee AS oshipmment_fee, order_total AS ototal, shipping_addressid, billing_addressid
                  FROM orders JOIN order_status USING (order_statusid) JOIN order_subtotal USING (orderid)
                  JOIN payment_method USING (userid, payment_methodid) JOIN shipment_fee USING (shipment_feeid)
                  WHERE userid = %s"""


INSERT_EMPTY_ORDER = """INSERT INTO orders (cartid, shipment_feeid, order_statusid, shipping_addressid, userid, payment_methodid, order_date, order_total)
                        VALUES(%s,%s, 2, %s, %s, %s, current_date, 0) RETURNING orderid"""


INSERT_ORDER_DETAILS = """INSERT INTO order_details (orderid, productid, product_price, product_qty)
                          (SELECT %s AS orderid, productid, product_price, cart_product_qty as product_qty
                          FROM cart_contains JOIN product USING (productid)
                          WHERE cartid = %s)
                          RETURNING *"""


UPDATE_USER_PREFERRED_BILLING_ADDR = """UPDATE user_preferences SET billing_addressid = %s WHERE userid = %s RETURNING *"""


UPDATE_USER_PREFERRED_SHIPPING_ADDR = """UPDATE user_preferences SET shipping_addressid = %s WHERE userid = %s RETURNING *"""


UPDATE_USER_PREFERRED_PAYMENT = """UPDATE user_preferences SET payment_methodid = %s WHERE userid = %s RETURNING *"""


SELECT_USER_PREFERENCES = """SELECT * FROM user_preferences WHERE userid = %s"""


SELECT_USER_MAX_PAYMENT_ID = """SELECT max(payment_methodid) as pid FROM payment_method WHERE userid = %s"""


SELECT_SEARCH_TITLE = """SELECT * FROM product_details WHERE lower(title) LIKE lower(%s)"""


SELECT_SEARCH_BLANK = """SELECT * FROM product_details WHERE"""


SELECT_USER_MAX_ORDER_ID = """SELECT max(orderid) AS orderid FROM orders WHERE userid = %s"""


UPDATE_ORDER_TOTAL = """UPDATE orders
                        SET order_total = (SELECT sum((order_details.product_price * (order_details.product_qty)::numeric)) + shipment_fee.fee AS total
                                            FROM order_details JOIN orders USING(orderid) JOIN shipment_fee USING (shipment_feeid)
                                            WHERE orderid = %s
                                            GROUP BY order_details.orderid, shipment_fee.fee)
                        WHERE orderid = %s"""


VALIDATE_SHIPMENT_FEE = """SELECT CASE WHEN %s IN (SELECT shipment_feeid FROM shipment_fee WHERE active = TRUE ) THEN TRUE
                            ELSE FALSE END AS valid_fee"""


VALIDATE_ADDRESS_ID = """SELECT CASE WHEN %s IN (SELECT addressid FROM address WHERE userid = %s AND active = TRUE) THEN TRUE
                          ELSE FALSE END AS valid_aid"""


VALIDATE_PAYMENT_ID = """SELECT CASE WHEN %s IN (SELECT payment_methodid FROM payment_method WHERE userid = %s AND active = TRUE) THEN TRUE
                          ELSE FALSE END AS valid_pid"""


UPDATE_ORDER_SATUS = """UPDATE orders SET order_statusid = %s WHERE orderid = %s"""


SELECT_SHIPMENT_FEE = """SELECT f.shipment_feeid, f.fee, f.fee_description FROM shipment_fee AS f WHERE active = TRUE"""


SELECT_USER_SHIPPING_ADDRESS = """SELECT address_state AS aState, address_line_1 AS aaddress1, address_line_2 AS aaddress2, address_city AS acity,
                      address_country AS acountry, active AS acurrent, address_fullname AS afullname, addressid AS aid,
                      address_zip AS azip, 'shipping' AS atype,
                      CASE WHEN addressid IN (SELECT up.billing_addressid FROM user_preferences up) THEN TRUE
                        WHEN  addressid IN (SELECT up.shipping_addressid FROM user_preferences up) THEN TRUE
                        ELSE FALSE END AS preferred
                      FROM address
                      WHERE userid = %s AND  addressid NOT IN (SELECT billing_addressid FROM payment_method)"""


SELECT_USER_BILLING_ADDRESS = """SELECT address_state AS aState, address_line_1 AS aaddress1, address_line_2 AS aaddress2, address_city AS acity,
                      address_country AS acountry, active AS acurrent, address_fullname AS afullname, addressid AS aid,
                      address_zip AS azip, 'billing' AS atype,
                      CASE WHEN addressid IN (SELECT up.billing_addressid FROM user_preferences up) THEN TRUE
                        WHEN  addressid IN (SELECT up.shipping_addressid FROM user_preferences up) THEN TRUE
                        ELSE FALSE END AS preferred
                      FROM address
                      WHERE userid = %s AND  addressid IN (SELECT billing_addressid FROM payment_method)"""


SELECT_STORE_GENRES = """SELECT genre FROM genre WHERE active = TRUE"""



SELECT_RELATED_PRODUCTS = """SELECT * FROM product_details
                                WHERE (genre, category, platformid) IN
                                (
                                  SELECT genre, category, platformid
                                  FROM product_details WHERE pid = %s
                                )
                                AND pid <> %s"""


SELECT_HOME_TOP_PRODUCTS = """SELECT * FROM product_details ORDER BY rating DESC LIMIT 30"""


SELECT_PLATFORM_TOP_PRODUCTS = """SELECT * FROM product_details WHERE platformid = %s ORDER BY rating DESC LIMIT 30"""


AUTHENTICATE_ADMIN_USER = """SELECT active FROM account_info
                          WHERE roleid = 3 AND active = TRUE
                          AND upassword = crypt(%s,upassword)
                          AND username = %s
                          """

SELECT_USERS = """SELECT a.accountid, a.username, b.email AS user_email, b.user_firstname, b.user_lastname, a.roleid ,a.active
                  FROM account_info AS a JOIN cg_user AS b USING (accountid)
                  ORDER BY a.active, a.username"""


SELECT_PRODUCT_ALT_IMGS = """SELECT pi.product_img FROM product_img AS pi WHERE pi.productid = %s AND pi.cover = FALSE"""



