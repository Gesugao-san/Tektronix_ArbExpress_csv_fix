#!/usr/bin/env python3
# -*- coding: utf-8 -*-


### https://stackoverflow.com/a/3579625/8175291
### https://www.techbeamers.com/python-copy-file/


from tkinter import Tk     # from tkinter import Tk for Python 3.x
from tkinter.filedialog import askopenfilename
from shutil import copyfile
import os, sys
import time
from os.path import basename


def displayFileStats(filepath):
	print(f'Stats of "{filepath}":')
	file_stats = os.stat(filepath)
	print('\tMode    :', file_stats.st_mode)
	print('\tCreated :', time.ctime(file_stats.st_ctime))
	print('\tAccessed:', time.ctime(file_stats.st_atime))
	print('\tModified:', time.ctime(file_stats.st_mtime))


print('Staring...')

cwd      = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))  # os.getcwd()
path_in  = os.path.join(cwd, "in")
path_out = os.path.join(cwd, "out")


#displayFileStats(os.path.join(cwd, 'src', __file__))
Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
# initialdir - https://stackoverflow.com/a/42040479/8175291
filepath = askopenfilename(title = 'Choose file to move in input folder', filetypes = [('CSV Files', '*.csv')] ) # show an "Open" dialog box and return the path to the selected file
if not filepath:
	exit(1)
filepath = os.path.normpath(filepath)
#filename = basename(filepath)
displayFileStats(filepath)

path_in_target = os.path.join(path_in, basename(filepath))
print(f'Copying "{filepath}"\n     to "{path_in_target}"...')
try:
	copyfile(filepath, path_in_target, follow_symlinks = True)
except IOError as e:
	print("Unable to copy file: %s" % e)
	exit(1)
except:
	print("Unexpected error:", sys.exc_info())
	exit(1)
print('Work done, exiting.')


