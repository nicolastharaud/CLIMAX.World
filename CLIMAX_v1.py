# -*- coding: utf-8 -*-
"""
Created on Sun Oct 27 21:50:27 2024

@author: nthar
"""

### !!! CLimate Integrated Modeling and Analysis eXperiment !!! ###
### !!! CLIMAX World !!! ###

import numpy as np
import matplotlib.pyplot as plt
from cmcrameri import cm
import matplotlib.patches as mpatches

# Creating variables
lat   = np.linspace(0, 49, 50)
lon   = np.linspace(0, 49, 50)  
depth = np.linspace(0, 9, 10)
time  = np.linspace(0, 364, 365)
temperature = np.zeros((len(lon), len(lat), len(depth), len(time)))

lon, lat, depth, time

# Parameters for poles and the equator
temp_poles = -20            # Temperature at the poles
temp_equator = 20           # Maximum temperature at the equator
lat_center = len(lat) // 2  # Position of the equator in the `lat` vector

# Creating lat_effect: linear variation of temperature based on latitude
lat_effect = np.linspace(temp_poles, temp_equator, lat_center)  # Variation from the north pole to the equator
lat_effect = np.concatenate([lat_effect, np.linspace(temp_equator, temp_poles, len(lat) - lat_center)])
        
depth_effect = np.linspace(5, 0, len(depth))                             # Temperature decreases with depth
seasonvar    = 10 * np.sin(2 * np.pi * np.arange(len(time)) / len(time)) # Summer-winter variation

# Creating the temperature variable
for t in range(len(time)):
    temperature[:, :, :, t] = (15 + seasonvar[t] + lat_effect[:, None, None] + depth_effect[None, None, :])

#%% Temperature checks
# 1. Geographical cross-section
plt.imshow(temperature[:, :, 5, 12], cmap = cm.batlow) # origin='lower' to set 0 as the origin
plt.colorbar(label="Temperature (°C)")
plt.title("Temperature (°C) based on latitude and longitude")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

#%%
# 2. Temporal evolution: Temperature over time for a specific latitude and depth
plt.plot(range(len(time)), temperature[0, 10, 5, :], label="Latitude = 10, Depth = 5")
plt.xlabel("Day of the year")
plt.ylabel("Temperature (°C)")
plt.title("Temporal evolution of temperature for a specific latitude")
plt.legend()
plt.grid()

#%% CO2 forcing
# pCO2 concentrations in ppm
pCO2_levels = [560]
temperature_forcings = []

# Conversion into warming factors
def calculate_forcing(pCO2):
    baseline_pCO2 = 280  # Reference level (pre-industrial)
    # Approximation: doubling pCO₂ results in about a 3°C increase
    forcing_factor = 3 * np.log2(pCO2 / baseline_pCO2)
    return forcing_factor

# Add a forced temperature array
temperature_forced = np.zeros_like(temperature)

# Apply forcings for each pCO2 level
for pCO2 in pCO2_levels:
    forcing = calculate_forcing(pCO2)
    temperature_forced[:, :, :, :] = temperature + forcing  # Apply the forcing
    temperature_forcings.append(temperature_forced.copy())  # Save each scenario

# Visualization of forced temperature for a given day and depth
for i, (pCO2, temp_forced) in enumerate(zip(pCO2_levels, temperature_forcings)):
    plt.subplot(1, len(pCO2_levels), i + 1)
    plt.imshow(temp_forced[:, :, 5, 12], cmap="coolwarm", vmin=-20, vmax=40)
    plt.colorbar(label="Forced Temperature (°C)")
    plt.title(f"Forced temperature for pCO₂ = {pCO2} ppm")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")

plt.tight_layout()

#%% Improved geographical zones
# 0 = ocean, 1 = forest, 2 = desert, 3 = continent, 4 = polar ice cap, 5 = tropics
geo_map = np.zeros((len(lon), len(lat)))

# Polar ice caps
geo_map[:2, :]      = 4  # Arctic zone in the north
geo_map[45:, :]     = 4  # Antarctic in the south
geo_map[1:8, 15:21] = 4  # Greenland

# Oceans
#geo_map[:, :] = 0    # Default fill with oceans

# Continents
geo_map[5:20, 5:15]   = 3  # North America
geo_map[20:35, 12:18] = 3  # South America
geo_map[5:18, 25:45]  = 3  # Europe-Asia
geo_map[20:35, 20:30] = 3  # Africa
geo_map[30:40, 35:45] = 3  # Southeast Asia
geo_map[35:45, 38:45] = 3  # Australia

# Deserts
geo_map[15:20, 22:28] = 2  # Sahara
geo_map[32:36, 38:44] = 2  # Australian desert
geo_map[10:15, 30:35] = 2  # Gobi desert

# Forests
geo_map[25:30, 15:20] = 1  # Amazon
geo_map[22:28, 35:40] = 1  # Borneo and Sumatra
geo_map[25:35, 25:30] = 1  # Congo forest

# Tropics (approximation of the Tropics of Cancer and Capricorn)
# geo_map[10:15, :] = 5  # Tropic of Cancer
# geo_map[35:40, :] = 5  # Tropic of Capricorn

# Displaying improved geographical zones
plt.figure(figsize=(13.5, 6.25))
plt.imshow(geo_map, cmap="terrain", origin='lower')
plt.colorbar(label="Geographical zones: 0=Ocean, 1=Forest, 2=Desert, 3=Continent, 4=Ice cap")
plt.title("Simplified map of improved geographical zones")
plt.gca().invert_yaxis()  
plt.xlabel("Longitude")
plt.ylabel("Latitude")
plt.grid(linestyle=':')
#plt.savefig('Model_geography.png', dpi=300, bbox_inches='tight')

#%% Parameters to adjust temperature based on geographical zones

temperature2 = np.zeros((len(lon), len(lat), len(depth), len(time)))

for lat2 in range(len(lat)):
    for lon2 in range(len(lon)):
        zone = geo_map[lon2, lat2]
        if zone == 0:    # Ocean
            temperature2[lon2, lat2, :, :] *= 0.9   # More stable temperature (slight reduction in variations)
        elif zone == 1:  # Forest
            temperature2[lon2, lat2, :, :] *= 0.95  # Moderate temperature, less variation
        elif zone == 2:  # Desert
            temperature2[lon2, lat2, :, :] += 5     # Higher temperature to simulate desert conditions
        elif zone == 3:  # Continent
            temperature2[lon2, lat2, :, :] += 2     # Moderate temperature, less variation
        elif zone == 4:  # Polar ice cap
            temperature2[lon2, lat2, :, :] -= 15    # Colder temperature to simulate polar conditions

temperature_forced += temperature2

#%% Map of geographical zone contours and temperature
plt.figure(figsize=(13.5, 6.25))
plt.imshow(temperature_forced[:, :, 5, 12], cmap = 'coolwarm', alpha = 1, vmin=-20, vmax=40) # origin='lower' to set 0 as the origin
plt.colorbar(label="Temperature (°C)") # for cmap = cm.batlow (crameri)
plt.title("Simulation at 560 ppm CO2")
plt.xlabel("Longitude")
plt.ylabel("Latitude")

### Contours of the continents
## Plot the contours of each geographical zone individually
zone_labels = ["Ocean", "Forest", "Desert", "Continent", "Polar ice cap"]
zone_colors = ['blue', 'green', 'yellow', 'black', 'white']  # Colors for each zone
handles = []
# Draw contours for each geographical zone separately
for zone_value, color in zip(np.unique(geo_map), zone_colors):
    plt.contour(geo_map == zone_value, levels=[0.5], colors=color, linewidths=1.5, alpha=0.9)
# levels = [0.5] A fixed value to extract the zone boundary

# Add contour lines for specific temperatures
contour_levels = [-20, -10, 0, 10, 20, 30, 40]  # Temperature levels for contours
contour_plot = plt.contour(temperature_forced[:, :, 5, 12], levels=contour_levels, colors='white', linewidths=1)
# Add labels to the contour lines
plt.clabel(contour_plot, inline=True, fontsize=8, fmt="%1.0f°C")  # Label the temperature levels on contours

# Create a legend for the geographical zones
patches = [mpatches.Patch(color=color, label=label) for color, label in zip(zone_colors, zone_labels)]
plt.legend(handles=patches, loc='lower left', title="Geographical zones")

#plt.savefig('Simul_840ppm_3X.png', dpi=300, bbox_inches='tight')
