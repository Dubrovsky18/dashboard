
import database
from database import execute_query, query_external_supplies, query_checks, query_products_on_shelves
from init_database import conn_small, conn_prod
import init_database

events_small = {}
shelves_count_small = {}
categories_small = []

events_prod = {}
shelves_count_prod = {}
categories_prod = []


def init_data_small():
    external_supplies_data_small = execute_query(query_external_supplies, conn_small)
    checks_data_small = execute_query(query_checks, conn_small)
    products_on_shelves_data_small = execute_query(query_products_on_shelves, conn_small)
    for _, row in external_supplies_data_small.iterrows():
        date = row['date']
        category = row['category_name']
        sum_products_finish_date = row['sum_products_finish_date']
        if date not in events_small:
            events_small[date] = []
        if category not in categories_small:
            categories_small.append(category)
        events_small[date].append({'type': 'external_supply', 'data': {'category_name': category, 'product_count': int(sum_products_finish_date)}})
    for _, row in checks_data_small.iterrows():
        date = row['date']
        category = row['category_name']
        sum_products_issue_date = row['sum_products_issue_date']
        if date not in events_small:
            events_small[date] = []
        if category not in categories_small:
            categories_small.append(category)
        events_small[date].append({'type': 'check', 'data': {'category_name': category, 'product_count': int(sum_products_issue_date)}})
    for _, row in products_on_shelves_data_small.iterrows():
        shelves_count_small[row['category_name']] = row['shelves_count']

def init_date_prod():
    external_supplies_data_prod = execute_query(query_external_supplies, conn_prod)
    checks_data_prod = execute_query(query_checks, conn_prod)
    products_on_shelves_data_prod = execute_query(query_products_on_shelves, conn_prod)
    for _, row in external_supplies_data_prod.iterrows():
        date = row['date']
        category = row['category_name']
        sum_products_finish_date = row['sum_products_finish_date']
        if date not in events_prod:
            events_prod[date] = []
        if category not in categories_prod:
            categories_prod.append(category)
        events_prod[date].append({'type': 'external_supply', 'data': {'category_name': category, 'product_count': int(sum_products_finish_date)}})
    for _, row in checks_data_prod.iterrows():
        date = row['date']
        category = row['category_name']
        sum_products_issue_date = row['sum_products_issue_date']
        if date not in events_prod:
            events_prod[date] = []
        if category not in categories_prod:
            categories_prod.append(category)
        events_prod[date].append({'type': 'check', 'data': {'category_name': category, 'product_count': int(sum_products_issue_date)}})
    for _, row in products_on_shelves_data_prod.iterrows():
        shelves_count_prod[row['category_name']] = row['shelves_count']

def take_data(schema):
    if schema == 'prod':
        return events_prod, shelves_count_prod, categories_prod
    elif schema == 'small':
        return events_small, shelves_count_small, categories_small


