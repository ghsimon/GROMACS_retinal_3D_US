"""
This script generates executable run files for two cycles of equilibration and a production run for a single trajectory in 3D Umbrella Sampling (US). 
Each trajectory is carried out on a single CPU, determined by the 'pinoffset' value.

The script creates necessary directories, prepares the system for simulation using 'gmx_mpi grompp', and runs the simulation using 'gmx_mpi mdrun'. 
It does this for the two equilibration stages and production run.

Parameters:
pinoffset: A 2D numpy array that determines the CPU allocation for each trajectory.
i, j, k: Indices used to iterate over the 'pinoffset' array and to generate unique file names.

Output:
Generates a shell script 'run{i}{j}{k}.sh' for each combination of i, j, k. Each script contains the commands to run the equilibration and production stages of the simulation.
"""

import numpy as np

pinoffset = np.arange(45)+1         # create an array of 45 elements from 1 to 45 representing the CPU allocation (1 trajectory per CPU at a time, 45 CPUs total)
pinoffset = pinoffset.reshape(9,5)  # reshape the array to a 9x5 matrix so CPUs can be allocated easily based on the gridpoint

for i in range(9): # index of grid along phi CV
    for j in range(9): # index of grid along improper1 CV
        for k in range(9): # index of grid along improper2 CV
            # write the commands to run the simulation to a shell script; 
            # each script runs one 3D US trajectory
            # indices i, j, k determine the position of the biasing potential on the 3D grid by calling the correct plumed input files
            # the pinoffset is assigned based on the first two indices: new pinoffsets are used for each different value of i and every two values of j
            # i.e. run00?.sh and run01?.sh will use the same pinoffset value, run02?.sh and run03?.sh will use the same pinoffset, run10?.sh and run11?.sh will use the same pinoffset, etc., with the k index always taking values between 0-8
            # this divides 729 simulations over 45 pinoffset values, with 16 simulations per pinoffset value
            run = f'''mkdir -p EQCOLVAR
mkdir -p COLVAR
mkdir -p eq1
mkdir -p eq2
mkdir -p us
mkdir -p traj

### First equilibration at lower spring constants for impropers
gmx_mpi grompp -f eq1_nvt.mdp -c conf/conf{i}.gro -p topol.top -r 6eid_capped_matched.gro -o eq1/eq1_nvt{i}{j}{k}.tpr
gmx_mpi mdrun -pin on -pinoffset {pinoffset[i,j//2]} -plumed plumed_input/eq1_plumed{i}{j}{k}.dat -deffnm eq1/eq1_nvt{i}{j}{k} -x eq1/eq1_traj{i}{j}{k}.xtc

### Equilibration at actual spring constants
gmx_mpi grompp -f eq2_nvt.mdp -c eq1/eq1_nvt{i}{j}{k}.gro -p topol.top -r 6eid_capped_matched.gro -o eq2/eq2_nvt{i}{j}{k}.tpr
gmx_mpi mdrun -pin on -pinoffset {pinoffset[i,j//2]}  -plumed plumed_input/eq2_plumed{i}{j}{k}.dat -deffnm eq2/eq2_nvt{i}{j}{k} -x eq2/eq2_traj{i}{j}{k}.xtc

### Production run
gmx_mpi grompp -f md.mdp -c eq2/eq2_nvt{i}{j}{k}.gro -t eq2/eq2_nvt{i}{j}{k}.cpt -p topol.top -r 6eid_capped_matched.gro -o us/us{i}{j}{k}.tpr
gmx_mpi mdrun -pin on -pinoffset {pinoffset[i,j//2]} -plumed plumed_input/plumed{i}{j}{k}.dat -deffnm us/us{i}{j}{k} -x traj/traj{i}{j}{k}.xtc
'''
            f = open(f'run_input/run{i}{j}{k}.sh','w')
            f.write(run)
