from collections import namedtuple
import altair as alt
import math
import pandas as pd
import streamlit as st
import numpy as np
import cv2

"""
# Welcome to Streamlit!

Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
forums](https://discuss.streamlit.io).

In the meantime, below is an example of what you can do with just a few lines of code:
"""


with st.echo(code_location='below'):
    total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
    num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

    Point = namedtuple('Point', 'x y')
    data = []

    points_per_turn = total_points / num_turns

    for curr_point_num in range(total_points):
        curr_turn, i = divmod(curr_point_num, points_per_turn)
        angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
        radius = curr_point_num / total_points
        x = radius * math.cos(angle)
        y = radius * math.sin(angle)
        data.append(Point(x, y))

    st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
        .mark_circle(color='#0068c9', opacity=0.5)
        .encode(x='x:Q', y='y:Q'))
    
    # Drawing Shapes
 
def ImageProcessing():
    image = np.zeros((512, 512, 3), np.uint8)
 
    cv2.line(image, (20,200), (200,20), (0,0,255),5)
    cv2.rectangle(image, (200,60), (20,200), (255,0,0), 3)
    cv2.circle(image, (80,80), 50, (0,255,0), 4)
 
    mytext = "Hello World"
 
    cv2.putText(image, mytext, (100,300), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255) )
 
    cv2.imshow('Black Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
 
ImageProcessing()
