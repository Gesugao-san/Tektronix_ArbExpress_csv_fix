#!/usr/bin/env python3
# -*- coding: utf-8 -*-


### https://plotly.com/python/axes/#enumerated-ticks-with-tickvals-and-ticktext
### https://datatofish.com/matplotlib-charts-tkinter-gui/
### https://www.anycodings.com/1questions/4141887/how-can-i-draw-a-grid-onto-a-tkinter-canvas
### https://stackoverflow.com/a/17238509/8175291
### https://stackoverflow.com/q/19364166/8175291


from asyncio import constants
import tkinter as tk
from pandas import DataFrame
from matplotlib.figure import Figure  #import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from os import listdir, strerror, path
import os
import numpy as np


cwd      = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..'))  # os.getcwd()
path_in  = os.path.join(cwd, "in")
path_out = os.path.join(cwd, "out")

full_mode = False
out_arr1, out_arr2, out_dict, in_raw = [], [], {}, []
old_line = ''
data_min, data_max = 0, 0
time_min, time_max = 0, 0
with open(path.join(path_in, 'TRC01.CSV'), 'r') as ofile:
	for line in ofile:
		line = line.rstrip()
		if (("#CLOCK=" in line) or \
			("#SIZE=" in line) or \
			("[" in line) or \
			("]" in line)):
			continue

		if "," not in line:  # Format: "-5.1800E-04,-4.000E-02"
			continue

		in_raw += [line]
		processing = line.split(',')
		processing = [float(processing[0]), float(processing[1])]

		if (processing[0] > time_max): time_max = processing[0]
		if (processing[0] < time_min): time_min = processing[0]
		if (processing[1] > data_max): data_max = processing[1]
		if (processing[1] < data_min): data_min = processing[1]

		#if (processing[0] == old_line): processing[0] = float(str(processing[0]) + '1')
		#out_arr += [str(float(processing[0])) + ',' + str(float(processing[1])) + ',0,0']
		#out_arr += [str(float(line.split(',')[1])) + (',0,0' if full_mode else '')]
		out_arr1 += [processing[0]]
		out_arr2 += [processing[1]]
		old_line = processing[0]
	ofile.close()

max_lengt = 0
for el in out_arr1:
	el = str(el)
	if not '.' in el:
		continue
	pre_lengt = len(el.split('.')[1])
	if (pre_lengt > max_lengt):
		max_lengt = pre_lengt

for el in in_raw:
	if "," not in el:  # Format: "-5.1800E-04,-4.000E-02"
		continue
	processing = el.split(',')
	#print(processing)
	out_dict[f'%1.{max_lengt}f' % (float(processing[0]))] = float(processing[1])


data2 = {
	'Time': out_arr1,
	'Voltage (ADC-1)': out_arr2
}
df2 = DataFrame(data2, columns = ['Time', 'Voltage (ADC-1)'])


root = tk.Tk()
window = tk.Canvas(root)
window.pack()
plotWindow = tk.Frame(root)
plotWindow.pack()

figure = Figure(figsize = (14, 6), dpi=100)
ax = figure.add_subplot(111)
#x=[-100,100]
#y=[0,4]
#ax.plot(x, y, '-r')
df2 = df2[['Time', 'Voltage (ADC-1)']].astype(float).groupby('Time').sum()
df2.plot(kind = 'line', legend = True, ax = ax, color = 'r', marker = 'o', fontsize = 10)
ax.set_title('Time Vs. Voltage')

ax.grid()

#ax = ax.gca()
#ax.set_xticks(numpy.arange(0,1,0.5))

canvas = FigureCanvasTkAgg(figure, window) #root)
canvas.get_tk_widget().pack() #side=tk.LEFT, fill=tk.BOTH)

toolbar_frame = tk.Frame(root)
toolbar_frame.pack(side = tk.LEFT, fill = tk.BOTH) #.grid(row=21,column=4,columnspan=2)
toolbar = NavigationToolbar2Tk(canvas, plotWindow) #toolbar_frame )

out_arr3 = []
for x in range(0, len(out_arr1)):
	out_arr3 += [[out_arr1[x], out_arr2[x]]] # , float(0.0)

out_arr3.sort(reverse = True)
#X = 10 * np.random.rand(5, 3)
X = np.array(out_arr3)
#print('out_dict:\n', out_dict)

#print(out_arr1, out_arr2)
print('data limits:', data_min, data_max)
print('time limits:', time_min, time_max)
print('X type:', type(X))
print('X:\n', X)

numrows, numcols = X.shape
print(numrows, numcols)
def format_coord(x, y):
	_x = x
	#x = x * numrows
	#y = y * numcols
	col = int(x + 0.5)
	#row = int(y + 0.5)
	time = '%1.5f' % (x) # str(x or 0)
	#key_str = '%1.*f' % (max_lengt, x)
	#key_str = '{x:6.{max_lengt}f}'.format(max_lengt=max_lengt, x=x)
	key_str = f"{_x:1.{max_lengt}f}"
	key_float = float(key_str)
	if (((key_float <= data_max) or (key_float >= data_min)) and (key_float in out_dict)):
		data = str(out_dict[key_str]) #0.005462
	else:
		data = 'N\A'
	""" if ((col >= 0) and (col < numcols) and
		(row >= 0) and (row < numrows)):
		z = X[row, col]
		return 'x=%1.4f, y=%1.4f, z=%1.4f' % (float(x), float(y), float(z))
	else:
		return 'x=%1.4f, y=%1.4f, z=_.____' % (x, y) """
	#return 'x: %i (%1.4f), y: %i (%1.4f), time: %1.6f, data: %1.6f' % (col, x, row, y, time, data)
	return f'x: %i (%1.{max_lengt}f), key_str: %s, max_lengt: %i, time: %s, data: %s' % (col, x, key_str, max_lengt, time, data)

ax.format_coord = format_coord
canvas.draw()

root.mainloop()




