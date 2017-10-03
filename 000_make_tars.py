#!/usr/bin/python2
import SimFolderTarArchives.create_tar_archives as cta

def cmd(dry_run):
    cta.recursively_make_tar_archives('/storage/local_backup_data', '/backup/local_backup_storage_tar', only_verbose=dry_run, delete_after=False)

cmd(dry_run=True)

cont = raw_input('Continue? yes/no\n')

if cont == 'yes':
    cmd(dry_run=False)
else:
    print('Exit!')

