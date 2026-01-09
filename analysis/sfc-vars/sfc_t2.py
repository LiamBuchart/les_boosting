"""
    
    2m temperatures plots
    
    Required: WRF output file directory (loop through many files)
    
    Output: 2d plot for each wrfout file
    
    lbuchart@eoas.ubc.ca
    November 15, 2025
    
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

## USER INPUTS ##
# option
exp = "TEST-REAL-POS1" + "/"  # name of the experiment you are plotting
lev = 10  # height in m that you want wind velocity perturbation

start = (0, 80)
end = (-1, 80) 

## END USER INPUTS ##

path, save_path, relevant_files, wrfin = setup_script(exp=exp)

# loop through files to get velocity 
for ii in range(0, len(wrfin)):
    # import the file in a readable netcdf format
    ncfile = wrfin[ii]
    
    # extract the time in datetime format
    ct = extract_times(ncfile, timeidx=0)
    print(ct)
    
    # get the 2m temperatures
    t2 = getvar(ncfile, "T2", meta=True) 
    #t = getvar(ncfile, "temp", units="degC", meta=True)
    #print(np.shape(t), np.min(to_np(t)), np.mean(to_np(t)), np.max(to_np(t)))
    
    height = getvar(ncfile, "height_agl", units="m",
                    meta=True)
    #t2 = interplevel(t, height, 5, meta=True)
    
    print(np.shape(t2))
    print(np.min(to_np(t2)),np.mean(to_np(t2)), np.max(to_np(t2)))

    # get the terrain height
    ter = getvar(ncfile, "ter", meta=True)
    ter_cross = interpline(ter, 
                           start_point=CoordPair(start[0], start[1]),
                           end_point=CoordPair(end[0], end[1]))
    ridge_dist = dist_from_ridge(ter_cross)
    
    # some values to make nice figures    
    # Get the latitude and longitude points
    lats, lons = latlon_coords(t2)

    # Get the cartopy mapping object
    cart_proj = get_cartopy(t2) 
    
    # make the figure
    fig, ax = plt.subplots(constrained_layout=True)
    
    # levels to plot the velocity perturbation
    temp_levels = np.arange(-30, 35, 5)
    ter_levels = np.arange(0, 1000, 200) 
    
    # Make the contours of terrain and wind perturbation
    ter_lines = plt.contour(ridge_dist, to_np(lats[:, 0]), to_np(ter), 
                            levels=ter_levels, colors="black")
    t_contour = plt.contourf(ridge_dist, to_np(lats[:, 0]), to_np(t2)-273.15,
                             levels=temp_levels, 
                             extend="max", cmap=colormaps['coolwarm'])
    
        # make pretty titles and whatnot
    ax.set_xticks(np.arange(-18000, 18000, 6000))
    ax.set_xlabel("Distance from Ridge Top [m]")
    ax.set_xlim([-17000, 19000])
    
    # colorbar 
    cbar = plt.colorbar(to_np(t_contour), ax=ax,
                        ticks=np.arange(temp_levels[0], temp_levels[-1], 5),
                        orientation="horizontal")
    cbar.set_label("Temperature [°C]", fontsize=10)
    
    plt.savefig(save_path + "temp_2m_" + str(ct)[11:19])
    plt.close()  