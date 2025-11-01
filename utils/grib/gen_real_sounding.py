"""

    Use the uw sounding data (from etl_uw.py) to generate
    a sounding file suitable for a wrf run
    
    lbuchart@eoas.ubc.ca
    October 15, 2025

"""
import json
import numpy as np
import pandas as pd
import metpy.calc as mpcalc

from metpy.units import units
from context import json_dir

with open(json_dir + 'models.json') as f:
    models = json.load(f)

sounding = models["real"]["name"]
fstring = models["real"]["string"]

obs = pd.read_csv(f"./{sounding}{fstring}")

h = obs["height"].values * units.meter
p = obs["pressure"].values * units.hPa  
T = obs["temperature"].values * units.degC
Td = obs["dewpoint"].values * units.degC 

wind_speed = obs["speed"].values * units.knots
wind_dir = obs["direction"].values * units.degrees
u, v = mpcalc.wind_components(wind_speed, wind_dir) 

# get vapour mixing ratio 
rh = mpcalc.relative_humidity_from_dewpoint(T, Td)
Q = mpcalc.mixing_ratio_from_relative_humidity(p, T, rh) 
Q = Q.to("g/kg")

P0 = p[0]
T0 = T[0]
Q0 = Q[0]                  

input_sounding = pd.DataFrame(columns=["height", "theta", "q", "U", "V"])

# overwrite the base input_sounding dateframe to account for first row formatting
# note that the first row of height is actually the surface pressure
sfc_data = {"height":[P0.magnitude], 
            "theta":[T0.magnitude], 
            "q":[int(Q0.magnitude)], 
            "U":[np.nan], "V":[np.nan]}
input_sounding = pd.DataFrame(sfc_data, index=[0])

# append the rest of the data
for ii in range(1, len(h)):
    theta = mpcalc.potential_temperature(p[ii], T[ii])
    row_data = {"height":[round(h[ii].magnitude, 1)], 
                "theta":[round(theta.magnitude, 1)], 
                "q":[round(int(Q[ii].magnitude), 1)], 
                "U":[round(u[ii].magnitude, 1)], 
                "V":[round(v[ii].magnitude, 1)]}
    row_df = pd.DataFrame(row_data, index=[ii])
    input_sounding = pd.concat([input_sounding, row_df], ignore_index=True)

# clean - remove rows with an NaN or blank values
first_row = input_sounding.iloc[[0]]
above_rows = input_sounding.iloc[1:].dropna()

input_sounding = pd.concat([first_row, above_rows])

input_sounding.to_csv("real_input_sounding.csv", 
                      sep=" ", 
                      header=False, 
                      index=False, 
                      index_label=None)

input_sounding.to_csv("full_real_sounding.csv", 
                      sep=" ", 
                      header=True, 
                      index=False, 
                      index_label=None)  # also save with full headers to call for other scripts