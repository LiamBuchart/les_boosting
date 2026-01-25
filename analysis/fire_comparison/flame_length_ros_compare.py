"""
    
    Simmply grab fire flame length and ros
    plot and compare each experiment
    on subpanels
    
    lbuchart@eoas.ubc.ca
    December 12, 2025    
    
"""
import json

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import colormaps
import metpy.calc as mpcalc

from file_funcs import (setup_script, dist_from_ridge)
from context import json_dir

from wrf import (interpline, extract_times, get_cartopy,
                 getvar, to_np, latlon_coords, CoordPair,
                 interplevel, cartopy_xlim, cartopy_ylim)

##########
exp_list = "Initial_Ensemble_POS1"

# for real experiments this data will be stores in a json file
with open(str(json_dir) + "names.json") as f:
    experiment_info = json.load(f)

# return name of the set of experiments
exp_suite = experiment_info[exp_list]["Suite_Name"]
    
exps = experiment_info[exp_list]["Dir_Names"]
labels = experiment_info[exp_list]["Plot_Names"]

comp_save_path = "/home/lbuchart/les_boosting/analysis/FIGURES/FIRE_COMPARISON/"
##########

# load grid dimensions which are saved in the context file
with open(str(json_dir) + "config.json") as f:
    config = json.load(f)
    
dx = config["grid_dimensions"]["dx"]  # grid dimensions
dy = config["grid_dimensions"]["dy"]  # grid dimensions

# loop through experiments to get areas into a dataframe
fire_ros = pd.DataFrame(columns=exps)
fire_fl = pd.DataFrame(columns=exps)
for ee in exps:
    print(ee)
    path, save_path, relevant_files, wrfin = setup_script(exp=ee)
    
    for ii in range(0, len(wrfin)):
        # import the file in a readable netcdf format
        ncfile = wrfin[ii]
        
        # get flame length and ros
        fl = getvar(ncfile, "FLAME_LENGTH", meta=True)
        ros = getvar(ncfile, "ROS_FRONT", meta=True)
        
        # put the max values into a dataframe
        fire_ros.loc[ii, ee] = np.max(to_np(ros))
        fire_fl.loc[ii, ee] = np.max(to_np(fl))
        
        ct = extract_times(ncfile, timeidx=0)
        # append the times (some varying experiment lengths)
        fire_ros.loc[ii, 'Time'] = str(ct)[11:16]  # only keep hh:mm
        fire_fl.loc[ii, 'Time'] = str(ct)[11:16]  # only keep hh:mm
        
print(fire_ros.head())
print(fire_fl.head())

# add nans to empty cells
fire_ros = fire_ros.fillna(np.nan)
fire_fl = fire_fl.fillna(np.nan)
     
# save the fire areas to a csv
fire_ros.to_csv(comp_save_path + "fire_ros_comparison.csv", index=False)
fire_fl.to_csv(comp_save_path + "fire_fl_comparison.csv", index=False)  

# make a plot comparing fire flame length and ros (on different y-axis)
fig, ax = plt.subplots(figsize=(12, 12))

# clean up 
plt.xticks(rotation=45)
ymax_plot = max(list(fire_ros.max())[0:-1])
plt.ylim([0, ymax_plot * 1.1]) 
#plt.xlim([fire_ros["Time"].iloc[0], fire_ros["Time"].iloc[-1]])

# plot ros on left y-axis
for ee, lab in zip(exps, labels):
    plt.plot((fire_ros['Time']).astype(str), fire_ros[ee], 
             label=lab, linestyle='-', marker='*', linewidth=2)
plt.ylabel("Rate of Spread[m/s]: Solid Lines", fontsize=16) 

# add legend
plt.legend(fontsize=14)

# plot fire flame length on right y_axis
ax.twinx()
ymax_plot = max(list(fire_fl.max())[0:-1])
plt.ylim([0, ymax_plot * 1.1]) 

for ee, lab in zip(exps, labels):
    ax.plot((fire_fl['Time']).astype(str), fire_fl[ee], 
             label=lab, linestyle='--', marker='o', linewidth=2)
plt.ylabel("Flame Length [m]: Dashed Lines", fontsize=16)

# set title
plt.xlabel("Time [LT]", fontsize=16)
plt.title("Flame Length and Rate of Spread Comparison", fontsize=16)

# add _ to all blank spaces in experiment suite name
exp_suite = exp_suite.replace(" ", "_")

plt.savefig(comp_save_path + f"{exp_suite}_flame_length_ros_comparison.png")
print("Done...")