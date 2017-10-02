from __future__ import division, print_function
import os
import shutil
import time
import tarfile

def list_dir(folder):
    """
    Returns the contents of folder: directories and files.
    """
    all_files = [os.path.join(folder, dir_) for dir_ in os.listdir(folder)]
    dirs = filter(os.path.isdir, all_files)
    files = filter(os.path.isfile, all_files)
    return dirs, files

def is_single_sim_folder(folder):
    dirs, files = list_dir(folder)
    base_files = set(map(os.path.basename, files))
    is_sim_folder = {'machine_parameters.input', 'beam.beam', 'job.job', 'Pyecltest.mat'}.issubset(base_files) and not (folder == 'config')
    return is_sim_folder

def is_full_simulation_folder(folder):
    """
    Checks if a folder has the contents that identify it as a PyECLOUD simulation folder.
    """
    dirs, files = list_dir(folder)
    base_files = map(os.path.basename, files)
    base_dirs = map(os.path.basename, dirs)
    is_sim_folder = ('simulations' in base_dirs and 'config' in base_dirs and
              ('run' in base_files or 'run_htcondor' in base_files))
    return is_sim_folder

def make_tar_archive(source, tarname, delete_after):
    """
    Does nothing if tarname already exists.
    """

    if os.path.isfile(tarname):
        print('%s already exists.' % tarname)
        return

    target_parent = os.path.dirname(tarname)
    source_parent = os.path.dirname(source)
    source_base = os.path.basename(source)

    if not os.path.isdir(target_parent):
        os.makedirs(target_parent)

    print('Creating %s from %s' % (tarname, source))
    with tarfile.open(tarname, 'w') as tar:

        # chdir is for shorter file names within the tar archive
        old_dir = os.getcwd()
        try:
            os.chdir(source_parent)
            tar.add(source_base)
        finally:
            os.chdir(old_dir)

    if delete_after:
        shutil.rmtree(source)
        print('Deleted %s. Done.' % source)
    else:
        print('Done.')

def make_tar_archive_multiple(source, tarname, delete_after):
    n_tries_max = 5
    for _ in xrange(n_tries_max):
        try:
            make_tar_archive(source, tarname, delete_after)
            return
        except IOError as e:
            print(e)
            time.sleep(5)
            if os.path.isfile(tarname):
                os.remove(tarname)
    raise e

def recursively_make_tar_archives(source_folder, target_folder, only_verbose, delete_after, single_sim_or_all_sim):
    """
    Arguments: source_folder, target_folder, only_verbose, delete_after
    Run with only_verbose=True to see what it is doing.
    """
    if single_sim_or_all_sim == 'single_sim':
        sim_folder_func = is_single_sim_folder
    elif single_sim_or_all_sim == 'all_sim':
        sim_folder_func = is_full_simulation_folder

    dirs, _ = list_dir(source_folder)

    for subdir in dirs:
        base = os.path.basename(subdir)
        if sim_folder_func(subdir):
            tarname = os.path.join(target_folder, base)+'.tar'
            if os.path.isfile(tarname):
                pass
            else:
                if only_verbose:
                    print('This would create %s from %s.' % (tarname, subdir))
                else:
                    make_tar_archive_multiple(subdir, tarname, delete_after, single_sim_or_all_sim)
        else:
            new_target_folder = os.path.join(target_folder, base)
            recursively_make_tar_archives(subdir, new_target_folder, only_verbose, delete_after)

if __name__ == '__main__':
    import argparse
    import sys

    if sys.version_info.major != 2:
        raw_input = input

    parser = argparse.ArgumentParser()
    parser.add_argument('source_folder')
    parser.add_argument('target_folder')
    parser.add_argument('--delete', help='delete source after creating target', action='store_true')
    args = parser.parse_args()

    if args.delete:
        cont = raw_input('Are you sure you want to delete after creating tar archives? yes/no\n')
        if cont != 'yes':
            print('Exit!')
            sys.exit()

    recursively_make_tar_archives(args.source_folder, args.target_folder, only_verbose=True, delete_after=False)
    cont = raw_input('Continue? yes/no\n')
    if cont == 'yes':
        recursively_make_tar_archives(args.source_folder, args.target_folder, only_verbose=False, delete_after=args.delete)

