import psycopg2

conn_small = psycopg2.connect(
    database='appdb',
    user='app',
    password='verysecretpassword',
    host='locahost',
    port=5432,
    options=f'-c search_path={'small'}'
)

conn_prod = psycopg2.connect(
    database='appdb',
    user='app',
    password='verysecretpassword',
    host='localhost',
    port=5432,
    options=f'-c search_path={'prod'}'
)


