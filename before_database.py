
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
    events = {}
    shelves_count = {}
    categories = []
    for _, row in external_supplies_data_small.iterrows():
        date = row['date']
        category = row['category_name']
        sum_products_finish_date = row['sum_products_finish_date']
        if date not in events:
            events[date] = []
        if category not in categories:
            categories.append(category)
        events[date].append({'type': 'external_supply', 'data': {'category_name': category, 'product_count': int(sum_products_finish_date)}})
    for _, row in checks_data_small.iterrows():
        date = row['date']
        category = row['category_name']
        sum_products_issue_date = row['sum_products_issue_date']
        if date not in events:
            events[date] = []
        if category not in categories:
            categories.append(category)
        events[date].append({'type': 'check', 'data': {'category_name': category, 'product_count': int(sum_products_issue_date)}})
    for _, row in products_on_shelves_data_small.iterrows():
        shelves_count[row['category_name']] = row['shelves_count']
    events_small = events
    shelves_count_small = shelves_count
    categories_small = categories

def init_date_prod():
    external_supplies_data_prod = execute_query(query_external_supplies, conn_prod)
    checks_data_prod = execute_query(query_checks, conn_prod)
    products_on_shelves_data_prod = execute_query(query_products_on_shelves, conn_prod)
    events = {}
    shelves_count = {}
    categories = []
    for _, row in external_supplies_data_prod.iterrows():
        date = row['date']
        category = row['category_name']
        sum_products_finish_date = row['sum_products_finish_date']
        if date not in events:
            events[date] = []
        if category not in categories:
            categories.append(category)
        events[date].append({'type': 'external_supply', 'data': {'category_name': category, 'product_count': int(sum_products_finish_date)}})
    for _, row in checks_data_prod.iterrows():
        date = row['date']
        category = row['category_name']
        sum_products_issue_date = row['sum_products_issue_date']
        if date not in events:
            events[date] = []
        if category not in categories:
            categories.append(category)
        events[date].append({'type': 'check', 'data': {'category_name': category, 'product_count': int(sum_products_issue_date)}})
    for _, row in products_on_shelves_data_prod.iterrows():
        shelves_count[row['category_name']] = row['shelves_count']
    events_prod = events
    shelves_count_prod = shelves_count
    categories_prod = categories

def take_data(schema):
    if schema == 'prod':
        return events_prod, shelves_count_prod, categories_prod
    elif schema == 'small':
        return events_small, shelves_count_small, categories_small


