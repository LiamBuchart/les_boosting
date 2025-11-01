"""
Function which takes a terrain type input:
***** gaussian, sinusoidal, plateau, angular *****
and creates idealized terrain heights based on namelist input
information for your idealized WRF run,

Used to create topography for downslope wind storm experiments.
Note that all configurations with have a max height of 1000m.

lbuchart@eoas.ubc.ca
"""
#%%
import numpy as np
from context import json_dir, name_dir
import json

author="lbuchart"
outfile_name = "input_ht" 
fuel_cat = 1  # one of the Anderson fuel categories used in WRF

# load grid dimensions which are saved in the context file
with open(str(json_dir) + "config.json") as f:
    config = json.load(f)

we_n = config["grid_dimensions"]["ndx"]
sn_n = config["grid_dimensions"]["ndy"]
dx = config["grid_dimensions"]["dx"]  # grid dimensions

sr_x = config["grid_dimensions"]["sr_x"]  # starting region x
sr_y = config["grid_dimensions"]["sr_y"]  # starting region y

# topogrpahy characteristics
mht = config["topo"]["mht"]  # topography height
hw = config["topo"]["hw"]  # topography half width
ridges = config["topo"]["ridge_tops"]  # plaement of ridges

base_elevation = config["topo"]["base_ht"]  # base elevation to add to all heights (Vernon sounding site)

# create a grid of zeros based on namelist size
hgt = np.empty((we_n, sn_n), np.float32)
grid_size = np.shape(hgt)
print(hgt.ndim, grid_size[0], grid_size[1])

# NOTE: the fuels grid is for the fire grid itself (atmos resolution time fire model refinement)
fuels = np.ones((we_n * sr_x, sn_n * sr_y), np.int32) * fuel_cat  # fuels grid (simple)

def agnesi(mht, x, hw):
    # mht is the mountain/ridge maximum height
    # x = range over which the hill is made
    # hw = the half width of the mountain/ridge
            
    return mht * ( (hw**2) / ((hw**2) + (x**2)) )

# loop through the grid and add topography heights based on the chosen methods
# note that topography is added in the east-west direction
for ii in range(grid_size[1]):
        
    r1 = (np.arange(grid_size[0]) * dx) - ridges[0]
    r2 = (np.arange(grid_size[0]) * dx) - ridges[1]
    r3 = (np.arange(grid_size[0]) * dx) - ridges[2]
    
        
    hgt[:, ii] = base_elevation + ( agnesi(mht, r1, hw) + 
                   agnesi(mht, r2, hw) + 
                   agnesi(mht, r3, hw) )

# now add the required info and array to the outfile_name text file which we will create
dims = str(we_n) + " " + str(sn_n)
fuel_dims = str(we_n * sr_x) + " " + str(sn_n * sr_y)

np.savetxt(outfile_name, hgt, header=dims, comments="", fmt="%i")
np.savetxt("input_fc", fuels, header=fuel_dims, comments="", fmt="%i")
print("Saved the height array")