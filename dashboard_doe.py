import streamlit as st
import plotly.express as px

import plotly.graph_objects as go
from plotly.graph_objs import *
import plotly
import numpy as np
import pandas as pd

from DoE import *

#---------------------------------------------------------------------------------------------------

st.set_page_config(layout="wide")

st.markdown("""
<style>
.reportview-container .main footer, .reportview-container .main footer a {
    color: #0c0080;
}
</style>
    """, unsafe_allow_html=True)

st.title("Design of Experiments - DoE")

st.markdown("** **")


#---------------------------------------------------------------------------------------------------

# 2 dropdowns for no of samples and method
# 3D plot for showing the experiment points in parameter space.

c1,c2=st.columns([1,2])

experiment=pd.DataFrame(columns=["roof_length","front_length","back_length"])

doe=definitions()
#st.write(doe)

method=c1.selectbox("Select the experiment design method",options=["BoxBehnkenGenerator","FullFactorialGenerator","GeneralizedSubsetGenerator","LatinHypercubeGenerator","PlackettBurmanGenerator","UniformGenerator"],key="select_method")
if doe[method]["num_samples"]:
    num_samples=c1.text_input("Select the overall number of samples for your experiment",key="textbox_num_samples")
else:
    num_samples=0
if doe[method]["samples"]==True:
    samples=c1.text_input("Select the overall number of samples for your experiment",key="textbox_samples")    
else:
    samples=0
if doe[method]["levels"]==True:
    levels=c1.text_input("Select the number of evenly spaced levels per factor",key="textbox_levels")
else:
    levels=0
if doe[method]["center"]==True:
    center=c1.text_input("Select the number of center points to include",key="textbox_levels")
else:
    center=0
reduction="2"

if c1.button("Create Design of Experiments"):
    values=create_doe(method,int(levels),int(samples),int(num_samples),int(reduction),int(center))

    experiment=pd.DataFrame(data=values,columns=["roof_length","front_length","back_length"])

#layout = Layout(
#    Scene(aspectmode='cube')
#)

#fig=px.scatter_3d(experiment,x="roof_length",y="front_length",z="back_length")
fig = go.Figure(data=[go.Scatter3d(x=experiment["roof_length"],y=experiment["front_length"],z=experiment["back_length"],
                                   mode='markers')])

#fig.update_layout(aspectmode='cube')
fig.update_scenes(aspectmode='cube',xaxis_title="roof_length",yaxis_title="front_length",zaxis_title="back_length")

c2.plotly_chart(fig,use_container_width=True)
#c2.write(experiment)


footer="""<style>
a:link , a:visited{
color: blue;
background-color: transparent;
text-decoration: underline;
}

a:hover,  a:active {
color: red;
background-color: transparent;
text-decoration: underline;
}

.footer {
position: fixed;
left: 0;
bottom: 0;
width: 100%;
background-color: white;
color: black;
text-align: center;
}
</style>
<div class="footer">
<p>Developed with ❤ by <a style='display: block; text-align: center;' href="https://www.cfdsolutions.net/" target="_blank">Astrid Walle CFDsolutions</a></p>
</div>
"""
st.markdown(footer,unsafe_allow_html=True)
