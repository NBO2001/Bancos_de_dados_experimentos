import psycopg2

def get_connection():
    conn = psycopg2.connect(
        host="localhost",
        port= 5432,
        database="postgres",
        user="postgres",
        password="db123")
    cur = conn.cursor()
    return conn, cur


def execute_query(query, cur, conn, is_select=False):
    cur.execute(*query)
    print(cur.query.decode("utf-8").strip())
    result = list()
    if is_select:
        result = cur.fetchall()
    else:
        conn.commit()
    return result