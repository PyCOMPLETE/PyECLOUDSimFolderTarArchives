#!/usr/bin/python2
"""
This is an example script for the create_tar_archives utility.
In this case, the raw PyECLOUD simulation studies are located in data_source.
This command replicates the same data structure in data_destination,
but replaces single simulation folders by tar archives.
"""
from __future__ import division, print_function
import sys
import SimFolderTarArchives.create_tar_archives as cta

# python3 compatibility
if sys.version_info.major != 2:
    raw_input = input

data_source = '/storage/local_backup_data'
data_destination = '/backup/local_backup_storage_tar'

def cmd(dry_run):
    cta.recursively_make_tar_archives(data_source, data_destination, dry_run, delete_after=False)

cmd(dry_run=True)

cont = raw_input('Continue? yes/no\n')

if cont == 'yes':
    cmd(dry_run=False)
else:
    print('Exit!')

