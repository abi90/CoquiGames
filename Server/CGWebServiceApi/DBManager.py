import os
import psycopg2
import urlparse
import QueryManager as query
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
        cur.execute(query.SELECT_SPECIAL_PRODUCTS)

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
        cur.execute(query.SELECT_LATEST_PRODUCTS)

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

def fetch_products():
    try:
        conn = connection()
        cur = conn.cursor()
        cur.execute(query.SELECT_PRODUCT_DETAILS)

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
fetch_special_products()
