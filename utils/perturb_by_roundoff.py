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

from context import name_dir, output_dir

##### USER INPUT #####

exp = "TEST-REAL-POS1"
var_perturb = "T" # ["T", "U_1" (U_2), "V_1" (V_2), "QVAPOR"]
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

# open the file
ds = xr.open_dataset(restart_file)

# stochastically perturb the variable
rng = np.random.default_rng(seed=seed_value)
ds[var_perturb] = ds[var_perturb] + np.random.normal(0, error, 
                                                     ds[var_perturb].shape)