# -*- coding: utf-8 -*-
"""
Created on Sat Apr 16 16:18:31 2022

@author: User
"""
import streamlit as st
import pandas as pd
import numpy as np
import rasterio as rio
from matplotlib import pyplot as plt
import os
st.title('Sanitation Scenario Explorer')

p_out = 'scn_data/opt_out.tif'
mask = 'scn_data/pop_mask3.tif'
p_a1_econ = 'scn_data/ecn_a1.tif'
p_a2_econ = 'scn_data/ecn_a2.tif'
p_a3_econ = 'scn_data/ecn_a3.tif'
p_a4_econ = 'scn_data/ecn_a4.tif'
p_a1_env = 'scn_data/env_a1.tif'
p_a2_env = 'scn_data/env_a2.tif'
p_a3_env = 'scn_data/env_a3.tif'
p_a4_env = 'scn_data/env_a4.tif'
p_a1_soc = 'scn_data/soc_a1.tif'
p_a2_soc = 'scn_data/soc_a2.tif'
p_a3_soc = 'scn_data/soc_a3.tif'
p_a4_soc = 'scn_data/soc_a4.tif'


 # Open as rasterio rasters to numpy arrays
a1_ecn = rio.open(p_a1_econ).read()
a2_ecn = rio.open(p_a2_econ).read()
a3_ecn = rio.open(p_a3_econ).read()
a4_ecn = rio.open(p_a4_econ).read()
a1_env = rio.open(p_a1_env).read()
a2_env = rio.open(p_a2_env).read()
a3_env = rio.open(p_a3_env).read()
a4_env = rio.open(p_a4_env).read()
a1_soc = rio.open(p_a1_soc).read()
a2_soc = rio.open(p_a2_soc).read()
a3_soc = rio.open(p_a3_soc).read()
a4_soc = rio.open(p_a4_soc).read()

mask = rio.open(mask).read()
opt_out = rio.open(p_out)

# Sliders
k1 = st.slider('Economic', 0, 10, 5)
k2 = st.slider('Environmental', 0, 10, 5)
k3 = st.slider('Social', 0, 10, 5)

# Plotting a scenario
from matplotlib.colors import ListedColormap
import matplotlib.patches as mpatches
cmap = ListedColormap(["white","darkorange", "gold", "lawngreen", "lightseagreen",'gainsboro'])
bounds = [-0.5,0.5,1.5,2.5,3.5,4.5,5.5]
ticks = [0,1,2,3,4,5]
alt_colors = {
    'Alt 1: Centralized Sewerage' : 1,
    'Alt 2: Simplified Sewerage' : 2,
    'Alt 3: On Site with FSM' : 3,
    'Alt 4: Improved Onsite' : 4,
    'Unpopulated Areas': 5,
    }
patches = [mpatches.Patch(color=cmap(v), label=k) for k,v in alt_colors.items()]

a1 = k1*a1_ecn + k2*a1_env + k3*a1_soc
a2 = k1*a2_ecn + k2*a2_env + k3*a2_soc
a3 = k1*a3_ecn + k2*a3_env + k3*a3_soc
a4 = k1*a4_ecn + k2*a4_env + k3*a4_soc

optim = np.where((a1>a2) & (a1>a3) & (a1>a4), 1,0)
optim = np.where((a2>a1) & (a2>a3) & (a2>a4), 2,optim)
optim = np.where((a3>a1) & (a3>a2) & (a3>a4), 3,optim)
optim = np.where((a4>a1) & (a4>a3) & (a4>a1), 4,optim)
optim = np.where((mask==0), 5,optim)

fig, ax = plt.subplots(figsize=(12,12))
ax.imshow(optim[0], cmap=cmap, interpolation='nearest')
ax.set_title("Optimum distribution of sanitation slternatives")
ax.legend(handles=patches)
st.pyplot(fig)

#optimdf = pd.DataFrame(optim[0])
st.markdown('### Histogram of sanitation alternatives')
hist = np.histogram(optim[0], bins=[1,2,3,4,4.5])
st.bar_chart(hist[0])

#median filter
from scipy import ndimage, misc
filt = ndimage.median_filter(optim, size=12)
fig2, ax2 = plt.subplots(figsize=(12,12))
ax2.imshow(filt[0], cmap=cmap, interpolation='nearest')
ax2.set_title("Optimum distribution of sanitation slternatives")
ax2.legend(handles=patches)
st.pyplot(fig2)

# Sidebar explainer of the app
st.sidebar.text('')
st.sidebar.text('')
st.sidebar.markdown("**About**")
st.sidebar.text('')
st.sidebar.markdown('This software is a visual explorer of the results of a sanitation planning study that developed data-driven and spatial analytic methods for optimizing a sanitation portfolio consisting of both centralized and decentralized technologies')
st.sidebar.text('')
st.sidebar.markdown('**Sanitation Alternatives** <br />1. Centralized Sewerage <br /> 2. Simplified Sewerage <br /> 3. On-site Sanitation with Faecal Sludge Treatment <br /> 4. Improved On-site Sanitation ', unsafe_allow_html=True)

st.sidebar.markdown("**Sanitation system evaluation**")
st.sidebar.markdown('Sanitation systems are evaluted based on the ***Economic***, ***Environmental*** and ***Social*** appropriateness of the alternatives estimated based on the methodology described **here**.')

st.sidebar.markdown("**How to use:**")
st.sidebar.markdown('The sliders control the weightages given for the three components of the score. Adjust the sliders to generate optimized sanitation plans for different scenarios.')


#plt.bar(optim.flatten(), bins=[1,2,3,4],)
#plt.show()
        
#plt.imshow(optim[0], cmap=cmap, interpolation='nearest')
#plt.title("Optimized Sanitation Scenarios")
#plt.colorbar(boundaries=bounds, ticks=ticks, label = 'Alternative')
#plt.show()


