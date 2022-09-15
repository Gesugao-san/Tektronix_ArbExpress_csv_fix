#!/usr/bin/env python3
# -*- coding: utf-8 -*-


### https://plotly.com/python/axes/#enumerated-ticks-with-tickvals-and-ticktext
### https://datatofish.com/matplotlib-charts-tkinter-gui/
### https://www.anycodings.com/1questions/4141887/how-can-i-draw-a-grid-onto-a-tkinter-canvas


import tkinter as tk
from pandas import DataFrame
from matplotlib.figure import Figure  #import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)

data2 = {
	'Year': [1920,1930,1940,1950,1960,1970,1980,1990,2000,2010],
	'Unemployment_Rate': [9.8,12,8,7.2,6.9,7,6.5,6.2,5.5,6.3]
}
df2 = DataFrame(data2,columns=['Year','Unemployment_Rate'])


root = tk.Tk()
window = tk.Canvas(root)
window.pack()
plotWindow = tk.Frame(root)
plotWindow.pack()

figure = Figure(figsize=(6, 5), dpi=100)
ax = figure.add_subplot(111)
#x=[-100,100]
#y=[0,4]
#ax.plot(x, y, '-r')
df2 = df2[['Year','Unemployment_Rate']].groupby('Year').sum()
df2.plot(kind='line', legend=True, ax=ax, color='r',marker='o', fontsize=10)
ax.set_title('Year Vs. Unemployment Rate')

ax.grid()

#ax = ax.gca()
#ax.set_xticks(numpy.arange(0,1,0.5))

canvas = FigureCanvasTkAgg(figure, window) #root)
canvas.get_tk_widget().pack() #side=tk.LEFT, fill=tk.BOTH)

toolbar_frame = tk.Frame(root)
toolbar_frame.pack(side=tk.LEFT, fill=tk.BOTH) #.grid(row=21,column=4,columnspan=2)
toolbar = NavigationToolbar2Tk(canvas, plotWindow) #toolbar_frame )

canvas.draw()

root.mainloop()




