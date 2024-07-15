import datetime
import pandas as pd
import psycopg2
import streamlit as st
import time
# from sshtunnel import SSHTunnelForwarder
#
# tunnel = SSHTunnelForwarder(
#     ('62.84.126.82', 22),
#     ssh_username='dubrovin02',
#     ssh_private_key='/Users/test/.ssh/id_rsa',
#     remote_bind_address=('localhost', 5432),
# )
# tunnel.start()




def execute_query(sql_query, conn):
    with conn.cursor() as cur:
        cur.execute(sql_query)
        columns = [desc[0] for desc in cur.description]
        result = pd.DataFrame(cur.fetchall(), columns=columns)
    return result


query_external_supplies = """
SELECT * FROM mv_external_supplies
ORDER BY date, category_name ASC;
        """

query_checks = """
SELECT * FROM mv_product_summary
ORDER BY date, category_name ASC;
        """
        
query_products_on_shelves = """
SELECT * FROM mv_shelve_count
ORDER BY category_name ASC;
        """



schema = st.selectbox('Select schema', ('prod', 'small'), key='schema_selector')

start_time = time.time()

conn = psycopg2.connect(
    database='appdb',
    user='app',
    password='verysecretpassword',
    host='localhost',
    port=5432,
    options=f'-c search_path={schema} -c work_mem=512MB'
)

# conn = psycopg2.connect(
#     database='appdb',
#     user='app',
#     password='verysecretpassword',
#     host=tunnel.local_bind_host,
#     port=tunnel.local_bind_port,
#     options=f'-c search_path={schema}'
# )

external_supplies_data = execute_query(query_external_supplies, conn)
checks_data = execute_query(query_checks, conn)
products_on_shelves_data = execute_query(query_products_on_shelves, conn)

events = {}
shelves_count = {}
categories = []

for _, row in external_supplies_data.iterrows():
    date = row['date']
    category = row['category_name']
    sum_products_finish_date = row['sum_products_finish_date']
    if date not in events:
        events[date] = []
    if category not in categories:
        categories.append(category)
    events[date].append({'type': 'external_supply', 'data': {'category_name': category, 'product_count': int(sum_products_finish_date)}})

for _, row in checks_data.iterrows():
    date = row['date']
    category = row['category_name']
    sum_products_issue_date = row['sum_products_issue_date']
    if date not in events:
        events[date] = []
    if category not in categories:
        categories.append(category)
    events[date].append({'type': 'check', 'data': {'category_name': category, 'product_count': int(sum_products_issue_date)}})

for _, row in products_on_shelves_data.iterrows():
    shelves_count[row['category_name']] = row['shelves_count']

index = [x.strftime('%Y-%m-%d') for x in sorted(events.keys())]
first_date = min(events.keys())

graph_data = {category: [0] * (len(index)+1) for category in categories}

for category_name in graph_data:
    graph_data[category_name][-1] = shelves_count[category_name]

first = list(sorted(events.keys()))[0]
events[first - datetime.timedelta(days=1)] = []
index = [(first_date - datetime.timedelta(days=1)).strftime('%Y-%m-%d')] + index

diffs = {}
offset = 0

for event_date in reversed(sorted(events.keys())):


    day_events = events[event_date]
    if offset != 0:
        for category in graph_data:
            graph_data[category][-1 - offset] = graph_data[category][-1-(offset-1)] + diffs.get(category, 0)
    diffs.clear()
    for event in day_events:
        category = event['data']['category_name']
        if event['type'] == 'check':
            if category not in diffs:
                diffs[category] = 0
            diffs[category] += event['data']['product_count']
        elif event['type'] == 'external_supply':
            if category not in diffs:
                diffs[category] = 0
            diffs[category] -= event['data']['product_count']
    offset += 1
data = pd.DataFrame(data=graph_data, index=index)
elapsed_time = time.time() - start_time
print(elapsed_time)
st.write(f"Время выполнения: {elapsed_time:.2f} секунд")
st.area_chart(data)


query_refresh = ("""
    REFRESH MATERIALIZED VIEW mv_shelve_count;
    REFRESH MATERIALIZED VIEW mv_external_supplies;
    REFRESH MATERIALIZED VIEW mv_product_summary;
""")
external_supplies_data = execute_query(query_refresh, conn)

