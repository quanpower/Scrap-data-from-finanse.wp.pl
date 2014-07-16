import Tkinter as tk
import csv
from finanse_wp import *

nameAr = []
codeAr = []

with open('stocks.csv', 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
    	nameAr.append(row[0])
    	codeAr.append(row[1])

def select():
	# wywolanie wykresu dla danego codeAr
	index = nameAr.index(var.get())
	stock_id = codeAr[index]
	graphData(stock_id, 20, 200)

root = tk.Tk()
# use width x height + x_offset + y_offset (no spaces!)
root.geometry("%dx%d+%d+%d" % (400, 80, 200, 150))
root.title("Simple Stock Chart Drawing Tool")

var = tk.StringVar(root)
# initial value
var.set('Pick a stock')

choices = nameAr
option = tk.OptionMenu(root, var, *choices)
option.pack(side='left', padx=10, pady=10)
button = tk.Button(root, text="Draw a chart!", command=select)
button.pack(side='right', padx=20, pady=10)

root.mainloop()