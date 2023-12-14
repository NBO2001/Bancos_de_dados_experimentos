from connect import exec_query

ID_PRODUCT = 38

sql_question_b = """
SELECT p2.product_id, p2.asin, p2.title, p2.salesrank
FROM products p1
JOIN productproduct pp ON pp.product_id_fk = p1.product_id
JOIN products p2 ON p2.asin = pp.referenc_asin
WHERE p1.product_id = %s AND p2.salesrank < p1.salesrank
order by p2.salesrank;
"""


resuls = exec_query(query=[sql_question_b, (ID_PRODUCT, )], is_select=True)

print(f"Questão B, os similares ao produto de id {ID_PRODUCT} são:")

if len(resuls) == 0:
    print("\t - Sem resultados encontrados!")
for resul in resuls:
    print(resul)
