import streamlit as st
import pandas as pd
import before_database
from draw import draw_graph
import streamlit

import database

schema = st.selectbox('Select schema', ('small', 'prod'), key='schema_selector')

if schema == 'small':
    data = pd.DataFrame(data=streamlit.graph_data_small, index=streamlit.index_small)
    st.area_chart(data)
else:
    data = pd.DataFrame(data=streamlit.graph_data_prod, index=streamlit.index_prod)
    st.area_chart(data)







