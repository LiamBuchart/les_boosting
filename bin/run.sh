#!/bin/bash
#SBATCH -t 02:00:00
#SBATCH --nodes=8
#SBATCH --ntasks-per-node=32
#SBATCH --mail-type=ALL
#SBATCH --mail-user=lbuchart@eoas.ubc.ca
#SBATCH --account=def-rstull

ml StdEnv/2023 intel/2025.2.0 openmpi/4.1.5
module load wrf/4.7.1

exp=TEST-REAL-POS1
cd ../exps/${exp}
edir=$(pwd)

dir_path=/home/lbuchart/scratch/les_boosting_output/${exp}/
mkdir -p $dir_path

rm -r rsl.*

# move into the scratch directory and link over all fires from the experiment directory
cd $dir_path

ln -sv ${edir}/* .

srun ./wrf.exe 1>wrf.log 2>&1

mkdir -p log
mv rsl.* log/
mv wrf.log log/

mkdir -p output
mv wrfout* output/

#rm -r namelist.input
#ln -sv namelist.input.restart namelist.input

#srun ./wrf.exe 1>wrf.log 2>&1

#mkdir -p log/restart
#mv rsl.* log/restart/
#mv wrf.log log/restart/
