"""
    
    Plot vertical cross section of potential temperature and wind speed 
    through the center of the domain.
    Include topography (add option to include wind barbs)
    
    Required: WRF output file directory (loop through many files)
    
    Output: plot for each time of the vertical cross section
    
    lbuchart@eoas.ubc.ca
    August 12, 2022
    November 12, 2025 - reconfig for les-boosting
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import xarray as xr
  
from netCDF4 import Dataset
from context import name_dir, script_dir
from file_funcs import (setup_script, get_heights, 
                        dist_from_ridge, fmt)
from icecream import ic

from wrf import (getvar, xy, interp2dxy, interpline, 
                CoordPair, get_cartopy, to_np,
                extract_times)
    
########## 

## USER INPUTS ##
# options [
exp = "TEST-REAL-BRUSH" + "/" # name of the experiment you want to plot
start = (0, 80)
end = (-1, 80)

## END USER INPUTS ##

path, save_path, relevant_files, wrfin = setup_script(exp)

# extract heights of all layers 
heights = get_heights(wrfin[0])

ic("These are the heights")
ic(heights[:, 1, 1])

ys = heights[:, 0, 0]  
ys = ys[1:]

# loop through files list and make our plots
all_temp = []
all_pot = []
for ii in range(0, len(wrfin)):
    # import the file in a readable netcdf format
    print(relevant_files[ii])
    ncfile = wrfin[ii]
    
    # get the time in datetime format
    ct = extract_times(ncfile, timeidx=0)
    print(ct)
    
    # temperatures
    TT = getvar(ncfile, "T", 
               meta=True)
    TT_line = xy(TT, start_point=start, end_point=end)
    TT_cross = interp2dxy(TT, TT_line)
    print("temps is in ")
    print("Mean temp: ", np.mean(to_np(TT_cross)))
    
    # potential temperature
    theta = getvar(ncfile, "theta", units="k", 
                   meta=True)
    theta_line = xy(theta, start_point=start, end_point=end)
    theta_cross = interp2dxy(theta, theta_line)
    print("potentialtemps are in")
    
    # terrain
    ter = getvar(ncfile, "ter", meta=True)
    ter_cross = interpline(ter, 
                           start_point=CoordPair(start[0], start[1]),
                           end_point=CoordPair(end[0], end[1]))
    print("terrain is in ")

    ridge_dist = dist_from_ridge(ter_cross)
    
    # get the cartopy projections
    proj = get_cartopy(TT)

    # make the figure
    fig, axs = plt.subplots(2, 1, 
                            sharex=True,
                            gridspec_kw={"height_ratios":[5, 1]})

    temp_levels = np.arange(15, 105, 5)  # contour lines 
    theta_levels = np.arange(270, 370, 1)

    xs = np.arange(0, TT.shape[-1], 1)
    temp_contour = axs[0].contourf(ridge_dist,
                                ys,
                                to_np(TT_cross),
                                cmap="Reds",
                                extend="both",
                                levels=temp_levels)

    xs = np.arange(0, theta.shape[-1], 1)
    theta_contour = axs[0].contour(ridge_dist, 
                               ys,
                               to_np(theta_cross), 
                               colors="k",
                               levels=theta_levels)
    
    axs[0].clabel(theta_contour, theta_contour.levels[::2], inline=True, fmt=fmt, fontsize=10)

    ht_fill = axs[1].fill_between(ridge_dist, 0, to_np(ter_cross),
                                  facecolor="saddlebrown")
    
    # hide x labels on all but the bottom 
    for ax in axs:
        ax.label_outer()

    # make pretty titles and whatnot
    axs[0].set_xticks(np.arange(-18000, 19000, 3000))
    axs[1].set_xticks(np.arange(-18000, 19000, 3000))
    
    axs[0].set_xlim([-6000, 6000])
    axs[1].set_xlim([-6000, 6000])

    axs[0].set_ylabel("Height AGL [m]", fontsize=10)
    axs[1].set_ylabel("Terrain Height [m]", fontsize=10)
    #axs[0].yaxis.set_label_coords(-.1, .3)

    axs[0].set_yticks(np.arange(0, 10500, 250))
    axs[0].set_ylim([0, 1000])
    
    axs[1].set_yticks(np.arange(0, 1250, 250))
    axs[1].set_ylim([0, 1000])

    # colorbar 
    fig.tight_layout()  # call this before calling the colorbar and after calling 
    cbar = plt.colorbar(temp_contour, ax=axs)
    cbar.set_label("Temperature [°C]", fontsize=10)
    
    plt.savefig(save_path + f"temp_xsection_{str(ct)[11:19]}")
    plt.close()
    
    # concatenate over all time to get a mean picture
    mTT = TT_cross.to_numpy()
    mtheta = theta_cross.to_numpy()
    if ii == 5:
        all_temp = mTT
        all_pot = mtheta
    elif ii > 5: 
        all_temp = np.dstack((all_temp, mTT))
        all_pot = np.dstack((all_pot, mtheta))
    
# make a plot of the mean of the cross section values
fig, axs = plt.subplots(2, 1, 
                        sharex=True,
                        gridspec_kw={"height_ratios":[5, 1]})

xs = np.arange(0, TT.shape[-1], 1)
TT_contour = axs[0].contourf(ridge_dist,
                            ys,
                            np.mean(all_temp, axis=2),
                            cmap="Reds",
                            extend="both",
                            levels=temp_levels)

xs = np.arange(0, theta.shape[-1], 1)
t_contour = axs[0].contour(ridge_dist, 
                            ys,
                            np.mean(all_pot, axis=2), 
                            colors="k",
                            levels=theta_levels)
    
axs[0].clabel(t_contour, t_contour.levels[::2], inline=True, fmt=fmt, fontsize=10)

ht_fill = axs[1].fill_between(ridge_dist, 0, to_np(ter_cross),
                              facecolor="saddlebrown")
    
# hide x labels on all but the bottom 
for ax in axs:
    ax.label_outer()

# make pretty titles and whatnot
axs[0].set_xticks(np.arange(-18000, 19000, 3000))
axs[1].set_xticks(np.arange(-18000, 19000, 3000))

axs[0].set_xlim([-6000, 6000])
axs[1].set_xlim([-6000, 6000])

axs[0].set_ylabel("Height AGL [m]", fontsize=10)
axs[1].set_ylabel("Terrain Height [m]", fontsize=10)

axs[0].set_yticks(np.arange(0, 10500, 250))
axs[0].set_ylim([0, 1000])
    
axs[1].set_yticks(np.arange(0, 1250, 250))
axs[1].set_ylim([0, 1000])

# colorbar 
fig.tight_layout()  # call this before calling the colorbar and after calling 
cbar = plt.colorbar(TT_contour, ax=axs)
cbar.set_label("Temperature [°C]", fontsize=10)
    
plt.savefig(save_path + "temp_xsection_mean")
plt.close()
    
print("Complete")    
