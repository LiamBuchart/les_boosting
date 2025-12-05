#!/bin/bash
# very simple script to set your python environment to run wrf analysis
# just need these modules to use wrf-python, xarray, etc.
# execute: source set_python.sh

ml scipy-stack mpi4py netcdf

source ./venv/bin/activate
