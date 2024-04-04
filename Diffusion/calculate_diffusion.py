"""
This script calculates the diffusion coefficients for a range of phi, improper1, and improper2 values. 
The diffusion coefficients are calculated using a Cython module 'diffusionC'.

The script first defines constant and 3D grid values. 
It then imports the 'diffusionC' module. 
After that, it initializes arrays to store the diffusion coefficients and position averages for each simulation. 
Finally, it iterates over the windows (on the grid points) and corresponding trajectories and calculates the diffusion coefficients and average positions in each direction.

Parameters:
phi_range: A numpy array of phi values corresponding to the grid points on which the US windows are run.
impr1_range: A numpy array of improper1 values corresponding to the grid points on which the US windows are run.
impr2_range: A numpy array of improper2 values corresponding to the grid points on which the US windows are run.
i, j, k: Indices of the grid used to iterate over the ranges and to indicate the COLVAR names. This in correspondence with the indexing of the windows in the 3D US simulations.

Output:
The script saves the calculated diffusion coefficients and average positions for all windows to numpy files.
"""

import numpy as np
import scipy.constants as constants

###########################
###     CONSTANTS       ###
###########################

Nsteps      = 1000001   # 2 ns
dt          = 0.002     # ps 
kbT         = constants.k*300*constants.N_A/1000 # kJ/mol
beta        = 1/kbT
eqsteps     = 0
stride      = 1

###############################
###    3D US GRID VALUES    ###
###############################

# Load the grid values in accordance to 3D US windows
phi_range   = np.load('../phi_range.npy')
impr1_range = np.arange(-1.0,1.01,0.25)
impr2_range = np.arange(-1.0,1.01,0.25)
N_phi       = len(phi_range)    # 9
N_impr1     = len(impr1_range)  # 9
N_impr2     = len(impr2_range)  # 9
Nsims       = N_phi*N_impr1*N_impr2 # 729
print(f'Nsims = {Nsims}')

########################################
###   IMPORT DIFFUSION FROM CYTHON   ###
########################################

# To build the Cython diffusion module:
# python3 buildCythonModule.py build_ext --inplace
from diffusionC import diffusionC

#################################
###   DIFFUSION CALCULATION   ###
#################################

# Initialize arrays to store diffusion coefficients and average positions
# For each single window, we store the average position and the diffusion coefficient in each direction
# This means for all 729 grid points, we save 6 numbers: 3 corresponding to the average positions in phi, improper1 and improper2, and 3 corresponding to the diffusion coefficients in the same directions
# Consequently, we initialize 6 arrays of length 729 to store these values
diff_arr_phi    = np.zeros(Nsims) # store the diffusion coefficient in phi direction for each window
diff_arr_impr1  = np.zeros(Nsims) # store the diffusion coefficient in improper1 direction for each window
diff_arr_impr2  = np.zeros(Nsims) # store the diffusion coefficient in improper2 direction for each window
avg_arr_phi     = np.zeros(Nsims) # store the average phi value for each window
avg_arr_impr1   = np.zeros(Nsims) # store the average improper1 value for each window
avg_arr_impr2   = np.zeros(Nsims) # store the average improper2 value for each window

# Iterate over the 3D US grid values
l = 0 # index for the diffusion and average position arrays
for i in range(N_phi):
    for j in range(N_impr1):
        for k in range(N_impr2):
            directory       = f"../COLVAR/COLVAR_{i}{j}{k}" # directory name for the COLVAR files generated during 3D US simulations
            print(directory)
            # load data skipping the first row and loading only the second column, i.e. the relevant coordinate
            with open(directory) as f:
                lines  = (line for line in f if not line.startswith('#'))
                values = np.loadtxt(lines, usecols = (1,2,3), unpack = True)[eqsteps:]

            # unwrap phi values and remove discontinuities
            phi             = np.unwrap(values[0,:])
            # calculate the average phi value
            avg_phi         = np.mean(phi)

            # shift phi values to be between -pi and pi
            if avg_phi > np.pi:
                avg_phi -= 2*np.pi
            elif avg_phi < -np.pi:
                avg_phi += 2*np.pi

            # store the average phi value and the corresponding diffusion coefficient in phi direction
            avg_arr_phi[l]  = avg_phi # store the average phi value
            diff_arr_phi[l] = diffusionC(Nsteps, dt, stride).compute(phi) # compute diffusion coefficient in phi direction
            print(f'avg phi: {avg_phi}')
            print(f'diffusion phi: {diff_arr_phi[l]}')

            # unwrap improper1 values and remove discontinuities
            improper1         = np.unwrap(values[1,:])
            # calculate the average improper1 value
            avg_impr1         = np.mean(improper1)

            # store the average improper1 value and the corresponding diffusion coefficient in imporper1 direction
            avg_arr_impr1[l]  = avg_impr1 # store the average improper1 value
            diff_arr_impr1[l] = diffusionC(Nsteps, dt, stride).compute(improper1) # compute diffusion coefficient in improper1 direction
            print(f'avg improper1: {avg_impr1}')
            print(f'diffusion improper1: {diff_arr_impr1[l]}')

            # unwrap improper2 values and remove discontinuities
            improper2         = np.unwrap(values[2,:])
            # calculate the average improper2 value
            avg_impr2         = np.mean(improper2)

            # store the average improper2 value and the corresponding diffusion coefficient in imporper2 direction
            avg_arr_impr2[l]  = avg_impr2 # store the average improper2 value
            diff_arr_impr2[l] = diffusionC(Nsteps, dt, stride).compute(improper2) # compute diffusion coefficient in improper2 direction
            print(f'avg improper2: {avg_impr2}')
            print(f'diffusion improper2: {diff_arr_impr2[l]}')

            l += 1 # increment the index for the diffusion and average position arrays

# Save the diffusion coefficients and average positions to numpy files
np.save('diff_arr_phi.npy',diff_arr_phi)
np.save('diff_arr_impr1.npy',diff_arr_impr1)
np.save('diff_arr_impr2.npy',diff_arr_impr2)
np.save('avg_arr_phi.npy',avg_arr_phi)
np.save('avg_arr_impr1.npy',avg_arr_impr1)
np.save('avg_arr_impr2.npy',avg_arr_impr2)
