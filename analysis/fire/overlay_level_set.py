"""
    
    Plot the level set function outlining the fire perimeter
    Plot the function as a thick red lines overlayed with the topography
    
    Required: WRF output file directory (loop through many files)
    
    Output: plot for each time of model output
    
    lbuchart@eoas.ubc.ca
    December 1, 2025
    
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colormaps
import metpy.calc as mpcalc

from file_funcs import (setup_script, dist_from_ridge, 
                        dist_from_ridge_fire)

from wrf import (interpline, extract_times, get_cartopy,
                 getvar, to_np, latlon_coords, CoordPair)

## USER INPUTS ##
# option
#exps = ["TEST-REAL-BRUSH/", "TEST-REAL-FIRE/", "TEST-REAL-SPOTTING/", "TEST-FIRE-LARGE/", 
#        "TEST-REAL-VALLEY/", "TEST-SPOTTING-LOW/", "TEST-VALLEY-LARGE/"]

exp = "TEST-VALLEY-LARGE" + "/"  # name of the experiment you are plotting

start = (0, 80)
end = (-1, 80) 

## END USER INPUTS ##

path, save_path, relevant_files, wrfin = setup_script(exp=exp)

start_index = 2
# loop through files save every third level set plot
# starting with the third file
for ii in range(start_index, len(wrfin), 3):
    # import the file in a readable netcdf format
    ncfile = wrfin[ii]
    
    # extract the time in datetime format
    ct = extract_times(ncfile, timeidx=0)
    print(ct)
    
    # get the level set function variable
    ls = getvar(ncfile, "LFN", meta=True)
    
    # change first and last row and columns to nan to avoid contouring issues
    ls[:, 0:10] = np.nan
    ls[:, -10:] = np.nan
    ls[0:10, :] = np.nan
    ls[-10:-1, :] = np.nan
    
    print('Level set min/max: ', np.min(to_np(ls)), np.max(to_np(ls)))
    print(np.shape(ls))
    
    # get the terrain height
    ter = getvar(ncfile, "ter", meta=True)
    ter_heights = np.arange(150, 850, 50)
    ter_cross = interpline(ter, 
                           start_point=CoordPair(start[0], start[1]),
                           end_point=CoordPair(end[0], end[1]))
    ridge_dist = dist_from_ridge(ter_cross)
    ridge_dist_fire = dist_from_ridge_fire(ter_cross)
    print("Fire Ridge Distance: ", ridge_dist_fire)
       
    # Get the latitude and longitude points
    lats, lons = latlon_coords(ter)
    fxlats = getvar(ncfile, "FXLAT", meta=True)
    fxlons = getvar(ncfile, "FXLONG", meta=True)
    

    # Get the cartopy mapping object
    cart_proj = get_cartopy(ter) 
    
    # make the figure
    fig, ax = plt.subplots(constrained_layout=True)
    
    if ii == start_index: 
        # plot the 2d terrain just the first time
        ter_plot = plt.contourf(ridge_dist, to_np(lats[:, 0]), to_np(ter),
                        cmap=colormaps['terrain'], 
                        levels=ter_heights, extend='both')
        
        # colorbar label with terrain height values
        cbar = plt.colorbar(ter_plot, ax=ax, orientation="horizontal",
                        ticks=ter_heights)
        cbar.set_label("Terrain Height [m]", fontsize=10)
        
    # plot the level set function contour at 0
    # add the timestamp to the contour label
    ls_contour = ax.contour(ridge_dist_fire, to_np(fxlats[:, 0]), to_np(ls),
                           levels=[0.0], colors='red', linewidths=2.0)
    ax.clabel(ls_contour, fmt={0.0: f'Fire Perimeter {str(ct)[11:16]}'}, colors='red')
        
    # make pretty titles and whatnot
    ax.set_xticks(np.arange(-18000, 19000, 6000))
    ax.set_xlabel("Distance from Ridge Top [m]")
    ax.set_xlim([-17000, 19000])

plt.savefig(save_path + "overlay_level_set")
plt.close() 
           
print("Complete")     
    