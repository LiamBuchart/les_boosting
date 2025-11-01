#!/bin/bash
#SBATCH -t 00:05:00
#SBATCH --mem-per-cpu=3000M
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=32
#SBATCH --mail-type=ALL
#SBATCH --mail-user=lbuchart@eoas.ubc.ca
#SBATCH --account=def-rstull

ml StdEnv/2023  gcc/12.3  openmpi/4.1.5
module load wrf/4.7.1

exp=TEST-REAL
cd ../exps/${exp}

mpirun -np 1 ./ideal.exe
