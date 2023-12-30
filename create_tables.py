from connect import exec_query

groups = """
CREATE TABLE IF NOT EXISTS groups (
    group_id SERIAL PRIMARY KEY NOT NULL,
    name VARCHAR(50) UNIQUE
)
"""

products = """
CREATE TABLE IF NOT EXISTS products (
    product_id INTEGER NOT NULL,
    asin CHAR(10) NOT NULL UNIQUE,
    title VARCHAR(255),
    salesrank BIGINT,
    total_reviews INTEGER,
    group_id_fK INTEGER,
    PRIMARY KEY (product_id),
    FOREIGN KEY (group_id_fk) REFERENCES groups (group_id) ON DELETE CASCADE
)
"""

reviews = """
CREATE TABLE IF NOT EXISTS reviews (
    review_id SERIAL NOT NULL,
    date DATE,
    rating INTEGER,
    votes INTEGER,
    helpful INTEGER,
    customer_id CHAR(15),
    product_id_fk INTEGER,
    PRIMARY KEY (review_id),
    FOREIGN KEY (product_id_fk) REFERENCES products (product_id) ON DELETE CASCADE
)
"""

category = """
    CREATE TABLE IF NOT EXISTS category (
        category_id INTEGER NOT NULL,
        name VARCHAR(50),
        parent_id INTEGER,
        PRIMARY KEY (category_id),
        FOREIGN KEY (parent_id) REFERENCES category (category_id) ON DELETE CASCADE
    )
"""

products_category = """
    CREATE TABLE IF NOT EXISTS ProductsCategories (
        product_id_fk INTEGER NOT NULL,
        category_id_fk INTEGER NOT NULL,
        PRIMARY KEY (product_id_fk, category_id_fk),
        FOREIGN KEY (product_id_fk) REFERENCES products (product_id) ON DELETE CASCADE,
        FOREIGN KEY (category_id_fk) REFERENCES category (category_id) ON DELETE CASCADE
    )
"""

product_product = """
 CREATE TABLE IF NOT EXISTS ProductProduct (
    product_id_fk INTEGER NOT NULL,
    referenc_asin CHAR(10) NOT NULL,
    FOREIGN KEY (product_id_fk) REFERENCES products (product_id) ON DELETE CASCADE
 )
"""

tables = [groups, products, reviews, category, products_category, product_product]

for table in tables:
    exec_query(query=[table,], debugger=True)
