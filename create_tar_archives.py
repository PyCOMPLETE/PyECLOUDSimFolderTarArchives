from __future__ import division, print_function
import os
import tarfile
import shutil

def list_dir(folder):
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
    dirs, files = list_dir(folder)
    base_files = map(os.path.basename, files)
    base_dirs = map(os.path.basename, dirs)
    is_sim_folder = ('simulations' in base_dirs and 'config' in base_dirs and
              ('run' in base_files or 'run_htcondor' in base_files))
    return is_sim_folder

# Not used any more
def make_full_tar_archive(source, tarname, delete_after):
    """
    Does nothing if tarname already exists
    """
    target_parent = os.path.dirname(tarname)
    source_parent = os.path.dirname(source)
    source_base = os.path.basename(source)

    real_tarname = tarname + '.tar'

    if os.path.isfile(real_tarname):
        print('%s already exists.' % real_tarname)
        return

    if not os.path.isdir(target_parent):
        os.makedirs(target_parent)

    print('Creating %s from %s' % (real_tarname, source))
    with tarfile.open(real_tarname, 'w') as tar:
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

def make_split_tar_archive(source, target, delete_after):
    """
    Does nothing if tarname already exists
    """
    if os.path.isdir(target):
        print('%s already exists.' % target)
        return
    else:
        os.makedirs(target)

    print('Creating %s from %s' % (target, source))
    dirs, files = list_dir(source)
    for dir_ in (dirs + files):
        base_dir = os.path.basename(dir_)
        if base_dir == 'simulations':
            pass
        else:
            target_dir = os.path.join(target, base_dir)
            if os.path.isdir(dir_):
                shutil.copytree(dir_, target_dir)
            else:
                shutil.copy2(dir_, target_dir)

    source_sim_dir = os.path.join(source, 'simulations')
    single_sim_dirs, sim_files = list_dir(source_sim_dir)
    target_sim_dir = os.path.join(target, 'simulations')
    os.mkdir(target_sim_dir)

    for sim_file in sim_files:
        target_file = os.path.join(target_sim_dir, os.path.basename(sim_file))
        shutil.copy2(sim_file, target_file)
        print('Copy %s to %s' % (sim_file, target_file))

    print('Creating %s from %s' % (target_sim_dir, source_sim_dir))
    for single_sim_dir in single_sim_dirs:
        single_sim_base = os.path.basename(single_sim_dir)
        target_tarname = os.path.join(target_sim_dir, single_sim_base+'.tar')
        with tarfile.open(target_tarname, 'w') as tar:
            old_dir = os.getcwd()
            try:
                os.chdir(source_sim_dir)
                tar.add(single_sim_base)
                #print('Created %s from %s' % (target_tarname, single_sim_dir))
            finally:
                os.chdir(old_dir)

    if delete_after:
        shutil.rmtree(source)
        print('Deleted %s. Done.' % source)
    else:
        print('Done.')

def recursively_make_tar_archives(source_folder, target_folder, only_verbose, delete_after):
    """
    Run with only_verbose=True to see what it is doing.
    """

    dirs, _ = list_dir(source_folder)

    for subdir in dirs:
        base = os.path.basename(subdir)
        if is_pyecloud_sim_folder(subdir):
            tarname = os.path.join(target_folder, base)
            if only_verbose:
                print('This would create %s from %s' % (tarname, subdir))
            else:
                make_split_tar_archive(subdir, tarname, delete_after)
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

