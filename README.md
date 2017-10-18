# PyECLOUDSimFolderTarArchives

There are several example scripts:
000_make_tars.py: Recreates a local file tree consisting of the folder structure of PyECLOUD simulations.
  Single simulation folders are replaced by tar archives. Already existing files are ignored
001_rsync_to_eos_project.py: Copy this file tree to the EOS project space, while ignoring already existing files.
002_test_read_tar.py: A third loads the data from one of the previously created tar archives into python.

A typical workflow, where the 000 and 001 scripts only have to be adapted once.

1. A simulation study is finished and the resulting folder structure is on AFS.
  Structure: A folder that has a 'config' and a 'simulations' subfolder, while 'simulations' holds many single simulation folders.
2. Copy this folder to your local hard drive
3. Run 000_make_tars.py
4. Run 001_rsync_to_eos_project.py
