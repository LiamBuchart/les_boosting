#!/bin/bash
#SBATCH -t 06:00:00
#SBATCH --nodes=8
#SBATCH --ntasks-per-node=32
#SBATCH --mail-type=ALL
#SBATCH --mail-user=lbuchart@eoas.ubc.ca
#SBATCH --account=def-rstull

ml StdEnv/2023  gcc/12.3  openmpi/4.1.5
module load wrf/4.7.1

exp=TEST-REAL
cd ../exps/${exp}

rm -r rsl.*

#rm -r namelist.input
#ln -sv namelist.input.spinup namelist.input

srun ./wrf.exe 1>wrf.log 2>&1

mkdir -p log
mv rsl.* log/
mv wrf.log log/

mkdir -p /home/lbuchart/scratch/lbuchart/les_boosting_output/output/${exp}/
mv wrfout* /home/lbuchart/scratch/lbuchart/les_boosting_output/output/${exp}/

#rm -r namelist.input
#ln -sv namelist.input.restart namelist.input

#srun ./wrf.exe 1>wrf.log 2>&1

#mkdir -p log/restart
#mv rsl.* log/restart/
#mv wrf.log log/restart/
