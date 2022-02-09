from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import numpy as np

"""

In the meantime, below is an example of what you can do with just a few lines of code:
"""
sub_title = st.text_input("Name of Equipment")
st.title(sub_title + " Anchorage Calculation")

#set up df for subsections of equipment
equip = ['Architectural', 'Mechanical and Electrical']
equip_sel = pd.DataFrame(equip)
# df for equipment types
file = 'https://raw.githubusercontent.com/juanrossxo/streamlit-example/master/Seismic%20Anchorage.csv'
df_asce_arch = pd.read_csv(file, usecols =[0,1,2,3])
#df_asce_arch.set_index('Architectural Components')
df_asce_mep = pd.read_csv(file, usecols =[5,6,7,8])
df_asce_mep = df_asce_mep[df_asce_mep['Mechanical and Electrical Components'].notna()]
#df_asce_mep.set_index('Mechanical and Electrical Components')

#now create a drop down based on which component, etc.
select_equip = st.selectbox('Equipment Type', equip_sel, disabled=True)
#if statement for types of equipment
if select_equip == 'Architectural':
  select = st.selectbox('Equipment Subtype (ASCE 7-16, Table 13.5-1)', df_asce_arch, disabled=True)
  select_df = df_asce_arch.loc[df_asce_arch['Architectural Components'] == select]
else:
  select_equip == 'Mechanical and Electrical'
  select = st.selectbox('Equipment Subtype (ASCE 7-16, Table 13.6-1)', df_asce_mep, disabled=True)
  select_df = df_asce_mep.loc[df_asce_mep['Mechanical and Electrical Components'] == select]
try:
  ap = select_df['Ap']
  ap_print = st.latex('A_p')
except:
  ap = select_df['Ap.1']
select_df
#not quite done here.. how to display values nicely in latek with values inserted??

#checkbox for anchorage to concrete
overstrength_true = st.checkbox('Anchorage to Concrete or Masonry? (Overstrength \u03A90)')

