#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Naval Fate.

Usage:
  main.py
  naval_fate.py (-h | --help)
  naval_fate.py (-fm | --full_mode)

Options:
  -h --help        Show this screen.
  -fm --full_mode  Show version.

"""

# https://en.wikipedia.org/wiki/Scientific_notation#E_notation
# https://github.com/edrosten/eeprom-hacks/blob/master/analysis/v2/plot.sh

import os
import errno
from os import listdir, strerror, path
from os.path import isfile, join, basename
import argparse
import sys


class MyFormatter(
		argparse.ArgumentDefaultsHelpFormatter,
		argparse.MetavarTypeHelpFormatter):
	pass

parser = argparse.ArgumentParser(
	prog = 'main.py',
	description = 'Process some csv files to "AWG csv" type.',
	formatter_class = MyFormatter
)

parser.add_argument(
	#"-fm",
	"--full_mode",
	type = int,
	default = 0,
	help = "Process output data with additional data."
	#action = "store_const",
)
# parser.add_argument('integers', metavar='N', type=int, nargs='+', help='an integer for the accumulator')

parser.print_help(sys.stderr) #print(args.list)  #.accumulate(args.integers))
print()
#if len(sys.argv) == 1:
#	sys.exit(1)

args = parser.parse_args()
full_mode = bool(args.full_mode)

print('Staring...')
print('Working in full data output mode.' if full_mode else 'Working in minimal data output mode.')

cwd      = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))  # os.getcwd()
path_in  = os.path.join(cwd, "in")
path_out = os.path.join(cwd, "out")


set_template = [
	"MAGIC 4000",
	"Version 3",
	"Instrument AWG710",
	"Ch1WaveformSequence \"*.csv\"",  # replace it
	"Ch1Amplitude 2",
	"Ch1Offset 0",
	"Clock 100000000",
	"ClockReference Internal",
	"\n"
]

print('Reading input folder... ', end='')
onlyfiles = [f for f in listdir(path_in) if isfile(join(path_in, f))]
print('done.')

print('└ Files in input folder:', onlyfiles)

if len(onlyfiles) == 0:
	raise FileNotFoundError(
		errno.ENOENT,
		strerror(errno.ENOENT),
		path_in
	)

for current_file in onlyfiles:
	csv_filename = basename(current_file)
	print(f'Processing "{csv_filename} (main file)"... ', end='')
	out_arr = [
		'#CLOCK=1.0000000000e+002',
		('#SIZE=1000' if full_mode else '')
	]

	with open(path.join(path_in, current_file), 'r') as ofile:
		for line in ofile:
			line = line.rstrip()
			if (("#CLOCK=" in line) or \
				("#SIZE=" in line) or \
				("[" in line) or \
				("]" in line)):
				continue

			if "," not in line:  # Format: "-5.1800E-04,-4.000E-02"
				continue

			#processing = line.split(',')
			#out_arr += [str(float(processing[0])) + ',' + str(float(processing[1])) + ',0,0']
			out_arr += [str(float(line.split(',')[1])) + (',0,0' if full_mode else '')]
		ofile.close()

	print('done.')
	print(f'├ New file will contains (lines: {len(out_arr)}):')
	print('├', [out_arr[0], out_arr[1], out_arr[2], '...', out_arr[-1]])

	print(f'Saving "{csv_filename}" (main file)... ', end='')
	with open(path.join(path_out, current_file), 'w') as oofile:
		for line in out_arr:
			oofile.write(f"{line}" + '\n' if line else '')
		oofile.close()
	print('done.')

	set_filename = current_file.split('.')[0] + '.set'
	set_path     = path.join(path_out, set_filename)
	#print('set_filename:', type(set_filename))
	if full_mode:
		print(f'Saving "{set_filename}" (additional file)... ', end='')
		with open(set_path, 'w') as ooofile:
			#ooofile.write(set_template.replace("\"*.csv\""), f"\"{csv_filename}\"")
			replaced_arr = [x if (x != "Ch1WaveformSequence \"*.csv\"") else f"Ch1WaveformSequence \"{csv_filename}\"" for x in set_template]
			for line in replaced_arr:
				ooofile.write(f"{line}\n")

			ooofile.close()
		print(f'done.')
	else:
		if (os.path.isfile(set_path)):
			print(f'Detected old "{set_filename}" (additional file), deleting... ', end='')
			os.remove(set_path)
			print('done.')


print('Work done, exiting.')
#input()
#os.system("PAUSE")

#print(float("4.0000000000e+009"))  # print(format("4.0000000000e+009", 'f'))


#if __name__ == '__main__':






