"""
This script generates PLUMED input files for a range of phi, improper1, and improper2 values. 
The PLUMED input files are used to define the collective variables and restraints for a molecular dynamics simulation.

The script iterates over the ranges of phi, improper1, and improper2 values. 
For each combination of these values, it generates a PLUMED input file with the defined torsions and restraints. 
The restraints are defined with different KAPPA values for the equilibration and production stages of the simulation.

Parameters:
phi_range: A numpy array of phi values representing the C13=C14 dihedral torsion angle. phi_range
improper1_range: A numpy array of improper dihedral values of the C13 methyl out of plane bending.
improper2_range: A numpy array of improper dihedral values of the C14 hydrogen out of plane bending.
i, j, k: Indices used to iterate over the ranges and to generate unique file names.

Output:
Generates a PLUMED input file 'plumed_input/eq1_plumed{i}{j}{k}.dat', 'plumed_input/eq2_plumed{i}{j}{k}.dat', and 'plumed_input/plumed{i}{j}{k}.dat' for each combination of i, j, k. 
Each file contains the commands to define the torsions and restraints for the simulation.
"""

import numpy as np

phi_range       = np.load('phi_range.npy')  # 9 equidistant values between -pi and pi radians
improper1_range = np.arange(-1.0,1.01,0.25) # 9 equidistant values between -1 and 1
improper2_range = np.arange(-1.0,1.01,0.25) # 9 equidistant values between -1 and 1

for i,l in enumerate(phi_range): # index and value of grid along phi CV
    for j,m in enumerate(improper1_range): # index and value of grid along improper1 CV
        for k,n in enumerate(improper2_range): # index and value of grid along improper2 CV
            # write the PLUMED input file for the first NVT equilibration stage with lower spring constants;
            # the value of the torsion angle and improper dihedrals of the harmonic biases are set to the correct grid values;
            # the input files are saved with the corresponding indices i, j, k
            # this happens in correspondence to the run files, where the plumed input files are called with the correct indices
            eq1_plumed = f'''phi: TORSION ATOMS=34,29,27,25
improper1: TORSION ATOMS=29,27,34,30
improper2: TORSION ATOMS=27,25,29,28

restraint-phi: RESTRAINT ARG=phi KAPPA=400.0 AT={l:.2f}
restraint-impr1: RESTRAINT ARG=improper1 KAPPA=100.0 AT={m:.2f}
restraint-impr2: RESTRAINT ARG=improper2 KAPPA=100.0 AT={n:.2f}

PRINT STRIDE=1000 ARG=phi,improper1,improper2,restraint-phi.bias,restraint-impr1.bias,restraint-impr2.bias FILE=EQCOLVAR/EQ1COLVAR{i}{j}{k}'''
            f = open(f'plumed_input/eq1_plumed{i}{j}{k}.dat','w')
            f.write(eq1_plumed)
            f.close()

            # write the PLUMED input file for the second NVT equilibration stage with the same spring constants as the production runs;
            eq2_plumed = f'''phi: TORSION ATOMS=34,29,27,25
improper1: TORSION ATOMS=29,27,34,30
improper2: TORSION ATOMS=27,25,29,28

restraint-phi: RESTRAINT ARG=phi KAPPA=600.0 AT={l:.2f}
restraint-impr1: RESTRAINT ARG=improper1 KAPPA=600.0 AT={m:.2f}
restraint-impr2: RESTRAINT ARG=improper2 KAPPA=600.0 AT={n:.2f}

PRINT STRIDE=1000 ARG=phi,improper1,improper2,restraint-phi.bias,restraint-impr1.bias,restraint-impr2.bias FILE=EQCOLVAR/EQ2COLVAR{i}{j}{k}'''
            f = open(f'plumed_input/eq2_plumed{i}{j}{k}.dat','w')
            f.write(eq2_plumed)
            f.close()

            # write the PLUMED input file for the production runs;
            plumed = f'''phi: TORSION ATOMS=34,29,27,25
improper1: TORSION ATOMS=29,27,34,30
improper2: TORSION ATOMS=27,25,29,28

restraint-phi: RESTRAINT ARG=phi KAPPA=600.0 AT={l:.2f}
restraint-impr1: RESTRAINT ARG=improper1 KAPPA=600.0 AT={m:.2f}
restraint-impr2: RESTRAINT ARG=improper2 KAPPA=600.0 AT={n:.2f}

PRINT STRIDE=1 ARG=phi,improper1,improper2 FILE=COLVAR/COLVAR_{i}{j}{k}
PRINT STRIDE=1000 ARG=phi,improper1,improper2,restraint-phi.bias,restraint-impr1.bias,restraint-impr2.bias FILE=COLVAR/COLVAR2_{i}{j}{k}'''
            f = open(f'plumed_input/plumed{i}{j}{k}.dat','w')
            f.write(plumed)
            f.close()
