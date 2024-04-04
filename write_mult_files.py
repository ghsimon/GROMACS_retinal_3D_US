"""
This script generates multiple shell scripts (mult.sh files). Each generated shell script runs 16 other shell scripts (run.sh files) sequentially.

The script first creates a 2D numpy array 'pinoffset' with values from 1 to 45. 
It then iterates over this array. For each element of the array, it generates a shell script that contains bash commands to run 16 other shell scripts.
The 16 shell scripts correspond to 16 trajectories pinned to a specific CPU, as determined by the 'pinoffset' value in the 'run.sh' files. 
The index of the mult*.sh file corresponds to the 'pinoffset' value used for the 16 trajectories.

Parameters:
pinoffset: A 2D numpy array with values from 1 to 45.
i, j: Indices used to iterate over the 'pinoffset' array and to generate the correct names of the 16 run.sh files.

Output:
Generates a shell script 'mult/mult{pinoffset[i,j]}.sh' for each element of the 'pinoffset' array. 
Each generated script contains bash commands to run 16 shell scripts sequentially, corresponding to 16 trajectories pinned to a specific CPU.
"""
import numpy as np

pinoffset = np.arange(45)+1 # create an array of 45 elements from 1 to 45 representing the CPU allocation (1 trajectory per CPU at a time, 45 CPUs total)
pinoffset = pinoffset.reshape(9,5) # reshape the array to a 9x5 matrix so CPUs can be allocated easily based on the gridpoint

for i in range(9):
    for j in range(5):
        # write the commands to run the sequential simulations to a shell script;
        # each script runs 16 3D US trajectories sequentially
        # all 16 trajectories use the same pinoffset value, determined in the run.sh files
        mult = f'''bash run_input/run{i}{int(2*j)}{0}.sh
bash run_input/run{i}{int(2*j)}{1}.sh
bash run_input/run{i}{int(2*j)}{2}.sh
bash run_input/run{i}{int(2*j)}{3}.sh
bash run_input/run{i}{int(2*j)}{4}.sh
bash run_input/run{i}{int(2*j)}{5}.sh
bash run_input/run{i}{int(2*j)}{6}.sh
bash run_input/run{i}{int(2*j)}{7}.sh
bash run_input/run{i}{int(2*j)}{8}.sh
bash run_input/run{i}{int(2*j+1)}{0}.sh
bash run_input/run{i}{int(2*j+1)}{1}.sh
bash run_input/run{i}{int(2*j+1)}{2}.sh
bash run_input/run{i}{int(2*j+1)}{3}.sh
bash run_input/run{i}{int(2*j+1)}{4}.sh
bash run_input/run{i}{int(2*j+1)}{5}.sh
bash run_input/run{i}{int(2*j+1)}{6}.sh
bash run_input/run{i}{int(2*j+1)}{7}.sh
bash run_input/run{i}{int(2*j+1)}{8}.sh
'''
        f = open(f'mult/mult{pinoffset[i,j]}.sh','w')
        f.write(mult)
