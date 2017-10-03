from __future__ import division, print_function
import load_tar_archives as lta

# Created with 000_make_tars.py
tar_file = '/backup/local_backup_storage_tar/cell_scans/cell/simulations/LHC_Drift_6500GeV_sey1.10_1.1e11ppb_0.tar'

mat = lta.pyecltest_mat_from_tar(tar_file)
print("Keys of '%s/Pyecltest.mat':" % tar_file)
print(mat.keys())

sim_pars = lta.module_from_tar(tar_file, 'simulation_parameters.input', 'simulation_parameters')

print("Contents of '%s/simulation_parameters.input':" % tar_file)
print(dir(sim_pars))

