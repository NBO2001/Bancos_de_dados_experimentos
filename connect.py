import psycopg2

def exec_query(query: list, is_select: bool=False, debugger: bool = False) -> list:
    conn = psycopg2.connect(
        host="localhost",
        port= 5432,
        database="postgres",
        user="postgres",
        password="db123")
    results = []
    cur = conn.cursor()
    try:
        cur.execute(*query)

        if debugger:
            print(cur.query.decode("utf-8").strip())
        
        if is_select:
            results = cur.fetchall()
        else:
            # Commit the changes to the database
            conn.commit()
    except psycopg2.Error as e:
        print(f"ERROR: {e}")
    finally:
        # Close the cursor and connection
        cur.close()
        conn.close()
        return results