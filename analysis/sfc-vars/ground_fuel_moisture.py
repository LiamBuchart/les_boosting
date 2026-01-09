"""
    
    2d plot of ground fuel moisture and contour
    the topography
    full domain look
    
    lbuchart@eoas.ubc.ca
    December 12, 2025    
    
"""
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.cm import get_cmap
import metpy.calc as mpcalc

from file_funcs import (setup_script, dist_from_ridge,
                        vert_dist_center)

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

# loop through files to get fuel moisture
for ii in range(0, len(wrfin)):
    # import the file in a readable netcdf format
    ncfile = wrfin[ii]
    
    # extract the time in datetime format
    ct = extract_times(ncfile, timeidx=0)
    print(ct)
    
    fmc = getvar(ncfile, "FMC_G", meta=True)
    
    ter = getvar(ncfile, "ZSF", meta=True)
    print(np.shape(ter))
    ter_cross = interpline(ter, 
                           start_point=CoordPair(start[0], start[1]),
                           end_point=CoordPair(end[0], end[1]))
    ridge_dist = dist_from_ridge(ter_cross) 
    
    ter_cross_perp = interpline(ter, 
                           start_point=CoordPair(start[1], start[0]),
                           end_point=CoordPair(end[1], end[0]))   
    
    dist_center_y = vert_dist_center(ter_cross_perp)
    
    # some values to make nice figures    
    # Get the latitude and longitude points
    
    # make the figure
    fig, ax = plt.subplots(constrained_layout=True)
    
    ter_levels = np.arange(0, 1000, 200) 
    # Make the contours of terrain and wind perturbation
    ter_lines = plt.contour(ridge_dist, dist_center_y, to_np(ter), 
                            levels=ter_levels, colors="black")
    
    fmc_contour = plt.contourf(ridge_dist, dist_center_y, to_np(fmc),
                            extend="max", cmap=get_cmap("RdYlGn"))
    
    # make pretty titles and whatnot
    ax.set_xticks(np.arange(-18000, 19000, 6000))
    ax.set_xlabel("Distance from Ridge Top [m]")
    ax.set_xlim([-17000, 19000])
    
    # colorbar 
    cbar = plt.colorbar(to_np(fmc_contour), ax=ax,
                        orientation="horizontal")
    cbar.set_label("Ground Fuel Moisture [ ]", fontsize=10)
    
    plt.savefig(save_path + "ground_fuel_moisture_" + str(ct)[11:19])
    plt.close()
    
print("Complete")

# add a zsf contourf plot
fig, ax = plt.subplots(constrained_layout=True)
plt.imshow(to_np(ter), cmap=get_cmap("terrain"))
#ter_levels = np.arange(0, 1000, 100) 
# Make the contours of terrain and wind perturbation
#ter_lines = plt.contourf(ridge_dist, dist_center_y, to_np(ter),
#                        levels=ter_levels, extend="max", 
#                        cmap=get_cmap("terrain"))
    
# make pretty titles and whatnot
#ax.set_xticks(np.arange(-18000, 19000, 6000))
#ax.set_xlabel("Distance from Ridge Top [m]")
#ax.set_xlim([-17000, 19000])
    
# colorbar 
cbar = plt.colorbar(orientation="horizontal")
cbar.set_label("Terrain [m]", fontsize=10)

plt.savefig(save_path + "terrain_ZSF")
plt.close()