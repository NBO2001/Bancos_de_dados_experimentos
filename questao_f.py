from connect import exec_query


sql_question_f = """
WITH RECURSIVE category_tree AS (
    (SELECT ct.category_id, ct.name, ct.parent_id
    FROM category ct
    JOIN productscategories ON ct.category_id = category_id_fk
    JOIN products ON product_id = product_id_fk
    JOIN reviews ON reviews.product_id_fk = product_id
    GROUP BY ct.category_id, product_id
    HAVING AVG(CASE WHEN helpful > 0 THEN rating ELSE NULL END) IS NOT NULL AND AVG(CASE WHEN helpful > 0 THEN helpful ELSE NULL END) IS NOT NULL
    ORDER BY AVG(CASE WHEN helpful > 0 THEN rating ELSE NULL END) DESC, AVG(CASE WHEN helpful > 0 THEN helpful ELSE NULL END) DESC
    LIMIT 5)

    UNION ALL

    SELECT c.category_id, c.name, c.parent_id
    FROM category c
    JOIN category_tree ct ON c.category_id = ct.parent_id
) SELECT *
FROM category_tree;
"""

resuls = exec_query(query=[sql_question_f], is_select=True)

if len(resuls) == 0:
    print("\t - Sem resultados encontrados!")
for resul in resuls:
    print(resul)