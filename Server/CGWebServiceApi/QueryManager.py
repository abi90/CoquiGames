"""
Store Queries
"""
SELECT_PRODUCT_DETAILS = """SELECT * FROM product_details WHERE pid = %s"""


SELECT_LATEST_PRODUCTS = """SELECT *
                            FROM product_details
                            WHERE to_date(release,'YYYY-MM-DD') BETWEEN now()::DATE -  '62 days'::INTERVAL AND now()::DATE
                            ORDER BY to_date(release,'YYYY-MM-DD') DESC"""


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
                                      WHERE to_date(P.release,'YYYY-MM-DD') BETWEEN now()::DATE -  '62 days'::INTERVAL AND now()::DATE
                                      AND P.platformid = %s
                                      ORDER BY to_date(P.release,'YYYY-MM-DD') DESC"""


SELECT_PLATFORM_SPECIAL_PRODUCTS = """SELECT * FROM product_details WHERE inoffer = true AND platformid = %s"""


SELECT_PLATFORM_ANNOUNCEMENTS = """SELECT * FROM platform_announcements WHERE platformid = %s AND active = TRUE"""


SELECT_STORE_ANNOUNCEMENT = """SELECT * FROM store_announcement WHERE active = TRUE"""


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


SELECT_USER_WISH_LIST = """SELECT wi.productid as pid, p.product_title as pname, p.product_price as pprice, pi.product_img as cover,
CASE
            WHEN (p.productid IN ( SELECT offer.productid
               FROM offer
              WHERE ((offer.offer_start_date <= ('now'::text)::date) AND (offer.offer_end_date > ('now'::text)::date)))) THEN true
            ELSE false
        END AS inoffer,
        CASE
            WHEN (p.productid IN ( SELECT offer.productid
               FROM offer
              WHERE ((offer.offer_start_date <= ('now'::text)::date) AND (offer.offer_end_date > ('now'::text)::date)))) THEN (( SELECT min(o.offer_price) AS min
               FROM offer o
              WHERE ((o.productid = p.productid) AND (o.offer_start_date <= ('now'::text)::date) AND (o.offer_end_date > ('now'::text)::date))))::real
            ELSE (0)::real
        END AS offerprice
                          FROM wishlist_contains wi JOIN product p USING (productid) JOIN product_img pi USING(productid)
                          WHERE wi.userid = %s and pi.cover = true"""


SELECT_USER_ADDRESS = """SELECT address_state AS aState, address_line_1 AS aaddress1, address_line_2 AS aaddress2, address_city AS acity,
                      address_country AS acountry, active AS acurrent, address_fullname AS afullname, addressid AS aid,
                      address_zip AS azip, CASE WHEN addressid IN (SELECT billing_addressid FROM payment_method) THEN 'billing' ELSE 'shipping' END AS atype,
                      CASE WHEN addressid IN (SELECT up.billing_addressid FROM user_preferences up) THEN TRUE
                        WHEN  addressid IN (SELECT up.shipping_addressid FROM user_preferences up) THEN TRUE
                        ELSE FALSE END AS apreferred
                      FROM address
                      WHERE address.userid = %s AND address.active = TRUE"""


SELECT_USER_ADDRESS_ID = """SELECT address_state AS aState, address_line_1 AS aaddress1, address_line_2 AS aaddress2, address_city AS acity,
                      address_country AS acountry, active AS acurrent, address_fullname AS afullname, addressid AS aid,
                      address_zip AS azip, CASE WHEN addressid IN (SELECT billing_addressid FROM payment_method) THEN 'billing' ELSE 'shipping' END AS atype,
                      CASE WHEN addressid IN (SELECT up.billing_addressid FROM user_preferences up) THEN TRUE
                        WHEN  addressid IN (SELECT up.shipping_addressid FROM user_preferences up) THEN TRUE
                        ELSE FALSE END AS apreferred
                      FROM address
                      WHERE userid = %s AND addressid = %s"""


SELECT_USER_CREDIT_CARD = """SELECT to_char(card_exp_date, 'YYYY-MM') AS cexpdate, payment_methodid AS cid, card_last_four_digits AS cnumber, card_type AS ctype,
                              CASE WHEN payment_methodid IN (SELECT up.payment_methodid FROM user_preferences up) THEN TRUE
                              ELSE FALSE END AS ppreferred
                              FROM payment_method
                              WHERE userid = %s AND active = TRUE"""

SELECT_USER_PAYMENT_BY_ID= """SELECT to_char(card_exp_date, 'YYYY-MM') AS cexpdate, payment_methodid AS cid, card_last_four_digits AS cnumber, card_type AS ctype,
                              CASE WHEN payment_methodid IN (SELECT up.payment_methodid FROM user_preferences up) THEN TRUE
                              ELSE FALSE END AS ppreferred
                              FROM payment_method
                              WHERE userid = %s AND payment_methodid = %s"""


SELECT_USER_CART = """SELECT cc.productid AS pid,p.product_title AS pname, p.product_price AS pprice, cc.cart_product_qty as pquantity, pi.product_img AS cover,

  CASE
            WHEN (p.productid IN ( SELECT offer.productid
               FROM offer
              WHERE ((offer.offer_start_date <= ('now'::text)::date) AND (offer.offer_end_date > ('now'::text)::date)))) THEN true
            ELSE false
        END AS inoffer,
        CASE
            WHEN (p.productid IN ( SELECT offer.productid
               FROM offer
              WHERE ((offer.offer_start_date <= ('now'::text)::date) AND (offer.offer_end_date > ('now'::text)::date)))) THEN (( SELECT min(o.offer_price) AS min
               FROM offer o
              WHERE ((o.productid = p.productid) AND (o.offer_start_date <= ('now'::text)::date) AND (o.offer_end_date > ('now'::text)::date))))::real
            ELSE (0)::real
        END AS offerprice

                      FROM cart_contains cc JOIN product P USING (productid) JOIN product_img pi USING (productid)
                      WHERE cc.cartid IN (SELECT c.cartid FROM cart as c WHERE c.userid = %s AND c.active = TRUE) AND pi.cover = TRUE
                      ORDER BY cc.cartid, cc.insert_date"""


SELECT_USER_CARTID = """SELECT cartid FROM cart WHERE userid = %s AND active = TRUE;"""


UPDATE_USERNAME = """UPDATE account_info
                          SET username = %s
                          WHERE accountid = (SELECT u.accountid FROM cg_user AS u WHERE u.userid = %s) RETURNING username"""


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
                                            WHERE payment_method.userid = %s
                                                  AND payment_method.payment_methodid = %s
                                                  AND payment_method.payment_methodid
                                                  NOT IN (
                                                        SELECT up.payment_methodid FROM user_preferences up
                                                        WHERE up.payment_methodid = payment_method.payment_methodid
                                                      )
                                            RETURNING payment_methodid"""


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
                  WHERE userid = %s ORDER BY oid DESC"""


INSERT_EMPTY_ORDER = """INSERT INTO orders (cartid, shipment_feeid, order_statusid, shipping_addressid, userid, payment_methodid, order_date, order_total)
                        VALUES(%s,%s, 2, %s, %s, %s, current_date, 0) RETURNING orderid"""


INSERT_ORDER_DETAILS = """INSERT INTO order_details (orderid, productid, product_price, product_qty)
                          (SELECT %s AS orderid, productid,
                          CASE
                                WHEN (p.productid IN ( SELECT offer.productid
                                   FROM offer
                                  WHERE ((offer.offer_start_date <= ('now'::text)::date) AND (offer.offer_end_date > ('now'::text)::date)))) THEN (( SELECT min(o.offer_price) AS min
                                   FROM offer o
                                  WHERE ((o.productid = p.productid) AND (o.offer_start_date <= ('now'::text)::date) AND (o.offer_end_date > ('now'::text)::date))))::real
                                ELSE (p.product_price)
                            END AS product_price,
                          cart_product_qty as product_qty
                          FROM cart_contains JOIN product p USING (productid)
                          WHERE cartid = %s)
                          RETURNING *"""


UPDATE_USER_PREFERRED_BILLING_ADDR = """UPDATE user_preferences SET billing_addressid = %s WHERE userid = %s RETURNING *"""


UPDATE_USER_PREFERRED_SHIPPING_ADDR = """UPDATE user_preferences SET shipping_addressid = %s WHERE userid = %s RETURNING *"""


UPDATE_USER_PREFERRED_PAYMENT = """UPDATE user_preferences SET payment_methodid = %s WHERE userid = %s RETURNING *"""


UPDATE_USER_PASSWORD_ADMIN = """update account_info set upassword = crypt(%s, gen_salt('md5')) where accountid = %s RETURNING *"""


SELECT_USER_PREFERENCES = """SELECT * FROM user_preferences WHERE userid = %s"""


SELECT_USER_MAX_PAYMENT_ID = """SELECT max(payment_methodid) as pid FROM payment_method WHERE userid = %s"""


SELECT_SEARCH_TITLE = """SELECT * FROM product_details WHERE lower(title) LIKE lower(%s)"""

SELECT_SEARCH_NAVBAR = """ SELECT * FROM product_details WHERE platformid = %s and genre = %s and category = %s """


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
                      CASE WHEN addressid IN (SELECT up1.billing_addressid FROM user_preferences up1 WHERE up1.userid =%s) THEN TRUE
                        WHEN  addressid IN (SELECT up2.shipping_addressid FROM user_preferences up2 WHERE up2.userid =%s) THEN TRUE
                        ELSE FALSE END AS apreferred
                      FROM address
                      WHERE userid = %s AND addressid NOT IN (SELECT billing_addressid FROM payment_method pm WHERE pm.userid = %s) AND address.active = TRUE"""


SELECT_USER_BILLING_ADDRESS = """SELECT address_state AS aState, address_line_1 AS aaddress1, address_line_2 AS aaddress2, address_city AS acity,
                                  address_country AS acountry, active AS acurrent, address_fullname AS afullname, addressid AS aid,
                                  address_zip AS azip, 'billing' AS atype,
                                  CASE WHEN addressid IN (SELECT up1.billing_addressid FROM user_preferences up1 WHERE up1.userid =%s) THEN TRUE
                                    WHEN  addressid IN (SELECT up2.shipping_addressid FROM user_preferences up2 WHERE up2.userid =%s) THEN TRUE
                                    ELSE FALSE END AS apreferred
                                  FROM address
                                  WHERE userid = %s AND addressid IN (SELECT billing_addressid FROM payment_method pm WHERE pm.userid = %s) AND address.active = TRUE"""


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

SELECT_ALL_PRODUCTS = """SELECT * FROM admin_product_details"""


DEACTIVATE_ACCOUNT = """UPDATE account_info SET active = FALSE WHERE account_info.accountid = %s RETURNING *;"""

ACTIVATE_ACCOUNT = """UPDATE account_info SET active = TRUE WHERE account_info.accountid = %s RETURNING *;"""

DEACTIVATE_USER = """UPDATE cg_user SET active = FALSE WHERE cg_user.accountid = %s RETURNING *;"""

ACTIVATE_USER = """UPDATE cg_user SET active = TRUE WHERE cg_user.accountid = %s RETURNING *;"""

INSERT_ADMIN_USER = """INSERT INTO account_info (username, upassword, roleid, active)
                          VALUES (%s, crypt(%s, gen_salt('md5')), 3, TRUE) RETURNING accountid"""


SELECT_ALL_ORDERS = """SELECT o.orderid, o.userid, u.user_firstname, u.user_lastname, u.email, o.order_date, o.order_total, s.order_status_name, o.order_statusid
                        FROM orders AS o JOIN cg_user as u USING (userid)
                        JOIN order_status AS s USING(order_statusid)"""

SELECT_ESRB_RATING = """SELECT * from esrb_rating"""

SELECT_ALL_PLATFORMS = """SELECT * FROM platform"""

SELECT_ALL_CATEGORIES = """ SELECT category FROM category"""

SELECT_ALL_ANNOUNCEMENTS = """SELECT paid AS aid, pa_title AS a_title, pa_img AS a_img, platformid, active FROM platform_announcements
                               UNION ALL
                               SELECT said AS aid,sa_title AS a_title ,sa_img AS a_img, 0 AS platformid, active FROM store_announcement
                               ORDER BY platformid, aid"""

DEACTIVATE_PLATFORM = """UPDATE platform SET active = FALSE WHERE platformid = %s RETURNING *"""

SELECT_GENRES = """SELECT genre FROM genre"""

DEACTIVATE_PRODUCT = """UPDATE product SET active = FALSE WHERE productid = %s RETURNING *"""


SELECT_IDS = """SELECT c.categoryid, e.esrbid, g.genreid FROM category c, esrb_rating e, genre g WHERE c.category = %s AND e.esrb_rate = %s AND g.genre=%s"""


INSERT_PRODUCT = """INSERT INTO product (categoryid, genreid, esrbid, platformid, product_price,
                     release_date, product_qty, product_description, prodcut_additional_info,
                     active, product_title) VALUES (%s,%s,%s,%s,%s,to_date(%s,'YYYY-MM-DD'),%s,%s,%s,%s,%s) RETURNING productid"""


INSERT_PRODUCT_OFFER = """INSERT INTO offer (productid, offer_price, offer_start_date, offer_end_date) VALUES (%s, %s, to_date(%s,'YYYY-MM-DD'), to_date(%s,'YYYY-MM-DD')) RETURNING *"""


INSERT_PRODUCT_COVER = """INSERT INTO product_img (productid, product_img, cover) VALUES (%s, %s, TRUE) RETURNING *"""


SELECT_ALL_STATUS = """SELECT * FROM order_status"""


IS_USERNAME_TAKEN = """SELECT count(*) > 0 AS taken FROM account_info WHERE username = %s"""


IS_EMAIL_TAKEN = """SELECT count(*) > 0 AS taken FROM cg_user WHERE email = %s"""


CHANGE_ORDER_STATUS = """UPDATE orders SET order_statusid = %s WHERE orderid = %s RETURNING *"""


DEACTIVATE_STORE_ANNOUNCEMENTS = """ UPDATE store_announcement SET active = FALSE WHERE said = %s RETURNING said"""


DEACTIVATE_PLATFORM_ANNOUNCEMENTS = """ UPDATE platform_announcements SET active = FALSE WHERE paid = %s RETURNING paid"""


UDPATE_ADMIN_PRODUCT = """UPDATE product
                          SET product_title = %s, genreid = %s, esrbid = %s, release_date = to_date(%s, 'YYYY-MM-DD'),
                          product_price = %s, product_qty = %s, product_description = %s,prodcut_additional_info = %s, categoryid = %s, platformid =  %s, active = %s
                          WHERE productid = %s
                          RETURNING *"""


UPDATE_USER_PASSWORD = """update account_info
                          set upassword = crypt(%s, gen_salt('md5'))
                          where accountid = (select accountid from cg_user where userid = %s)
                          RETURNING *"""


UPDATE_OFFER = """UPDATE offer
                  SET offer_price = %s, offer_start_date = to_date(%s, 'YYYY-MM-DD'), offer_end_date = to_date(%s, 'YYYY-MM-DD')
                  WHERE productid = %s AND offerid = %s
                  RETURNING *"""


UPDATE_PLATFORM_ANNOUNCEMENTS = """UPDATE platform_announcements
                                    SET pa_img = %s, pa_title = %s, active = %s
                                    WHERE paid = %s AND platformid = %s
                                    RETURNING *"""


UPDATE_STORE_ANNOUNCEMENTS = """UPDATE store_announcement
                                SET sa_img = %s, sa_title = %s, active = %s
                                WHERE said = %s
                                RETURNING said"""


INSERT_PLATFORM_ANNOUNCEMENTS = """INSERT INTO platform_announcements (pa_title, pa_img, platformid, active)
                                   VALUES (%s, %s, %s, %s)
                                   RETURNING paid"""


INSERT_STORE_ANNOUNCEMENTS = """INSERT INTO store_announcement (sa_img, sa_title, active)
                                VALUES (%s, %s, %s)
                                RETURNING said"""

UPDATE_MULTIPLE_PAYMENT_ADDRESS_ID = """UPDATE payment_method
                            SET billing_addressid = %s
                            WHERE billing_addressid = %s AND userid =%s
                            RETURNING *"""


UPDATE_PAYMENT_ADDRESS_ID = """UPDATE payment_method
                            SET billing_addressid = %s
                            WHERE payment_methodid = %s AND userid =%s
                            RETURNING *"""

UPDATE_PRODUCT_QTY = """UPDATE product SET product_qty = product_qty - %s WHERE productid = %s"""

SELECT_ALL_GENRES = """SELECT * FROM genre"""


UPDATE_USER_FNAME = """UPDATE cg_user AS u
                        SET user_firstname = %s
                        WHERE u.userid = %s
                        RETURNING *"""


UPDATE_USER_LNAME = """UPDATE cg_user AS u
                        SET user_lastname = %s
                        WHERE u.userid = %s
                        RETURNING *"""


UPDATE_USER_EMAIL = """UPDATE cg_user AS u
                        SET email = %s
                        WHERE u.userid = %s
                        RETURNING *"""


UPDATE_USER_PHONE = """UPDATE cg_user AS u
                        SET phone = %s
                        WHERE u.userid = %s
                        RETURNING *"""


UPDATE_USER_DOB = """UPDATE cg_user AS u
                        SET dob = to_date(%s, 'YYYY-MM-DD')
                        WHERE u.userid = %s
                        RETURNING *"""

DEACTIVATE_GENRE = """ UPDATE genre SET active = FALSE WHERE genreid = %s RETURNING *"""

ACTIVATE_GENRE = """UPDATE genre SET active = TRUE WHERE genreid = %s RETURNING *"""

UPDATE_PRODUCT_COVER = """UPDATE product_img SET product_img = %s WHERE productid = %s AND cover = TRUE RETURNING *"""

INSERT_GENRE = """insert INTO genre (genre, active)
                  VALUES (%s,%s)
                  RETURNING genreid"""