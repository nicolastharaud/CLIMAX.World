# -*- coding: utf-8 -*-
"""
Created on Mon Nov 11 11:41:37 2024

@author: nthar
Data : Hansen et al., 2013; Westerhold et al., 2020
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Two ways to import data; one manually and one with pandas
time = []
d13C = []
d18O = []

with open('Table_Westerhold.txt', 'r') as file:
        
    for line in file:
        if not line.startswith('#'):
            elements = line.split('\t')
            try:
                time.append(float(elements[0]))
                d13C.append(float(elements[3]))
                d18O.append(float(elements[6]))
            except (IndexError, ValueError):
                pass

datas = "Table_Hansen.xlsx"
data  = pd.read_excel(datas)

time_hansen = data['Time_H']
d18O_hansen = data['delta_18O_H']

#%%
plt.figure(figsize=(13.5, 6.25))
plt.rcParams["font.family"] = "Times New Roman"

# Rolling average
d18O_smooth = pd.Series(d18O).rolling(window=100).mean()
d13C_smooth = pd.Series(d13C).rolling(window=100).mean()
d18O_smooth = pd.Series(d18O).rolling(window=100).mean()
d18O_hansen_smooth = pd.Series(d18O_hansen).rolling(window=100).mean()

plt.plot(time[8750:16900], d18O[8750:16900], c='b', linewidth=0.75, alpha=0.25)
plt.plot(time[8750:16900], d13C[8750:16900], c='r', linewidth=0.75, alpha=0.25)
plt.plot(time[8750:16900], d18O_smooth[8750:16900], c='b', linewidth=1.25, label='δ18O [Westerhold et al., 2020]')
plt.plot(time[8750:16900], d13C_smooth[8750:16900], c='r', linewidth=1.25, label='δ13C [Westerhold et al., 2020]')
plt.plot(time_hansen[8072:16191], d18O_hansen[8072:16191], c = 'green', alpha=0.25, linewidth=0.75)
plt.plot(time_hansen[8072:16191], d18O_hansen_smooth[8072:16191], c = 'green', linestyle='--', linewidth=1.25, label="δ18O [Hansen et al., 2013]")

plt.gca().invert_xaxis() # Invert the x-axis to have present time on the right

# Add a transparent rectangle behind the graph for different geological periods
plt.axvspan(time[11515],  time[16900], color='chocolate', alpha=1,   ymin = 0, ymax = 0.05)    # Oligocene
plt.axvspan(time[8750],   time[11514], color='yellow',    alpha=1,   ymin = 0, ymax = 0.05)    # Miocene
plt.axvspan(time[13910],  time[16900], color='chocolate', alpha=0.65, ymin = 0.05, ymax = 0.1) # Rupelian 
plt.axvspan(time[11515],  time[13909], color='chocolate', alpha=0.5, ymin = 0.05, ymax = 0.1)  # Chattian
plt.axvspan(time[10220],  time[11514], color='yellow',    alpha=0.65, ymin = 0.05, ymax = 0.1) # Aquitanian 
plt.axvspan(time[8750],   time[10219], color='yellow',    alpha=0.5, ymin = 0.05, ymax = 0.1)  # Burdigalian
plt.axvspan(time[13150],  time[14000], color='lightskyblue', alpha=0.5, ymin = 0.11, ymax = 1) # MOGI
 
plt.text(time[14100], -0.900, 'Oligocene',    ha='center', va='center', fontsize=15, color='black') 
plt.text(time[10020], -0.900, 'Miocene',      ha='center', va='center', fontsize=15, color='black') 
plt.text(time[15405], -0.670, 'Rupelian',     ha='center', va='center', fontsize=15, color='black') 
plt.text(time[12712], -0.670, 'Chattian',     ha='center', va='center', fontsize=15, color='black') 
plt.text(time[10867], -0.670, 'Aquitanian',   ha='center', va='center', fontsize=15, color='black') 
plt.text(time[9485],  -0.670, 'Burdigalian',  ha='center', va='center', fontsize=15, color='black')
plt.text(time[13575],  3.200, 'MOGI',         ha='center', va='center', fontsize=15, color='black')

# Title and axis labels
plt.xlabel("Time (My)", fontsize=15)
plt.xticks(np.arange(17, 35, 1), fontsize=15)
plt.yticks(fontsize=15)
plt.ylabel("δ18O and δ13C (‰ PDB)", fontsize=15)
plt.ylim(-1, 3.5)
plt.title("Evolution of δ18O and δ13C (benthic foraminifera) over time", 
          fontsize=15)

# Annotations
plt.annotate('', xy=(1.025, 0.9), xytext=(1.025, 0.6), xycoords='axes fraction', 
             arrowprops=dict(facecolor='blue', arrowstyle='<|-', lw=1.5, edgecolor='blue'), fontsize=12, ha='center')
plt.annotate('', xy=(1.025, 0.4), xytext=(1.025, 0.05), xycoords='axes fraction', 
             arrowprops=dict(facecolor='red', arrowstyle='-|>', lw=1.5, edgecolor='red'), fontsize=12, ha='center')
plt.text(16.6, 1.55, 'Warming',   fontsize=15, color='blue') 
plt.text(16.6, 1.0, 'Burial ', fontsize=15, color='red') 
plt.text(16.6, 0.825, 'of organic C', fontsize=15, color='red') 

# Custom background grid
y_lines = np.arange(-0.5, 3.5, 0.5)
x_lines = np.arange(17, 35, 1)
ymin = (-0.5 - plt.ylim()[0]) / (plt.ylim()[1] - plt.ylim()[0])
ymax = (3.0  - plt.ylim()[0]) / (plt.ylim()[1] - plt.ylim()[0])
xmin = (34   - plt.xlim()[0]) / (plt.xlim()[1] - plt.xlim()[0])
xmax = (17   - plt.xlim()[0]) / (plt.xlim()[1] - plt.xlim()[0])
for x in x_lines:
    plt.axvline(x, color='gray', linestyle='-', linewidth=0.5, ymin=ymin, ymax=ymax)
for y in y_lines:
    plt.axhline(y, color='gray', linestyle='-', linewidth=0.5, xmin=xmin, xmax=xmax)

# Legend
plt.legend(loc="upper left", prop={'size': 9})

#plt.savefig('d18O_d13C_comparison.png', dpi=300, bbox_inches='tight')


