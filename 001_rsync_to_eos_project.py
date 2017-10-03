#!/usr/bin/python2
import sys
import os

if sys.version_info.major != 2:
    raw_input = input

user = 'pdijksta'

local_backup_folders = '/backup/local_backup_storage_tar/*'
hostname = '%s@lxplus.cern.ch' % user
target_backup_folder = '%s:/eos/project/e/ecloud-simulations/%s' % (hostname, user)

def main(option_str=''):
    cmd = 'rsync -ruv %s --ignore-existing %s %s' % (option_str, local_backup_folders, target_backup_folder)
    print('Username: %s' % hostname)
    status = os.system(cmd)
    if status != 0:
        raise SystemError('%s failed with status %i' % (cmd, status))

main('--dry-run')
cont = raw_input('Continue? yes/no\n')

if cont == 'yes':
    main()
else:
    print('Exit!')

