"""

    Utility functions for testing grid refinement in WRF simulations.
    From : https://www2.mmm.ucar.edu/wrf/users/wrf_users_guide/build/html/fire.html#fire-state-variables
    Look up the function:
    grid%znw(k) = (exp(-(k-1)/float(kde-1)/z_scale) &  - exp(-1./z_scale))/(1.-exp(-1./z_scale)
    
    This is a pythonic way to look at your grid refinement. 
    Produce two plots: a full look at the vertical grid points
    and a zoomed at the lowest ~1000m
    
    lbuchart@eoas.ubc.ca
    November 23, 2025

"""
import numpy as np 
import matplotlib.pyplot as plt

##### User Inputs ##### Similar to wrf variable definitions
z_grd_scale = 0.35     # scale height for vertical grid stretching
e_vert = 81  # number of vertical levels

savepath = "./FIGURES/"

##### End User Inputs #####

grid_znw = np.zeros(e_vert)
for k in range(e_vert):
    grid_znw[k] = (np.exp(-(k)/float(e_vert-1)/z_grd_scale) - np.exp(-1./z_grd_scale)) / (1.-np.exp(-1./z_grd_scale))
    
    
# plot full grid
plt.figure(figsize=(10,10))
plt.plot(np.arange(0, e_vert, 1), grid_znw, 'ro')
# add grid lines
for i in range(0, e_vert, 10):
    plt.plot([i,i], [0, grid_znw[i]], 'k-', linewidth=0.5)

plt.xlabel("Level")
plt.ylabel("Height [m]")
plt.title("Full Vertical Grid")
plt.savefig(f"{savepath}full_vert_grid")