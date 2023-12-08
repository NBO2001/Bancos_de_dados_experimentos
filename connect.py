import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port= 5432,
    database="postgres",
    user="postgres",
    password="db123")

cur = conn.cursor()


query = """
CREATE TABLE products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    category VARCHAR(50)
)
"""

cur.execute(query)

# Commit the changes to the database
conn.commit()

# Close the cursor and connection
cur.close()
conn.close()