"""
    Docstring for utils.perturb_by_roundoff
    Functions to open modify wrf restart files
    
    Perturb the input_variable the roundoff error of fir
    See test_roundoff.py for an estimate
    Resave the wrf restart file with the same name
    
    lbuchart@eoas.ubc.ca
    January 5, 2026
"""
#%%
import xarray as xr
import os
import numpy as np
import matplotlib.pyplot as plt

from context import name_dir, output_dir, pertubation_dir

##### USER INPUT #####

exp = "TEST-REAL-POS1"
perturb_var = "T" # ["T", "U_1" (U_2), "V_1" (V_2), "QVAPOR"]
error = 10e-15
seed_value = 10 # random seed 10 different perturbations [10, 15, 20, 25, 30, 35, 40, 45, 50, 55]

#### END USER INPUT #####
full_path = f"{output_dir}/{exp}/output/" # name of the input

# get all restart files
restart_files = []
for root, dirs, files in os.walk(full_path):
    for file in files:
        if file.startswith("wrfrst"):
            restart_files.append(os.path.join(root, file))

# only need to deal with the final file in this list
restart_file = restart_files[-1]
print(restart_file)

# extract the datetime from the file name
date_time = restart_file.split("/")[-1].split("rst")[1]
print(f"Date: {date_time}") 

# open the file
ds = xr.open_dataset(restart_file)

# extract the perturbable variable
var_init = np.squeeze(ds[perturb_var].values) 

# stochastically perturb the variable
rng = np.random.default_rng(seed=seed_value)
ds[perturb_var] = ds[perturb_var] + np.random.normal(0, error, 
                                                     ds[perturb_var].shape)

# extract the perturbed variable
var_perturb = np.squeeze(ds[perturb_var].values)

# difference
var_diff = var_init - var_perturb

# compare in matplotlip plot
fig, ax = plt.subplots(1, 3, figsize=(8, 8))
ax[0].imshow(var_init[10, :, :])
ax[1].imshow(var_perturb[10, :, :])
diff_plot = ax[2].imshow(var_diff[10, :, :])
# add colorbar to the final figure
plt.colorbar(diff_plot, ax=ax[2], orientation="horizontal")
plt.savefig(f"{pertubation_dir}plot_{perturb_var}_{seed_value}{date_time}.png")
plt.close()

# save the file
print(f"Saving to {pertubation_dir}wrfrst_{perturb_var}_{seed_value}_{error}.nc...")
ds.to_netcdf(pertubation_dir + f"wrfrst_{perturb_var}_{seed_value}{date_time}.nc")