import connection

path = "downloads/gambiarra"

class Item():
    id: int = None
    asin: str = ""
    title: str = ""
    group: str = ""
    salesrank: str = ""
    similars: list = None
    categories: list = list()
    reviews: dict = { "total": 0, "downloaded": 0, "avg rating": 0 }
    list_reviews: list = list()

    def __str__(self):
        return (f"id: {self.id}\n"
            f"asin: {self.asin}\n"
            f"title: {self.title}\n"
            f"group: {self.group}\n"
            f"salesrank: {self.salesrank}\n"
            f"similars: {self.similars}\n"
            f"categories: {self.categories[:5]}\n"
            f"reviews: {self.reviews}\n"
            f"dowloaded: {self.list_reviews[:5]}\n")

def main():
    conn, cur = connection.get_connection()
    item = Item()
    category_count = 0
    reviews_count = 0
    with open(path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            if category_count > 0:
                item.categories.append(line)
                category_count -= 1
                continue

            data = [term.strip() for term in line.split(":")]
            if reviews_count > 0:
                item.list_reviews.append({
                    "date": data[0].split(" ")[0],
                    "customer_id": data[1].split(" ")[0],
                    "rating": int(data[2].split(" ")[0]),
                    "votes": int(data[3].split(" ")[0]),
                    "helpful": int(data[-1])
                })
                reviews_count -= 1
                continue

            match data[0]:
                case "Id":
                    if item.id:
                        insert(item=item, conn=conn, cur=cur)
                    item.id = int(data[1])
                case "ASIN":
                    item.asin = data[1]
                case "title":
                    item.title = ": ".join(data[1:])
                case "group":
                    item.group = data[1]
                case "salesrank":
                    item.salesrank = int(data[1])
                case "similar":
                    similars = data[1].split("  ")
                    item.similars = similars[1:]
                case "categories":
                    category_count = int(data[1])
                    item.categories = list()
                case "reviews":
                    item.reviews["total"] = int(data[2].split(" ")[0])
                    item.reviews["downloaded"] = int((data[3].split(" "))[0])
                    item.reviews["avg rating"] = float(data[-1])
                    item.list_reviews = list()
                    reviews_count = item.reviews["downloaded"]
                case _:
                    item = Item()
    if item.id:
        insert(conn=conn, cur=cur, item=item)
    cur.close()
    conn.close()
                
def insert(item, conn, cur):
    group_insert_sql = """
    INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING
    """
    connection.execute_query(conn=conn, cur=cur, query=[group_insert_sql, (item.group,)])

    product_insert_sql = """
    INSERT INTO products (product_id, asin, title, salesrank, total_reviews, group_id_fk)
    VALUES (%s,%s,%s,%s,%s, (SELECT group_id FROM groups WHERE name = %s))
    """
    connection.execute_query(conn=conn, cur=cur, query=[product_insert_sql, (item.id, item.asin, item.title, item.salesrank, item.reviews["total"], item.group,)])

    category_insert_sql = """
    INSERT INTO category (category_id, name, parent_id)
    VALUES (%s,%s,%s) ON CONFLICT (category_id) DO NOTHING
    """

    productscategories_insert_sql = """
    INSERT INTO productscategories (product_id_fk, category_id_fk)
    VALUES (%s, %s) ON CONFLICT ( product_id_fk, category_id_fk ) DO NOTHING
    """
    for category in item.categories:
        category = [cat for cat in category.split("|") if cat]
        first_category = category.pop(0).split("[")
        root_id = first_category[1][:-1]
        root_name = first_category[0]
        connection.execute_query(conn=conn, cur=cur, query=[category_insert_sql, (root_id, root_name, None)])
        for sub_category in category:
            sub_category = sub_category.split("[")
            sub_category_name = sub_category[0]
            sub_category_id = int(sub_category[1][:-1])
            connection.execute_query(conn=conn, cur=cur, query=[category_insert_sql, (sub_category_id, sub_category_name, root_id,)])
            root_id = sub_category_id
        connection.execute_query(conn=conn, cur=cur, query=[productscategories_insert_sql, (item.id, root_id,)])

    reviews_insert_sql = """
    INSERT INTO reviews (date, rating, votes, helpful, customer_id, product_id_fk)
    VALUES (%s,%s,%s,%s,%s,%s)
    """
    for review in item.list_reviews:
        connection.execute_query(conn=conn, cur=cur, query=[reviews_insert_sql, (review["date"], review["rating"], review["votes"], review["helpful"], review["customer_id"], item.id,)])


    productproduct_insert_sql = """
    INSERT INTO productproduct (product_id_fk, referenc_asin)
    VALUES (%s,  %s)
    """
    for similar in item.similars:
        connection.execute_query(conn=conn, cur=cur, query=[productproduct_insert_sql, (item.id, similar,)])

if __name__ == "__main__":
    main()