"""
    
    Plot 2d fire perimeter from the fire module
    
    
    Required: WRF output file directory (loop through many files)
    
    Output: plot for each time of the sfc variable
    
    lbuchart@eoas.ubc.ca
    November 13, 2025
    
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
    
    # get the fire area
    htflux = getvar(ncfile, "GRNHFX", meta=True)  # GRNHFX, FS_FIRE_AREA
    smoke = getvar(ncfile, "fire_smoke", meta=True)
    area = getvar(ncfile, "FS_FIRE_AREA", meta=True)
    
    # print the sum of the area
    print('Total heatflux: ', np.sum(to_np(htflux)))
    print('Total smoke: ', np.sum(to_np(smoke)))
    print('Total area: ', np.sum(to_np(area)))
    
    # get the terrain height
    ter = getvar(ncfile, "ter", meta=True)
    ter_cross = interpline(ter, 
                           start_point=CoordPair(start[0], start[1]),
                           end_point=CoordPair(end[0], end[1]))
    ridge_dist = dist_from_ridge(ter_cross)
    
    # some values to make nice figures    
    # Get the latitude and longitude points
    lats, lons = latlon_coords(smoke)

    # Get the cartopy mapping object
    cart_proj = get_cartopy(smoke) 
    
    if ii >= 3:  # fire doesnt start until 15 mins (3 output cycles)
        # make the figure
        fig, ax = plt.subplots(constrained_layout=True)
    
        # levels to plot the velocity perturbation
        #wind_levels = np.arange(0, 15, 1)
        ter_levels = np.arange(0, 1000, 200) 
    
        # Make the contours of terrain and wind perturbation
        ter_lines = plt.contour(ridge_dist, to_np(lats[:, 0]), to_np(ter), 
                            levels=ter_levels, colors="black")
        area_contour = plt.contourf(ridge_dist, to_np(lats[:, 0]), to_np(htflux), 
                             extend="max", cmap=colormaps['Reds'])
    
        # make pretty titles and whatnot
        ax.set_xticks(np.arange(-18000, 19000, 6000))
        ax.set_xlabel("Distance from Ridge Top [m]")
        ax.set_xlim([-17000, 19000])
    
        # colorbar 
        cbar = plt.colorbar(to_np(area_contour), ax=ax,
                        orientation="horizontal")
        cbar.set_label("Fire Heat Flux [W/m^2]", fontsize=10)  # [W/m^2]
    
        plt.savefig(save_path + "heat_flux_" + str(ct)[11:19])
        plt.close() 
    
        # plot the column integrated smokes
        plot_smoke = np.sum(smoke, axis=0)
        fig, ax = plt.subplots(constrained_layout=True)
    
        ter_levels = np.arange(0, 1000, 200) 
    
        # Make the contours of terrain and wind perturbation
        ter_lines = plt.contour(ridge_dist, to_np(lats[:, 0]), to_np(ter), 
                            levels=ter_levels, colors="black")
        smoke_contour = plt.contourf(ridge_dist, to_np(lats[:, 0]), to_np(plot_smoke), 
                             extend="max", cmap=colormaps['Purples'])
    
        # make pretty titles and whatnot
        ax.set_xticks(np.arange(-17000, 19000, 6000))
        ax.set_xlabel("Distance from Ridge Top [m]")
        ax.set_xlim([-17000, 19000])
    
        # colorbar 
        cbar = plt.colorbar(to_np(smoke_contour), ax=ax,
                        orientation="horizontal")
        cbar.set_label("Smoke Density [g_smoke/kg_air]", fontsize=10)  # [g_smoke/kg_air], [W/m^2]
    
        plt.savefig(save_path + "integrated_smoke_" + str(ct)[11:19])
        plt.close()