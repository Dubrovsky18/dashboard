import pandas as pd
import psycopg2


def execute_query(sql_query, conn):
    with conn.cursor() as cur:
        cur.execute(sql_query)
        columns = [desc[0] for desc in cur.description]
        result = pd.DataFrame(cur.fetchall(), columns=columns)
    return result

def connection_to_database(schema):
    return psycopg2.connect(
        database='appdb',
        user='app',
        password='verysecretpassword',
        host='62.84.126.82',
        port=5432,
        options=f'-c search_path={schema}'
    )

query_external_supplies = """
SELECT
    es.finish_date AS date,
    c.name AS category_name,
    SUM(esp.product_count) AS sum_products_finish_date
FROM
    external_supplies es
        LEFT JOIN external_supplies_products esp ON esp.ext_supply_id = es.ext_supply_id
        LEFT JOIN product_categories pc ON esp.product_id = pc.product_id
        LEFT JOIN categories c ON pc.category_id = c.category_id
WHERE
    esp.product_count IS NOT NULL
GROUP BY
    es.finish_date, c.name
ORDER BY
    es.finish_date;

        """

query_checks = """
SELECT
    ch.issue_date AS date,
    cat.name AS category_name,
    SUM(pcp.product_count) AS sum_products_issue_date
FROM
    checks ch
        LEFT JOIN product_check_positions pcp ON pcp.check_id = ch.check_id
        LEFT JOIN product_categories pc ON pcp.product_id = pc.product_id
        LEFT JOIN categories cat ON pc.category_id = cat.category_id
WHERE
    pcp.product_count IS NOT NULL
GROUP BY
    ch.issue_date, cat.name
ORDER BY ch.issue_date ASC;
        """

query_products_on_shelves = """
SELECT
    c.name AS category_name,
    SUM(pos.product_count) AS shelves_count
FROM
    products_on_shelves pos
        JOIN product_categories pc ON pos.product_id = pc.product_id
        JOIN categories c ON pc.category_id = c.category_id
WHERE
    pos.product_count IS NOT NULL
GROUP BY
    c.name;
        """

