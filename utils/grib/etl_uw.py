"""
    
    Utility functions for ETL operations on GRIB files.
    Grab files from a variety of internation weather
    forecast models to then generate the input soundings
    Note: the ICON model is grabbed from etl_icon.py because the 
    open_meteo api gives a code snippet to use.
    
    lbuchart@eoas.ubc.ca    
    October 10, 2025
    
"""
#%%
import requests
import os
import pandas as pd

from siphon.simplewebservice.wyoming import WyomingUpperAir
from datetime import datetime

### USER INPUTS
station = "CWVK"
s_elev = 379  # station elevation at Vernon
date = datetime(2025, 9, 26, 00)  # year, month, day, hour (UTC)

save_dir = "./"
if not os.path.exists(save_dir):
    os.makedirs(save_dir)
### END USER INPUTS 
    
def convert_datetime(datetime):
    # save as YYYYMMDD_HH
    return datetime.strftime("%Y%m%d_%H")
    
def real_sounding(datetime):
    print("Pulling real sounding from Wyoming Upper Air...")
    df = WyomingUpperAir.request_data(date, station)
    
    df["datetime"] = convert_datetime(datetime)
    
    return df

#%%
## main
# just select which function is needed for your purpose
df = real_sounding(date)
df.to_csv(f"{save_dir}/real_sounding_{station}_{df.datetime[0]}.csv", index=False, sep=',')