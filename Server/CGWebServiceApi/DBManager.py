import os
import psycopg2
import urlparse
import QueryManager as Query
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


def fetch_special_products():
    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute(Query.SELECT_SPECIAL_PRODUCTS)

        columns = [x[0] for x in cur.description]
        results = []
        for row in cur.fetchall():
            results.append(dict(zip(columns, row)))
        for e in results:
            print e
        conn.close()
        return results
    except Exception as e:
        print e


def fetch_latest_products():
    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute(Query.SELECT_LATEST_PRODUCTS)

        columns = [x[0] for x in cur.description]
        results = []
        for row in cur.fetchall():
            results.append(dict(zip(columns, row)))
        for e in results:
            print e
        conn.close()
        return results
    except Exception as e:
        print e


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


def fetch_special_products():
    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute(Query.SELECT_SPECIAL_PRODUCTS)

        columns = [x[0] for x in cur.description]
        results = []
        for row in cur.fetchall():
            results.append(dict(zip(columns, row)))
        for e in results:
            print e
        conn.close()
        return results
    except Exception as e:
        print e


def fetch_product(productid):
    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute(Query.SELECT_PRODUCT_DETAILS.format(productid))

        columns = [x[0] for x in cur.description]
        result = dict(zip(columns, cur.fetchall()[0]))
        print result
        conn.close()
        return result
    except Exception as e:
        print e


def fetch_platform_latest_products(platformid):
    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute(Query.SELECT_PLATFORM_LATEST_PRODUCTS.format(platformid))

        columns = [x[0] for x in cur.description]
        results = []
        for row in cur.fetchall():
            results.append(dict(zip(columns, row)))

        for e in results:
            print e

        conn.close()
        return results
    except Exception as e:
        print e


def fetch_platform_special_products(platformid):
    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute(Query.SELECT_PLATFORM_SPECIAL_PRODUCTS.format(platformid))

        columns = [x[0] for x in cur.description]
        results = []
        for row in cur.fetchall():
            results.append(dict(zip(columns, row)))

        for e in results:
            print e

        conn.close()
        return results
    except Exception as e:
        print e


#fetch_products()
#fetch_latest_products()
#fetch_special_products()
#fetch_platforms()
#fetch_product(2)
#fetch_platform_latest_products(1)
#fetch_platform_special_products(4)
