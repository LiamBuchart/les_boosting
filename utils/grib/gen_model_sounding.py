"""

    Use the data downloaded from open-meteo.com to generate
    an wrf suitable input_sounding file

"""
import json
import re
import numpy as np
import pandas as pd
import metpy.calc as mpcalc
import matplotlib.pyplot as plt

from metpy.units import units
from context import json_dir

##### User Input #####
model_select = "gfs"  # select model from models.json
##### End User Input #####

with open(json_dir + 'models.json') as f:
    models = json.load(f)

model_names = models["models"]["names"]
model_vars = models["models"]["vars"]
fstring = models["models"]["string"]

time_index = 24  # grab the 36th time step (12 UTC on day 1)

# ensure that model select is in model names
if model_select not in model_names:
    raise ValueError(f"Model {model_select} not in model names: {model_names}")
else:
    model = model_select

# create empty dataframe for input_sounding
input_sounding = pd.DataFrame(columns=["height", "theta", "q", "U", "V"])

print("Processing model: ")
print(model, " ", fstring)
mfile = pd.read_csv(f"./{model}{fstring}")

P0 = mfile["surface_pressure"].iloc[time_index]  # surface pressure
T0 = mfile["temperature_2m"].iloc[time_index]  # 2m temperature
rh0 = mfile["relative_humidity_2m"].iloc[time_index] 
rh0 = rh0/100

# get vapour mixing ratio at surface
Q0 = mpcalc.mixing_ratio_from_relative_humidity(P0 * units.hPa,
                                                T0 * units.degC,
                                                rh0 * units.dimensionless).to('g/kg')

# convert T0 to potential temperature
theta0 = mpcalc.potential_temperature(P0 * units.hPa, T0 * units.degC)

sfc_data = {"height":[P0], 
            "theta":[theta0.magnitude], 
            "q":[Q0.magnitude], 
            "U":[np.nan], "V":[np.nan]}
input_sounding = pd.DataFrame(sfc_data, index=[0]) 

base_model_data = pd.DataFrame(columns=model_vars)

# loop through variables
for var in model_vars:    
    
    print(f"Processing variable: {var}")
    # print variables with varible in the name and sort
    var_cols = [col for col in mfile.columns if var in col]
    
    # sort these columns
    var_cols = sorted(var_cols, key=lambda x: int(re.findall(r'\d+', x)[0]))
    
    # plot a vertical profile of geopotential height at the first time step
    var_data = mfile[var_cols].iloc[time_index].values
    
    if var != "geopotential_height":
        print("Removing surface value for non-geopotential height variable")
        var_data = var_data[1:]  # remove surface value for non-geopotential height variables
    
    base_model_data[var] = var_data
    
    #plt.plot(var_data, label=model)
    #plt.savefig(f"{model}_geopotential_profile.png")

# get a pressure proxy    
pressure = mpcalc.height_to_pressure_std(list(base_model_data["geopotential_height"]) * units.meters)
base_model_data["pressure"] = pressure.magnitude

# get the mixing ratio
Q = mpcalc.mixing_ratio_from_relative_humidity(list(base_model_data["pressure"]) * units.hPa,
                                            list(base_model_data["temperature"]) * units.degC,
                                            list(base_model_data["relative_humidity"] / 100) * units.dimensionless).to('g/kg')

# U and V winds from speed and dir
U, V = mpcalc.wind_components(list(base_model_data["wind_speed"]) * units('km/h'),
                              list(base_model_data["wind_direction"]) * units.deg)
U = U.to('m/s')
V = V.to('m/s')

# get potential temperature
theta = mpcalc.potential_temperature(list(base_model_data["pressure"]) * units.hPa,
                                     list(base_model_data["temperature"]) * units.degC)

# add to the base_model_data dataframe
base_model_data["Q"] = Q.magnitude
base_model_data["U"] = U.magnitude
base_model_data["V"] = V.magnitude
base_model_data["theta"] = theta.magnitude
    
# clean Nans from base_model_data
print(base_model_data)
print("Cleaning NaN values from base_model_data")
base_model_data = base_model_data.dropna().reset_index(drop=True)

# add to input_sounding, flipping so that surface is first
for ii in range(len(base_model_data)-1, -1, -1):
    row_data = {"height":[round(base_model_data["geopotential_height"].iloc[ii], 1)], 
                "theta":[round(base_model_data["theta"].iloc[ii], 1)], 
                "q":[round(int(base_model_data["Q"].iloc[ii]), 1)], 
                "U":[round(base_model_data["U"].iloc[ii], 1)], 
                "V":[round(base_model_data["V"].iloc[ii], 1)]}
    row_df = pd.DataFrame(row_data, index=[ii])  
    input_sounding = pd.concat([input_sounding, row_df], ignore_index=True) 
    
# round all values to 1 decimal place
input_sounding = input_sounding.round(1) 
print(input_sounding)

# save the input_sounding file
input_sounding.to_csv(f"{model}_input_sounding.csv",
                      sep=" ",
                      header=False,
                      index=False,
                      index_label=None)
print(f"Saved {model}_input_sounding.csv")