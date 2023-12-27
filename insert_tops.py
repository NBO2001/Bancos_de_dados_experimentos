import sys
import concurrent.futures
from config import Config
from readfile import readFile
from item import Item
from connect import Connect
from category import Category

group_set = set()



def process_range(start: int, end: int):            
    # The idea is to be the function for inserting into the database.
    connect = Connect()

    def addDatabase(item: Item):
        
        if item.id < start or item.id > end:
            return

        group_insert_sql = """
        INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING
        """
        product_insert_sql = """
        INSERT INTO products (product_id, asin, title, salesrank, total_reviews, group_id_fk)
        VALUES (%s,%s,%s,%s,%s, (SELECT group_id FROM groups WHERE name = %s))
        """

        category_insert_sql = """
        INSERT INTO category (category_id, name, parent_id)
        VALUES (%s,%s,%s) ON CONFLICT (category_id) DO NOTHING
        """

        reviews_insert_sql = """
        INSERT INTO reviews (date, rating, votes, helpful, customer_id, product_id_fk)
        VALUES (%s,%s,%s,%s,%s,%s)
        """

        productscategories_insert_sql = """
        INSERT INTO productscategories (product_id_fk, category_id_fk)
        VALUES (%s, %s)
        """

        productproduct_insert_sql = """
        INSERT INTO productproduct (product_id_fk, referenc_asin)
        VALUES (%s,  %s)
        """
        
        if item.group and item.group not in group_set:
            group_set.add(item.group)
            connect.exec_query(query=[group_insert_sql, (item.group, )])


        connect.exec_query(query=[product_insert_sql, (item.id, item.asin, item.title, item.salesrank, item.reviews[0], item.group)], debugger=True)

        if item.reviews[1]:

            for rvw in item.list_reviews:
                connect.exec_query(query=[reviews_insert_sql, (rvw.date,rvw.rating, rvw.votes, rvw.helpful, rvw.customer, item.id)])
        
        if item.categories:
            for category in item.categories:

                father:Category = category.pop(0)
                connect.exec_query(query=[category_insert_sql, (father.category_id, father.category_name, None)])

                for child in category:
                    connect.exec_query(query=[category_insert_sql, (child.category_id, child.category_name, father.category_id)])
                    father = child
                
                connect.exec_query(query=[productscategories_insert_sql, (item.id, father.category_id)])

        if item.similar:
            list_sims = [ x.strip() for x in item.similar.split(" ") if len(x.split()) ]
            tol_simis = int(list_sims.pop(0))

            if tol_simis:
                for simi in list_sims:
                    connect.exec_query(query=[productproduct_insert_sql, (item.id, simi)])        

    readFile(filename=path_file, callback=addDatabase)

    connect.close()


if __name__ == "__main__":

    conf = Config()
    path_file = "./downloads/amazon-meta.txt"

    # Define the ranges for multithreading
    # ranges = [
    #     (0, 50000),
    #     (50001, 100000),
    #     (100001, 150000),
    #     (150001, 200000),
    #     (200001, 250000),
    #     (250001, 300000),
    #     (300001, 350000),
    #     (350001, 400000),
    #     (400001, 450000),
    #     (450001, 500000),
    #     (500001, 600000),
    # ]

    ranges = [
        (450001, 500000),
        (500001, 600000),
    ]

    # Use multithreading to process different ranges concurrently
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(ranges)) as executor:
        executor.map(lambda r: process_range(*r), ranges)

    