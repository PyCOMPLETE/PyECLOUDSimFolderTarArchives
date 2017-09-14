from __future__ import division, print_function
import os
import tarfile

def walk(folder):
    """
    Returns the contents of folder: directories and files.
    """
    all_files = [os.path.join(folder, dir_) for dir_ in os.listdir(folder)]
    dirs = filter(os.path.isdir, all_files)
    files = filter(os.path.isfile, all_files)
    return dirs, files

def is_pyecloud_sim_folder(folder):
    """
    Checks if a folder has the contents that identify it as a PyECLOUD simulation folder.
    """
    dirs, files = walk(folder)
    base_files = map(os.path.basename, files)
    base_dirs = map(os.path.basename, dirs)
    is_sim_folder = ('simulations' in base_dirs and 'config' in base_dirs and
              ('run' in base_files or 'run_htcondor' in base_files))
    return is_sim_folder

def make_tar_archive(source, tarname):
    """
    Does nothing if tarname already exists
    """
    target_folder = os.path.dirname(tarname)
    source_parent = os.path.dirname(source)
    source_base = os.path.basename(source)

    if os.path.isfile(tarname):
        print('%s already exists.' % tarname)
        return

    if not os.path.isdir(target_folder):
        os.makedirs(target_folder)

    print('Creating %s from %s' % (tarname, source))
    with tarfile.open(tarname, 'w') as tar:
        old_dir = os.getcwd()
        try:
            os.chdir(source_parent)
            tar.add(source_base)
        finally:
            os.chdir(old_dir)
    print('Done')

def recursively_make_tar_archives(source_folder, target_folder, only_verbose):
    """
    run with only_verbose=True to see what it is doing.
    """

    dirs, _ = walk(source_folder)

    for subdir in dirs:
        base = os.path.basename(subdir)
        if is_pyecloud_sim_folder(subdir):
            tarname = os.path.join(target_folder, base)+'.tar'
            if only_verbose:
                print('I would create %s from %s' % (tarname, subdir))
            else:
                make_tar_archive(subdir, tarname)
        else:
            new_target_folder = os.path.join(target_folder, base)
            recursively_make_tar_archives(subdir, new_target_folder, only_verbose)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('source_folder')
    parser.add_argument('target_folder')
    parser.add_argument('--real', action='store_true')
    args = parser.parse_args()

    only_verbose = not args.real

    recursively_make_tar_archives(args.source_folder, args.target_folder, only_verbose)

