# This is compatible with python3
from __future__ import print_function, division
import os
import imp
import tarfile

import scipy.io as sio

def pyecltest_mat_from_tar(tar_archive, mat_filename='Pyecltest.mat'):
    tar_base = os.path.basename(tar_archive)[:-4] # internal name of folder in archive

    with tarfile.open(tar_archive) as tar:
        file_ = tar.extractfile(os.path.join(tar_base, mat_filename))
        mat = sio.loadmat(file_)

    return mat

def module_from_tar(tar_archive, file_name, module_name):
    tar_base = os.path.basename(tar_archive)[:-4]

    with tarfile.open(tar_archive) as tar:
        # String that contains the specified file
        file_str = tar.extractfile(os.path.join(tar_base, file_name)).read()

    # Create module from this string
    # https://stackoverflow.com/questions/5362771/load-module-from-string-in-python
    module = imp.new_module(module_name)
    exec(file_str, module.__dict__)
    return module

def dump_file(tar_archive, file_name, output=None):
    tar_base = os.path.basename(tar_archive)[:-4]

    with tarfile.open(tar_archive) as tar:
        # String that contains the specified file
        file_str = tar.extractfile(os.path.join(tar_base, file_name)).read()

    if output is None:
        print(file_str)
    else:
        with open(output, 'w') as f:
            f.write(file_str)

