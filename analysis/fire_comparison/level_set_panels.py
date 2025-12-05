"""

    Plot level set function overlay for each expeiment in a different panel
    Similar method to level_set.py but all plots are combined into a single figure with subplots.
    Zoomed in on the region of interest.
    
    December 3, 2025
    lbuchart@eoas.ubc.ca

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colormaps
import metpy.calc as mpcalc

from file_funcs import (setup_script, dist_from_ridge)

from wrf import (interpline, extract_times, get_cartopy,
                 getvar, to_np, latlon_coords, CoordPair,
                 interplevel, cartopy_xlim, cartopy_ylim)

##########

# for real experiments this data will be stores in a json file
exps = ["TEST-REAL-BRUSH/", "TEST-REAL-SPOTTING/", "TEST-FIRE-LARGE/", 
        "TEST-REAL-VALLEY/", "TEST-VALLEY-LARGE/", "TEST-LEE-SLOPE/"]
labels = ["Brush Fire", "Spotting Grass", "Large Fire Ignition", 
          "Valley Fire", "Valley Large", "Lee Slope"]

comp_save_path = "/home/lbuchart/les_boosting/analysis/FIGURES/FIRE_COMPARISON/"
##########

# initialize the figure and axes (manual based on experiments)
nrows = 2
ncols = 3
fig, axs = plt.subplots(nrows, ncols, figsize=(12, 10))  #, constrained_layout=True)

count = 0
for ee in exps:
    plot_label = labels[count]
    count += 1
    path, save_path, relevant_files, wrfin = setup_script(exp=ee)
    
    # set the panel in which the experiment will be plotted
    exp_index = exps.index(ee)
    row = exp_index // ncols
    col = exp_index % ncols
    print(f"Plotting experiment: {ee} in row {row} col {col}")
    
    # get the terrain height - just get once
    ter = getvar(wrfin[0], "ter", meta=True)
    ter_heights = np.arange(150, 850, 10)
    
    # get fire coords just once
    lats, lons = latlon_coords(ter)
    fxlats = getvar(wrfin[0], "FXLAT", meta=True)
    fxlons = getvar(wrfin[0], "FXLONG", meta=True)
    
    for ii in range(2, len(wrfin), 3):
        # import the file in a readable netcdf format
        ncfile = wrfin[ii]
        
        # extract the time in datetime format
        ct = extract_times(ncfile, timeidx=0)
        
        # get the fire area
        ls = getvar(ncfile, "LFN", meta=True)
        
        # change first and last row and columns to nan to avoid contouring issues
        # fire shouldnt get to the edge anyways!
        ls[:, 0:10] = np.nan
        ls[:, -10:] = np.nan
        ls[0:10, :] = np.nan
        ls[-10:-1, :] = np.nan
        
        # get coordinate of min ls
        min_lat, min_lon = np.unravel_index(np.nanargmin(ls), ls.shape)
        fire_lat = fxlats[min_lat, 0]
        fire_lon = fxlons[0, min_lon]
        
        # defined a bounding box around the fire
        bbox = [fire_lon-600, fire_lon+600, fire_lat-400, fire_lat+400]

        # Get the cartopy mapping object
        cart_proj = get_cartopy(ter) 
        
        # plot terrain contours
        ter_contours = axs[row, col].contour(to_np(lons[0, :]), to_np(lats[:, 0]), 
                                  to_np(ter), levels=ter_heights, 
                                  colors='black', linewidths=0.5)
        # add contour labels
        axs[row, col].clabel(ter_contours, fmt='%d', inline=1, colors='black')
        
        # plot the level set function contour at 0  
        ls_contour = axs[row, col].contour(to_np(fxlons[0, :]), to_np(fxlats[:, 0]), 
                                to_np(ls), levels=[0], colors='red', 
                                linewidths=2)
        axs[row, col].clabel(ls_contour, fmt={0: str(ct)[11:19]}, inline=1, colors='red')
        
        # zoom to the region of contours
        axs[row, col].set_xlim(bbox[0], bbox[1])
        axs[row, col].set_ylim(bbox[2], bbox[3]) 
        axs[row, col].set_title(plot_label, fontsize=16)
        
        

fig.text(0.5, 0.04, 'Distance from Lower Left [m]', 
         ha='center', fontsize=16)
fig.text(0.04, 0.5, 'Distance from Lower Left [m]', 
         va='center', rotation='vertical', fontsize=16)
        
# save the figure
plt.suptitle("Fire Front Evolution Comparison", fontsize=18)

plt.savefig(comp_save_path + "fire_comparison_level_set_panels")
plt.close()

print("Made a nice plots perhaps? We will find out...")       