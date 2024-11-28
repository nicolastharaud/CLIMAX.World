# -*- coding: utf-8 -*-
"""
Created on Tue Nov 26 18:50:00 2024

@author: nthar
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation
from netCDF4 import Dataset

# Load data from the NetCDF file
nc_orog = Dataset('orog_CESM1.2-CAM5_deepmip-eocene-p1-PI_v1.0.nc', 'r')
orog = nc_orog.variables['orog'][:]  # Extract the elevation data

# Create grids for latitude and longitude
nlat, nlon = orog.shape           # Dimensions of the elevation data
lat = np.linspace(-90, 90, nlat)  # Latitude grid
lon = np.linspace(0, 360, nlon)   # Longitude grid

# Convert latitude and longitude to radians
lat_rad = np.radians(lat)
lon_rad = np.radians(lon)

# Create 2D grids for latitude and longitude
lat_grid, lon_grid = np.meshgrid(lat_rad, lon_rad, indexing='ij')

# Convert to Cartesian coordinates
x = np.cos(lat_grid) * np.cos(lon_grid)
y = np.cos(lat_grid) * np.sin(lon_grid)
z = np.sin(lat_grid)

#%% Figure creation
fig = plt.figure(figsize=(13.5, 6.25))
ax = fig.add_subplot(111, projection='3d')

# Add a title to the figure
fig.suptitle('3D Earth', fontsize=16, fontfamily='Times New Roman')

# Initial plot of the sphere
surf = ax.plot_surface(
    x, y, z,
    rstride=1, cstride=1,
    facecolors=plt.cm.terrain(orog / orog.max()),  # Colors mapped to elevation
    linewidth=0, antialiased=False, shade=False)

# Initial adjustments
ax.set_box_aspect([1, 1, 1])  # Keep the sphere proportional
ax.set_axis_off()             # Hide the axes

# Animation function
def update(frame):
    # Rotation: Change the viewing angle
    ax.view_init(elev=-20, azim=frame)

# Create the animation
anim = FuncAnimation(fig, update, frames=np.arange(0, 360, 2), interval=1000)

# Save the animation as a video
anim.save('3D_Earth.mp4', fps=60, writer='ffmpeg')








