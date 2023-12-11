from connect import exec_query

ID_PRODUCT = 296

sql_question_c = """
SELECT date,
sum(rating)/count(date) as avg_avaliacao 
FROM reviews
WHERE product_id_fk = %s
GROUP BY date
ORDER BY date;
"""

sql_question_c_v2 = """
SELECT date, sum(rating) as rating_sum, 
sum(votes) as votes_sum, 
count(date), sum(rating)/count(date) as avg_avaliacao 
FROM reviews
WHERE product_id_fk = %s
GROUP BY date
ORDER BY date;
"""


resuls = exec_query(query=[sql_question_c, (ID_PRODUCT, )], is_select=True)

print(f"Questão C, a evolução diária do id {ID_PRODUCT} é:")

if len(resuls) == 0:
    print("\t - Sem resultados encontrados!")
for resul in resuls:
    print(resul)
