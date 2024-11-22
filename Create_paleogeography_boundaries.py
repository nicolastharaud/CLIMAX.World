# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 18:28:56 2024

@author: nthar
Data from Steinig et al., 2024.
Color Map from Crameri et al., 2020
"""

#%% Import packages

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from netCDF4 import Dataset
import numpy as np
from cmcrameri import cm  # Crameri et al., 2020 (e.g., bibliography)
from scipy.interpolate import griddata

#%% Load data

nc_tas = Dataset('tas_CESM1.2-CAM5_deepmip-eocene-p1-x1_v1.0.mean.nc', 'r')
print("Variables disponibles dans le fichier NetCDF :")
for variable in nc_tas.variables:
    print(variable)
    
nc_orog = Dataset('orog_CESM1.2-CAM5_deepmip-eocene-p1-x1_v1.0.nc', 'r')
print("\n", "Variables disponibles dans le fichier NetCDF :")
for variable in nc_orog.variables:
    print(variable)
    
#%% Extract variables

tas      = nc_tas.variables['tas'][:]       # Near air surface temperature
lat_tas  = nc_tas.variables['lat'][:]       # TAS Latitude
lon_tas  = nc_tas.variables['lon'][:]       # TAS Longitude

orog     = nc_orog.variables['orog'][:]     # Altitude
lat_orog = nc_orog.variables['lat'][:]      # OROG Latitude
lon_orog = nc_orog.variables['lon'][:]      # OROG Longitude

### Conversion K => °C
tas = tas - 273.15

#%% To avoid a white line (without data) between longitude 357.5 and 360

### TAS
lon_tas  = np.insert(lon_tas, 144, 360)
new_col_tas = (tas[:, :, 143] + tas[:, :, 0]) / 2 
tas = np.concatenate((tas, new_col_tas[:, :, np.newaxis]), axis=2)

### OROG
lon_orog = np.insert(lon_orog, 144, 360)
new_col_orog = (orog[:, 143] + orog[:, 0]) / 2  
orog = np.hstack((orog, new_col_orog[:, np.newaxis]))


#%% Create a regular grid

### TAS
lon_tas, lat_tas = np.meshgrid(lon_tas, lat_tas)
       
### OROG
lon_orog, lat_orog = np.meshgrid(lon_orog, lat_orog)
orog = np.where(orog < 2, np.nan, orog)             # Replace <2 values by nan in orog


#%% Create Paleogeography boundaries for OROG

def create_paleogeography_boundaries(orog):
    """
    Create a paleogeography matrix from the orography data.
    Identifies land areas (where orog > 0) and marks the edges with specific values.
    
    Parameters:
        orog (ndarray): 2D array representing the orography (altitude).
    
    Returns:
        Y (ndarray): Processed 2D matrix with:
            - Internal land marked with 5,
            - Borders of land regions marked with 2,
            - Other areas remain unchanged.
    """
    # Step 1: Create binary mask for land (1) and water (0)
    Z = np.where(orog > 0, 1, 0)

    # Step 2: Create an empty matrix to mark the borders
    W = np.zeros_like(Z)

    # Step 3: Loop through the matrix to identify border cells
    rows, cols = Z.shape
    for i in range(1, rows - 1):                            # Avoid boundaries of the matrix
        for j in range(1, cols - 1):                        # Avoid boundaries of the matrix
            if Z[i, j] == 1:                                # Land cell
                                                            # Check the 8 neighbors for water (Z == 0)
                if (Z[i-1, j] == 0 or Z[i+1, j] == 0 or     # Vertical neighbors
                    Z[i, j-1] == 0 or Z[i, j+1] == 0 or     # Horizontal neighbors
                    Z[i-1, j-1] == 0 or Z[i-1, j+1] == 0 or # Diagonal neighbors
                    Z[i+1, j-1] == 0 or Z[i+1, j+1] == 0):  # Diagonal neighbors
                    W[i, j] = 2                             # Mark border cells with 2

    # Step 4: Merge W and Z into Y
    Y = np.where(W == 2, W, Z)                              # Prioritize borders (2) over land (1)

    # Step 5: Replace internal land cells (1) with 5
    Y = np.where(Y == 1, 5, Y)

    return Y

Y = create_paleogeography_boundaries(orog)

#%% Mapping

fig = plt.figure(figsize=(13.5, 6.25))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson(central_longitude=0))

### OROG
CS = ax.contour(lon_orog, lat_orog, Y, levels=[1.6], colors='k', alpha=1, linewidths=1, transform=ccrs.PlateCarree())

### TAS
vmin = -10  # np.nanmin(tas) Minimum value (ignoring NaNs)
vmax = 40   # np.nanmax(tas) Maximum value (ignoring NaNs)
levels = np.arange(vmin, vmax + 1, 1)
im_tas = ax.contourf(lon_tas, lat_tas, tas[0, :, :], transform=ccrs.PlateCarree(), 
                     levels=levels, cmap=cm.batlow, extend='both', alpha=1)

# Colorbar for temperatures
cbar_tas = plt.colorbar(im_tas, ax=ax, orientation='horizontal', shrink=0.8, fraction=0.06, pad=0.1)
cbar_tas.set_ticks(np.linspace(-10, 40, 11))
cbar_tas.set_label("Near air surface temperature at 55 Ma (1X) (°C)")

# Add line and label for temperatures levels
contour_levels = [-30, -20, -10, -5, 0, 10, 20, 30, 40, 50]
contours = ax.contour(lon_tas, lat_tas, tas[0, :, :], levels=contour_levels, 
                      colors='white', linewidths=1, transform=ccrs.PlateCarree())
ax.clabel(contours, inline=True, fmt='%d°C', fontsize=9, colors='white')

### Graphic label
plt.title("Data 'tas' and 'orog' from CESM1.2-CAM5 climate model published by Steinig et al., 2024", fontsize=9)
fig.suptitle("Representation of paleogeography and near air surface temperatures at 55 Ma for 1X pCO2", fontsize=13)
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linestyle=':', linewidth=0) # linewidth = 0 => Invisible grid lines
gl.xlabel_style = {'size': 10, 'color': 'black'}
gl.ylabel_style = {'size': 10, 'color': 'black'}

### Save the map
#plt.savefig('tas_CESM1.2-CAM5_1X.png', dpi=300, bbox_inches='tight')
