from connect import exec_query

ID_PRODUCT = 2

sql = f"""
(SELECT date, rating, votes, helpful, customer_id
FROM reviews
WHERE product_id_fk = {ID_PRODUCT}
ORDER BY helpful DESC, rating DESC
LIMIT 5)

UNION ALL

(SELECT date, rating, votes, helpful, customer_id
FROM reviews
WHERE product_id_fk = {ID_PRODUCT}
ORDER BY helpful DESC, rating ASC
LIMIT 5)
"""


results = exec_query(query=[sql], is_select=True)

print(f"Questão A\nOs 5 comentários mais úteis e com maior e menor avaliação do produto {ID_PRODUCT} são:")

if len(results) == 0:
    print("\t - Sem resultados encontrados!")
for result in results:
    print(result)
