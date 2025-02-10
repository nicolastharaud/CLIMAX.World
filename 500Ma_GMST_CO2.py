# -*- coding: utf-8 -*-
"""
Created on Mon Feb 10 01:17:28 2025

@author: nthar
Data from Judd et al., 2024
"""

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
import numpy as np
import matplotlib.transforms as transforms
import matplotlib.patches as mpatches
import matplotlib.ticker as ticker

# Load data from an Excel file
datas = "PhanDA_GMSTandCO2_percentiles.xlsx"
data = pd.read_excel(datas)

# Extract relevant columns from the dataset
period = data['Period']
epoch = data['Epoch']
stage = data['Stage']
agemin = data['LowerAge']
agemax = data['UpperAge']
agemean = data['AverageAge']
gmst05 = data['GMST_05']
gmst16 = data['GMST_16']
gmst50 = data['GMST_50']
gmst84 = data['GMST_84']
gmst95 = data['GMST_95']
co205 = data['CO2_05']
co216 = data['CO2_16']
co250 = data['CO2_50']
co284 = data['CO2_84']
co295 = data['CO2_95']

# Create figure with two subplots (2 rows, 1 column)
fig, (ax2, ax1) = plt.subplots(2, 1, figsize=(25.25, 13.75))  
plt.rcParams["font.family"] = "Times New Roman"

# === CO2 Concentration Plot (ax2) ===
ax2.plot(agemean, co250, color="black", linestyle='-', linewidth=3, alpha=1, label='50')
ax2.fill_between(agemean, co216, co284, color="black", alpha=0.35, label='16 - 84')
ax2.fill_between(agemean, co205, co295, color="black", alpha=0.25, label='05 - 95')

# Configure X and Y-axis for CO2 (ax2)
ax2.set_xticks(np.arange(0, 550, 50))  
ax2.tick_params(axis='x', which='major', labelsize=25, length=7, width=2)  
ax2.xaxis.set_minor_locator(MultipleLocator(10))  
ax2.tick_params(axis='x', which='minor', length=5)  

ax2.set_ylabel("CO2 Concentration (ppm)", fontsize=25)
ax2.set_ylim(-850, 5000)

# Set Y-axis major and minor tick intervals
major_ticks = np.arange(0, 5001, 500)
ax2.yaxis.set_major_locator(ticker.FixedLocator(major_ticks))
minor_ticks = np.arange(0, 5001, 100)
ax2.yaxis.set_minor_locator(ticker.FixedLocator(minor_ticks))
ax2.tick_params(axis='y', which='major', labelsize=25, length=7, width=2)
ax2.tick_params(axis='y', which='minor', length=5)

# Hide negative labels on the Y-axis
ax2.set_yticklabels([str(label) if label >= 0 else '' for label in major_ticks])

# Reverse X-axis for both subplots
ax2.invert_xaxis()
ax1.invert_xaxis()

# === Global Mean Surface Temperature (GMST) Plot (ax1) ===
ax1.plot(agemean, gmst50, color="red", linestyle='-', linewidth=3, alpha=1, label='50')
ax1.fill_between(agemean, gmst16, gmst84, color="red", alpha=0.35, label='16 - 84')
ax1.fill_between(agemean, gmst05, gmst95, color="red", alpha=0.25, label='05 - 95')

# Configure axis labels for GMST (ax1)
ax1.set_xlabel("Age (Ma)", fontsize=25)  
ax1.set_ylabel("Global Mean Surface Temperature (°C)", fontsize=25)  

# Set ticks for X and Y axes
ax1.set_xticks(np.arange(0, 550, 50))  
ax1.tick_params(axis='x', which='major', labelsize=25, length=7, width=2)  
ax1.xaxis.set_minor_locator(MultipleLocator(10))  
ax1.tick_params(axis='x', which='minor', length=5)  

ax1.set_yticks(np.arange(0, 46, 5))  
ax1.tick_params(axis='y', which='major', labelsize=25, length=7, width=2)  
ax1.yaxis.set_minor_locator(MultipleLocator(1))  
ax1.tick_params(axis='y', which='minor', length=5)  

# Add title, legends, and grid lines
fig.suptitle("Variations in CO2 and Global Mean Surface Temperatures Over the Last 485 Million Years", fontsize=28)

legend1 = ax1.legend(loc='upper right', prop={'size': 18, 'style': 'italic'}, title="Percentiles GMST", title_fontsize=18)
legend2 = ax2.legend(loc='upper right', prop={'size': 18, 'style': 'italic'}, title="Percentiles CO2", title_fontsize=18)

# Make legend titles bold
legend1.get_title().set_fontweight('bold')
legend2.get_title().set_fontweight('bold')

# Add grid lines
ax1.grid(True, which='major', axis='both', linestyle='--', color='gray', alpha=0.5, zorder=1)
ax2.grid(True, which='major', axis='both', linestyle='--', color='gray', alpha=0.5, zorder=1)

# Create transformation objects for positioning rectangles
trans1 = transforms.blended_transform_factory(ax1.transData, ax1.transAxes)
trans2 = transforms.blended_transform_factory(ax2.transData, ax2.transAxes)

# Function to add colored rectangles and labels for geological time periods
def add_time_rectangles(ax, trans):
    rect_params = [
        (0, 2.58, 'lightyellow', "Q"),
        (2.58, 20.46, 'yellow', "Neogene"),
        (23.04, 42.96, 'coral', "Paleogene"),
        (66, 77.1, 'limegreen', "Cretaceous"),
        (143.1, 58.3, 'dodgerblue', "Jurassic"),
        (201.4, 50.5, 'purple', "Triassic"),
        (251.9, 47, 'orangered', "Permian"),
        (298.9, 59.96, 'turquoise', "Carboniferous"),
        (358.86, 60.76, 'peru', "Devonian"),
        (419.62, 23.48, 'aquamarine', "Silurian"),
        (443.1, 43.75, 'mediumseagreen', "Ordovician")]
    
    for x, width, color, name in rect_params:
        rect = mpatches.Rectangle((x, 0), width=width, height=0.09, transform=trans, color=color, alpha=1, zorder=2)
        ax.add_patch(rect)
        x_center = x + width / 2  
        ax.text(x_center, 0.04, name, transform=trans, ha='center', va='center', 
                fontsize=19, fontweight='bold', color='black')

# Function to add ice period indicators
def ice_rects(ax, trans, legend_patches):
    rectice = [(0, 34, 'aqua'), (260, 110, 'aqua'), (430, 30, 'aqua')]
    
    for x, width, color in rectice:
        rect = mpatches.Rectangle((x, 0.093), width=width, height=0.05, transform=trans, color=color, alpha=1, zorder=3)
        ax.add_patch(rect)

    # Add legend for ice periods only once
    if not legend_patches:
        legend_patches.append(mpatches.Patch(color="aqua", alpha=1, label="Ice Periods"))

legend_patches = []

# Apply functions to both subplots
ice_rects(ax1, trans1, legend_patches)
ice_rects(ax2, trans2, legend_patches)
fig.legend(handles=legend_patches, bbox_to_anchor=(0.145, 0.487), prop={'size': 18, 'weight': 'bold'}, frameon=True)

add_time_rectangles(ax1, trans1)
add_time_rectangles(ax2, trans2)

# Adjust layout to prevent overlap
plt.tight_layout()

# Save the figure 
#plt.savefig('500Ma_GMST_CO2.png', dpi=300, bbox_inches='tight')
