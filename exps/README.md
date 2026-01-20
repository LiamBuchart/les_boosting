Directory for all experiment setup.
Subdirectories are named for the model on which the initial sounding is constructed. 
Soundings are generated in ../utils/grib/

Real - sounding from the Vernon launch site 
ICON - German ICON 9km model
HRDPS - High Resolution Deterministic model 2.5km
ECMWF - Mid-range model 9km
GFS - NCEP GFS (0.25deg) ~28km

All directories with dates newer than December 5, 2025 use Anderson Fuel Category 2. Reference the json (located in the json directory) for ignition names and positions. E.g. the directory named REAL-POS1 cooresponds to the Real sounding at ignition location on (center ridge top).

Dead Fuel Moisture Content:
Default dead fuel moisture content in set to 0.18 (18%) in fuel Category 2. However, this is above the defined fuel moisture content of extinction (0.15). The defined fuel moisture content of extinction comes from the defined Anderson fuel categories. 
----------- 
> Based on the sounding surface temperature (18.8) and dewpoint (-0.2) yeilds a relative humidity of ~28% - this gives an approximated fuel moisture content of 7-8%.
> Based on the RH of the day (~40% - from the CWFIS website at hotspot locations) the dead fuel moisture would be ~10-11%. 
> Based only on the FFCM the needle moisture content is ~9%.
> Based only on the DMC the moisture content of the loosely compacted organic layer is ~25%.
> Based only on the DC the mositure content of the deep, compact, organic layers are ~62%.

By the observation period on Sep 27, the fire was 147 ha, closely corresponding to the 14% fuel moisture content run.

Given that the two fires had similar burn periods and sufficiently complex terrain, a total fuel moisture of 14% is used. This corresponds well to the burned area comparison and a composite of the FFMC, DMC, and DC fuel moistures. 

Pre-perturbation output is stored in the base output directory (/home/lbuchart/scratch/les_boosting_output/{exp}/output/) all post-restart output is stored in a subdirectory titled either UNPERTURBED or is named after the variable that is perturbed and the random seed that is used for the pertubation.
