# -*- coding: utf-8 -*-
"""
Created on Sun Nov 17 16:51:08 2024

@author: nthar 
Data : from Steinig et al., 2024
"""

import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature
from netCDF4 import Dataset
import numpy as np
from cmcrameri import cm  # Crameri et al., 2020 (e.g., bibliography)
from scipy.interpolate import griddata

nc = Dataset('tos_IPSLCM5A2_deepmip-eocene-p1-x3_v1.0.time_series.nc', 'r')
print("Variables disponibles dans le fichier NetCDF :")
for variable in nc.variables:
    print(variable)
    
nc2 = Dataset('orog_IPSLCM5A2_deepmip-eocene-p1-x3_v1.0.nc', 'r')
print("\n", "Variables disponibles dans le fichier NetCDF :")
for variable in nc.variables:
    print(variable)

#%%
test_tos  = nc.variables['tos']
test_lat  = nc.variables['nav_lat']
test_lon  = nc.variables['nav_lon']
test_time = nc.variables['time_counter']
print("tos=",test_tos, "\n")
print("lat=",test_lat, "\n")
print("lon=",test_lon, "\n")
print("deptht=",test_time, "\n")

#%%
# Load data
nc = Dataset('tos_IPSLCM5A2_deepmip-eocene-p1-x3_v1.0.time_series.nc', 'r')
nc2 = Dataset('orog_IPSLCM5A2_deepmip-eocene-p1-x3_v1.0.nc', 'r')

# Extract variables
tos = nc.variables['tos'][:]            # Sea surface temperature
lat = nc.variables['nav_lat'][:]        # Latitude
lon = nc.variables['nav_lon'][:]        # Longitude
time = nc.variables['time_counter'][:]  # Time
orog = nc2.variables['orog'][:]         # Altitude
lat_orog = nc2.variables['lat'][:]      # OROG Latitude
lon_orog = nc2.variables['lon'][:]      # OROG Longitude

# Create a regular grid
lon_reg, lat_reg = np.meshgrid(
    np.linspace(-180, 180, 360),  # 360 points in longitude
    np.linspace(-90, 90, 180))    # 180 points in latitude

# Remap data with scipy.interpolate.griddata
tos_remapped = griddata(
    (lon.flatten(), lat.flatten()),  # Original points
    tos[0, :, :].flatten(),          # Corresponding values
    (lon_reg, lat_reg),              # Target grid
    method='linear')                 # Interpolation method: 'linear', 'nearest', or 'cubic'

# Replace values greater than 10^5 with NaN
tos_remapped = np.where(tos_remapped > 1e5, np.nan, tos_remapped)

lon_orog, lat_orog = np.meshgrid(lon_orog, lat_orog)
# Remap the orog variable with scipy.interpolate.griddata
orog_remapped = griddata(
    (lon_orog.flatten(), lat_orog.flatten()),  # Original points
    orog.flatten(),                            # Corresponding values (in 1D)
    (lon_reg, lat_reg),                        # Target grid
    method='linear')                           # Interpolation method: 'linear', 'nearest', or 'cubic'

orog_remapped = np.where(orog_remapped == 0, np.nan, orog_remapped)

#%% Temperature Map
# Calculate levels for the color gradient
vmin = 12  # Minimum value (ignoring NaNs)
vmax = 40  # Maximum value (ignoring NaNs)
levels = np.arange(vmin, vmax + 1, 1)  # Level range with a step of 1

# Visualization
fig = plt.figure(figsize=(13.5, 6.25))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.Robinson(central_longitude=0))

# Plot the interpolated data (temperatures) with alpha for transparency
im_tos = ax.contourf(lon_reg, lat_reg, tos_remapped, levels=levels, transform=ccrs.PlateCarree(), 
                     cmap=cm.lipari, extend='both', alpha=1)

# Add line for temperatures levels
contour_levels = [15, 20, 25, 30, 35]
contours = ax.contour(lon_reg, lat_reg, tos_remapped, levels=contour_levels, 
                      colors='white', linewidths=0.8, transform=ccrs.PlateCarree())

# Add label for temperatures level
ax.clabel(contours, inline=True, fmt='%d°C', fontsize=8, colors='white')

# Altitude Map
# Calculate levels for altitude
vmin2 = 0
vmax2 = 2400
level_orog = np.arange(vmin, vmax + 1, 20)
levels_orog = [0, 5, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 200, 300,
               400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500,
               1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300, 2400]  # Level range for altitude

# Plot the interpolated data (altitude)
im_orog = ax.contourf(lon_reg, lat_reg, orog_remapped, levels=levels_orog, 
                      transform=ccrs.PlateCarree(), cmap='terrain', extend='both', alpha=1)  # alpha = 0.6 => 60% transparency

# Add line for temperatures levels
contour_levels2 = [1000, 1500, 2000, 2200, 2400]
contours2 = ax.contour(lon_reg, lat_reg, orog_remapped, levels=contour_levels2, 
                      colors='black', linewidths=0.8, transform=ccrs.PlateCarree())

# Add label for temperatures level
ax.clabel(contours2, inline=True, fmt='%dm', fontsize=8, colors='black')

# Colorbar for temperatures
cbar_tos = plt.colorbar(im_tos, ax=ax, orientation='horizontal', shrink=0.8, fraction=0.06, pad=0.1)
cbar_tos.set_label("Sea surface temperature at 45 Ma (3X) (°C)")

# Colorbar for altitude
cbar_orog = plt.colorbar(im_orog, ax=ax, orientation='vertical', shrink=0.8, fraction=0.06, pad=0.05)
cbar_orog.set_label("Topography at 45 Ma (m)")

# Add gridlines
plt.title("Data 'tos' and 'orog' from IPSLCM5A2 Model published by Steinig et al., 2024", fontsize=9)
fig.suptitle("Representation of topography and sea surface temperatures at 45 Ma", fontsize=13)
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linestyle=':')
gl.xlabel_style = {'size': 10, 'color': 'black'}
gl.ylabel_style = {'size': 10, 'color': 'black'}

#plt.savefig('tos_orog_IPSLCM5A2_3X_steinigetal2024.png', dpi=300, bbox_inches='tight') # Save the map










