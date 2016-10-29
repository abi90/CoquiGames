
"""
Query for fetching all prodcuts
"""
SELECT_PRODUCT_DETAILS = """SELECT * FROM product_details"""

SELECT_LATEST_PRODUCTS = """SELECT *
                            FROM product_details
                            WHERE to_date(release,'YYYY-MM-DD') BETWEEN now()::DATE -  '30 days'::INTERVAL AND now()::DATE """

SELECT_SPECIAL_PRODUCTS = """SELECT *
                             FROM product_details
                             WHERE INOFFER = true"""