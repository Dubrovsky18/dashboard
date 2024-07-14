import streamlit as st
import pandas as pd
import before_database
from draw import draw_graph

import database
before_database.init_data_small()
before_database.init_date_prod()

events, shelves_count, categories = before_database.take_data('prod')
graph_data_prod, index_prod = draw_graph(events, shelves_count, categories)

events, shelves_count, categories = before_database.take_data('small')
graph_data_small, index_small = draw_graph(events, shelves_count, categories)

schema = st.selectbox('Select schema', ('small', 'prod'), key='schema_selector')

if schema == 'small':
    data = pd.DataFrame(data=graph_data_small, index=index_small)
    st.area_chart(data)
else:
    data = pd.DataFrame(data=graph_data_prod, index=index_prod)
    st.area_chart(data)







