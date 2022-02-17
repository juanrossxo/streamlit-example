from handcalcs.decorator import handcalc
from handcalcs import handcalc
import math
from math import sqrt
import pandas as pd
import streamlit as st
import numpy as np

sub_title = st.text_input("Name of Equipment")
st.title(sub_title + " Anchorage Calculation")

#Typ. Parameters to Input
with st.expander('Seismic and Equipment Parameters',expanded=True):
  Sds = st.number_input("Sds Value", format='%g')
  Ip = [1.0,1.5]
  Ip1 = pd.DataFrame(Ip)
  Ip = st.selectbox('Importance Factor, Ip (ASCE7-16 13.1.3)', Ip1)
  W = st.number_input("Weight of the Equipment, Wp (kips)", format='%g')
  z = st.number_input("Elevation of the Equipment, z (ft.)", format='%g')
  h = st.number_input("Height of Building, h (ft.)", format='%g')
  length = st.number_input("Length of Equipment (long side), L (ft.)", format='%g')
  width = st.number_input("Width of Equipment (short side), W (ft.)", format='%g')
  height = st.number_input("Height of Equipment, H (ft.)", format='%g')
  #COG
  COG = 0.5*height
  COG_other = st.checkbox('Check to input other COG height',help='Default C.O.G. of unit used is 50% ht.')
  st.caption('Default C.O.G. of unit used is 50% ht.')
  if COG_other == True:
    COG = st.number_input("C.O.G. ht. (ft)", format='%g')
  #anchor points inset?
  ap_inset = st.checkbox('Are the anchor points offset inside or outside of the unit?')
  ap_off = 0
  if ap_inset == True:
    ap_off = st.number_input("Enter Offset: + for outside of unit, - for inset, (in.)", format='%g')
    #convert to feet
    ap_off = ap_off/12
  
#set up df for subsections of equipment
equip = ['Architectural', 'Mechanical and Electrical']
equip_sel = pd.DataFrame(equip)
# df for equipment types
file = 'https://raw.githubusercontent.com/juanrossxo/streamlit-example/master/Seismic%20Anchorage.csv'
df_asce_arch = pd.read_csv(file, usecols =[0,1,2,3])
#df_asce_arch.set_index('Architectural Components')
df_asce_mep = pd.read_csv(file, usecols =[5,6,7,8])
df_asce_mep = df_asce_mep[df_asce_mep['Mechanical and Electrical Components'].notna()]

st.sidebar.write('test')

#now create a drop down based on which component, etc.
if W > 100:
  wq = st.checkbox('Are you sure that your units are correct? *KIPS*')
  b = True
  if wq==True:
    b = False
else:
  b = False
select_equip = st.selectbox('Equipment Type', equip_sel, disabled=b)
#if statement for types of equipment
if select_equip == 'Architectural':
  select = st.selectbox('Equipment Subtype (ASCE 7-16, Table 13.5-1)', df_asce_arch, disabled=b)
  select_df = df_asce_arch.loc[df_asce_arch['Architectural Components'] == select]
  ap = select_df['Ap'].values[0]
  rp = select_df['Rp'].values[0]
  o0 = select_df['Omega-Not'].values[0]
else:
  select = st.selectbox('Equipment Subtype (ASCE 7-16, Table 13.6-1)', df_asce_mep, disabled=b)
  select_df = df_asce_mep.loc[df_asce_mep['Mechanical and Electrical Components'] == select]
  ap = select_df['Ap.1'].values[0]
  rp = select_df['Rp.1'].values[0]
  o0 = select_df['Omega-Not.1'].values[0]
#not quite done here.. how to display values nicely in latek with values inserted??
@handcalc()
def my_calc1():
  A_p = ap
  R_p = rp
latex_code, vals_dict = my_calc1()
st.latex(latex_code)
#checkbox for anchorage to concrete
overstrength_true = st.checkbox('Anchorage to Concrete or Masonry? (Overstrength \u03A90)')
if overstrength_true:
  @handcalc()
  def my_calc2():
    Omega_0 = o0
  latex_code1, vals_dict = my_calc2()
  st.latex(latex_code1)

if rp==0 or h==0 or Ip==0:
  test = False
  st.error('Please Input All Parameters')

#Fp calcs
with st.expander('Fp Calculations',expanded=True):
  @handcalc()
  def Fp1_calc():
    F_p_1 = (0.4*ap*Sds*W)/(rp/Ip) * (1+2*(z/h)) #Kips
  latex_code2, vals_dict = Fp1_calc()
  st.latex(latex_code2)
  
  st.write('but not less than:')
  @handcalc(override='params', precision=2)
  def Fp2_calc():
    F_p_2 = 0.3*Sds*Ip*W #Kips
  latex_code3, vals_dict = Fp2_calc()
  st.latex(latex_code3)
  
  st.write('but also not required to be taken greater than:')
  @handcalc(override='params', precision=2)
  def Fp3_calc():
    F_p_3 = 1.6*Sds*Ip*W #Kips
  latex_code4, vals_dict= Fp3_calc()
  st.latex(latex_code4)

  st.write('Therefore, Fp is:')
  F_p_1 = (0.4*ap*Sds*W)/(rp/Ip)*(1+2*(z/h))
  F_p_2 = (0.3*Sds*Ip*W)
  F_p_3 = 1.6*Sds*Ip*W
  @handcalc()
  def Fp_final_calc():
    F_p_final = min(max(F_p_1, F_p_2), F_p_3) #Kips
  latex_code5, vals_dict = Fp_final_calc()
  st.latex(latex_code5)
