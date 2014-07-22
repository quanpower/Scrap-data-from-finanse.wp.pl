import Tkinter as tk
import csv
from finanse_wp import *

nameAr = []
codeAr = []

with open('indicators.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=';')
    for row in reader:
    	nameAr.append(row[0])
    	codeAr.append(row[1])

def select():
	# draw a chart
	index = nameAr.index(name_var.get())
	stock_id = codeAr[index]
	try:
		graphData(stock_id, 20, 200)
	except Exception as e:
		print 'Something went wrong.\nError details: ', e

root = tk.Tk()
# use width x height + x_offset + y_offset (no spaces!)
root.geometry("%dx%d+%d+%d" % (400, 60, 200, 150))
root.title("Simple Stock Chart Drawing Tool")
name_var = tk.StringVar(root)
name_var.set('Pick a stock')
choices = nameAr

option = tk.OptionMenu(root, name_var, *choices)
option.pack(side='left', padx=10, pady=10)
button = tk.Button(root, text="Draw a chart!", command=select)
button.pack(side='right', padx=20, pady=10)

root.mainloop()