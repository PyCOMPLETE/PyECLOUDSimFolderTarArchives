from __future__ import division, print_function
import os
import tarfile

def walk(folder):
    all_files = [os.path.join(folder, dir_) for dir_ in os.listdir(folder)]
    dirs = filter(os.path.isdir, all_files)
    files = filter(os.path.isfile, all_files)
    return dirs, files


def is_pyecloud_sim_folder(folder):
    dirs, files = walk(folder)
    output = ('simulations' in dirs and 'config' in dirs and ('run' in files or 'run_htcondor' in files))
    print('%s is a sim_folder: %s' % (folder, output))
    return output


def recursively_make_tar_archives(source_folder, target_folder, verbose=False):

    dirs, _ = walk(source_folder)

    if verbose:
        print('all subdirectories: %s' % dirs)

    for subdir in dirs,:
        base = os.path.basename(subdir)
        if is_pyecloud_sim_folder(subdir):
            tarname = os.path.join(target_folder, base+'.tar')
            if verbose:
                print('I would create %s from %s' % (tarname, subdir))
            else:
                with tarfile.open(tarname, 'w') as tar:
                    tar.add(subdir)
        else:
            new_target_folder = os.path.join(target_folder, base)
            if verbose:
                print('I would create %s' % new_target_folder)
            else:
                os.mkdir(new_target_folder)
            recursively_make_tar_archives(subdir, new_target_folder)

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument('source_folder')
    parser.add_argument('target_folder')
    parser.add_argument('-v', action='store_true')
    args = parser.parse_args()

    recursively_make_tar_archives(args.source_folder, args.target_folder, args.v)
