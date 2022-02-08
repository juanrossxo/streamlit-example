from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import numpy as np

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""
sub_title = st.text_input("Name of Equipment")
st.title(sub_title + " Anchorage Calculation")

#set up df for subsections of equipment
equip = ['Architectural', 'Mechanical and Electrical']
equip_sel = pd.DataFrame(equip)
equip_sel
# df for equipment types
file = 'https://raw.githubusercontent.com/juanrossxo/streamlit-example/master/Seismic%20Anchorage.csv'
df_asce_arch = pd.read_csv(file, usecols =[0,1,2,3])
df_asce_mep = pd.read_csv(file, usecols =[5,6,7,8])
df_asce_mep = df_asce_mep[df_asce_mep['Mechanical and Electrical Components'].notna()]

#now create a drop down based on which component, etc.
equp_sel = st.selectbox('Equipment Type', equip_sel)
