"""
This script generates configurations at a series of equidistant phi values taken from a previous metadynamics simulation.
It loads the trajectory, computes the C13=C14 dihedral angles for each configuration in the trajectory, 
and then looks for configurations at certain phi values within an equidistant range. 
For each phi value in the range, it finds the e-th configuration where the angle is within a delta of the phi value. 
It then saves this configuration to a file.

Parameters:
phi_range: The range of phi values from -pi to pi over 9 points.
trj: The trajectory loaded from a previous metadynamics simulation.
angles: The C13=C14 dihedral angles computed from the trajectory.
d: The delta around the phi-value for selecting configurations from the trajectory.
e: The index of the configuration to be taken.
"""

import numpy as np
import matplotlib.pyplot as plt
import mdtraj as md

trj         = md.load('../../metadynamics/sigma005/traj.xtc',top='6eid_capped_matched.gro') # load trajectory from previous metadynamics simulation
angles      = md.compute_dihedrals(trj,[[33,28,26,24]],periodic=False) # compute C13=C14 dihedral angles

d           = 0.001 # delta around phi-value for trajectories in configuration
e           = 3 # how manieth configuration found should be taken

phi_range   = np.linspace(0,1,9)*2*np.pi - np.pi # make phi range from -pi to pi over 9 points
phi_range   = phi_range[:-1] #drop last point because of periodicity
np.save('phi_range.npy',phi_range) # save phi range to file

for i,j in enumerate(phi_range): # loop over phi values in phi_range
    k       = np.where((angles>j-d)&(angles<j+d))[0][e] # find the e-th configuration where the angle is within a delta of the phi value
    trj[k].save(f'conf/conf{i}.xtc') # save configuration to file, indicating the index value in the filename
