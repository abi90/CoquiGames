
"""
Query for fetching all prodcuts
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
                                  FROM product AS P NATURAL JOIN genre AS G
                                  WHERE categoryid IN (SELECT C.categoryid FROM category AS C WHERE C.category = 'Game') AND P.platformid = {0}"""


SELECT_PLATFORM_ACCESORIES = """SELECT DISTINCT G.genre
                                  FROM product AS P NATURAL JOIN genre AS G
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

SELECT_ACCOUNT_INFO = """SELECT * FROM account_info
WHEN username = '{0}' AND accountid = {1} AND upassword = crypt('{2}',upassword)"""








