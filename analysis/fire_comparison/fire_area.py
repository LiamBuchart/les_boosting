"""

  Simple grab of multiple fire area files to compare total fire area

  lbuchart@eoas.ubc.ca
  November 21, 2025

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

# for real experiments this data will be stores in a json file
exps = ["TEST-REAL-BRUSH/", "TEST-REAL-FIRE/", "TEST-REAL-SPOTTING/", "TEST-FIRE-LARGE/", 
        "TEST-REAL-VALLEY/", "TEST-SPOTTING-LOW/", "TEST-VALLEY-LARGE/",
        "TEST-LEE-SLOPE/"]
labels = ["Brush Fire", "Test Grass", "Spotting Grass", "Large Fire Ignition", 
          "Valley Fire", "Spotting Low", "Valley Large", "Lee Slope"]

comp_save_path = "/home/lbuchart/les_boosting/analysis/FIGURES/FIRE_COMPARISON/"
##########

# load grid dimensions which are saved in the context file
with open(str(json_dir) + "config.json") as f:
    config = json.load(f)
    
dx = config["grid_dimensions"]["dx"]  # grid dimensions
dy = config["grid_dimensions"]["dy"]  # grid dimensions

# loop through experiments to get areas into a dataframe
fire_areas = pd.DataFrame(columns=exps)
for ee in exps:
    path, save_path, relevant_files, wrfin = setup_script(exp=ee)
    
    for ii in range(0, len(wrfin)):
        # import the file in a readable netcdf format
        ncfile = wrfin[ii]
        
        # get the fire area
        area = getvar(ncfile, "FS_FIRE_AREA", meta=True)
        
        # convert to m^2
        area = to_np(area) * (dx * dy)
        # convert to ha
        area = area / 10000
        
        # put into a dataframe
        fire_areas.loc[ii, ee] = np.sum(area)
        
        ct = extract_times(ncfile, timeidx=0)
        
        # append the times (some varying experiment lengths)
        fire_areas.loc[ii, 'Time'] = str(ct)[11:16]  # only keep hh:mm

print(fire_areas.head())   
# add nans to empty cells
fire_areas = fire_areas.fillna(np.nan)
     
# save the fire areas to a csv
fire_areas.to_csv(comp_save_path + "fire_areas_comparison.csv", index=False)

# make a plot comparing fire areas
plt.figure(figsize=(10, 6))

for ee, lab in zip(exps, labels):
    plt.plot((fire_areas['Time']).astype(str), fire_areas[ee], 
             label=lab, linestyle='--', marker='o')

# clean up x-axis labels
plt.xticks(rotation=45)
# clean y-axis limits and labels
ylabels = np.arange(0, 140, 10)
plt.yticks(ylabels)
plt.ytick_labels = [str(int(yy)) for yy in ylabels]
plt.gca().set_yticklabels(plt.ytick_labels)
plt.ylim(bottom=0)
plt.xlim([fire_areas["Time"].iloc[0], fire_areas["Time"].iloc[-1]])

# add labels and legend
plt.legend()
plt.xlabel("Time [LT]", fontsize=12)
plt.ylabel("Fire Area [m^2]", fontsize=12)
plt.title("Fire Area Comparison", fontsize=14)
plt.tight_layout()
plt.savefig(comp_save_path + "fire_area_comparison")
    
print("Complete") 