from connect import exec_query

sql_question_d = """
SELECT product_id, title, salesrank, group_id_fk
FROM (
    SELECT product_id, title, salesrank, group_id_fk, ROW_NUMBER() OVER (PARTITION BY group_id_fk ORDER BY salesrank) AS group_index
    FROM products
    WHERE salesrank >= 0
)
WHERE group_index <= 10;
"""

resuls = exec_query(query=[sql_question_d], is_select=True)

if len(resuls) == 0:
    print("\t - Sem resultados encontrados!")
for resul in resuls:
    print(resul)
