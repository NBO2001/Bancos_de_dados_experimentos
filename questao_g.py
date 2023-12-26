from connect import exec_query

sql = """
WITH RankedCustomers AS (
  SELECT
    r.customer_id,
    p.group_id_fk,
    COUNT(*) AS comment_count,
    RANK() OVER (PARTITION BY p.group_id_fk ORDER BY COUNT(*) DESC) AS customer_rank
  FROM
    reviews r
  JOIN
    products p ON r.product_id_fk = p.product_id
  GROUP BY
    r.customer_id, p.group_id_fk
)

SELECT
  rc.customer_rank,
  rc.customer_id,
  g.name
FROM
  RankedCustomers rc
JOIN
  groups g ON rc.group_id_fk = g.group_id
WHERE
  rc.customer_rank <= 10;
"""

results = exec_query(query=[sql], is_select=True)

print(f"Questão G, os 10 clientes que mais fizeram comentários por grupo de produto:")

if len(results) == 0:
    print("\t - Sem resultados encontrados!")
for result in results:
    print(result)
