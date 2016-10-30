
"""
Query for fetching all prodcuts
"""
SELECT_PRODUCT_DETAILS = """SELECT * FROM product_details WHERE pid = {0}"""

SELECT_LATEST_PRODUCTS = """SELECT *
                            FROM product_details
                            WHERE to_date(release,'YYYY-MM-DD') BETWEEN now()::DATE -  '30 days'::INTERVAL AND now()::DATE """

SELECT_SPECIAL_PRODUCTS = """SELECT *
                             FROM product_details
                             WHERE INOFFER = true"""
SELECT_PLATFORMS = """SELECT pa.platformid, pa.logoimg, pa.platform
                      FROM platform AS pa
                      WHERE pa.active = TRUE"""

SELECT_PLATFORM_CONSOLES = """SELECT productid, product_title
                                FROM product AS P
                                WHERE categoryid IN (SELECT C.categoryid FROM category AS C WHERE C.category='Console')
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
                                      AND P.platformid = {0}"""

SELECT_PLATFORM_SPECIAL_PRODUCTS = """SELECT *
                             FROM product_details
                             WHERE INOFFER = true AND pid = {0}"""